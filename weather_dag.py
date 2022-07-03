import json
import pathlib
import airflow
import requests
import requests.exceptions as request_exceptions
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
import datetime as dt
from pathlib import Path
import pandas as pd
import pendulum
import os.path 
#객체의 인스턴스생성 


weather_key={
    "POP":"강수확률",
    "PTY":"강수형태",
    "R06":"6시간강수량",
    "REH":"습도",
    "S06":"6시간신적설",
    "SKY":"하늘상태",
    "T3H":"3시간 기온",
    "TMN":"아침최저기온",
    "TMX":"낮 최고기온",
    "UUU":"풍속(동서성분)",
    "VVV":"풍속(남북성분)",
    "WAV":"파고",
    "VEC":"풍향",
    "WSD":"풍속",
    "T1H":"기온",
    "RN1":"1시간강수량",
    "UUU":"동서바람성분",
    "VVV":"남북바람성분",
    "REH":"습도",

    
}
#한국시간적용
local_tz=pendulum.timezone("Asia/Seoul")

dag=DAG(
    dag_id='download_weather_information',
    start_date=dt.datetime(2022,7,3,12,0,0,tzinfo=local_tz),
    schedule_interval=dt.timedelta(hours=1),
)
#1일전부터 시작

download_weathers_information=BashOperator(
    task_id="fetch_events",
    bash_command=(
        "mkdir -p /opt/airflow/dags/events && "
        "curl -k -o '/opt/airflow/dags/events/{{ds}}-{{'{:02}'.format(execution_date.hour)}}00.json' "
        "'https://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst?serviceKey=(발급받을API_KEY)&pageNo=1&numOfRows=1000&dataType=Json&base_date={{ds_nodash}}&base_time={{'{:02}'.format(execution_date.hour) }}00&nx=55&ny=127'"
    ),
    dag=dag
)


def _get_weathers(**context):
    input_path=context["templates_dict"]["input_path"]
    output_path=context["templates_dict"]["output_path"] 
    Path(output_path).parent.mkdir(exist_ok=True)
    events=pd.read_json(input_path)
    if events['response']['header']['resultCode']!='00':
        return -1
    temp=dict()
    #계속 중복되는형태이므로 1번만 저장
    # 변하는부분만 저장
    for x in events['response']['body']['items']['item']:
        temp['baseDate']=x['baseDate']
        temp['baseTime']='{:04d}'.format(int(x['baseTime']))
        temp['nx']=x['nx']
        temp['ny']=x['ny']
        temp[x['category']]=x['obsrValue']
    df1=pd.DataFrame(columns=temp.keys())
    df1=df1.append(temp,ignore_index=True)
    # 파일이 존재하면 
    if os.path.isfile(output_path):
        df=pd.read_csv(output_path,index_col=0)
        df=pd.concat([df,df1],ignore_index=True)
        df.to_csv(output_path)
    else:
        df1.to_csv(output_path,index=False)



get_weathers=PythonOperator(
    task_id='get_weathers',
    python_callable=_get_weathers,
    templates_dict={"input_path":"/opt/airflow/dags/events/{{ds}}-{{'{:02}'.format(execution_date.hour)}}00.json",
    "output_path":"/opt/airflow/dags/results/{{ds}}.csv"},
    dag=dag,
)

notify=BashOperator(
    task_id='notify',
    bash_command='echo "There are now $ (ls /tmp/data/events/ | wc -l) json files."',
    dag=dag
)

#task 실행순서 결정
download_weathers_information>>get_weathers>>notify
