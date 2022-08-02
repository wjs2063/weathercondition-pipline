프로젝트 기간 2022-07-01~ ing

## DB구축.zip파일 사용법 
- 압축풀고 terminal에서 해당폴더로 진입  
- ``` docker-compose up -d ```
- ``` docker ps -a ``` 로  컨테이너 실행여부 확인
- 1분후 local host  웹서버로 진입후 admin-> connection 에서 추가  conn_id : my_postgres conn_type : postgres , localhost , airflow:airflow 로 설정 
- 그리고 DAG 실행 
- Tableau 로 해당 DB 서버에 맞는 port 로 접속 
- 사용자 지정 SQL 로 원하는 sql 문 작성 (group by 보단 over( partition by 가 더 유용할수있음) 
- ex )  select tm,hour,sub_city,AVG(t1h) from weather_info group by sub_city,tm,hour order by tm,hour,sub_city  ( Nan 값 또는 -999 등 이상한값이 주어지는경우는)  
- 추후에 데이터 분석 또는 머신러닝 전에 전처리를 따로 해주어야함 



# weathercondition-pipline
기상청 공공데이터 OPEN API 를 이용한 날씨데이터 자동화 구축

공공데이터-->  https://www.data.go.kr/iim/api/selectAPIAcountView.do

API --> RESTAPI  
API_KEY: 위 사이트에서 발급받은 개인 API_KEY 

Data Partitioning 을 통한 파일 별도 관리 

task:  
1.download_weather_information : rest_api로 부터 json파일 저장  
2.get_weathers                 : 로컬의 json파일로부터 dataframe 생성후 csv파일로 누적저장  
3.notify                       : webserver 에서 모니터링 





## USAGE 

``` docker-compose up -d ```















## Error 
1. 
url: (60) SSL certificate problem: unable to get local issuer certificate  
[2022-07-03 03:27:54,307] {bash.py:173} INFO - More details here: https://curl.haxx.se/docs/sslcerts.html  
[2022-07-03 03:27:54,311] {bash.py:173} INFO -   
[2022-07-03 03:27:54,315] {bash.py:173} INFO - curl failed to verify the legitimacy of the server and therefore could not  

요약하자면 curl 로 해당 url 불러오는 과정에서 certificate 문제가 생겼음  SSL 인증서와 관련있어보인다.    
 
해결 : curl -k 라는 옵션을 추가해서 verify 를 거치지않는형태로 만들어준다   
    : 또는 송신 -> 수신 측에서 http요청 -> 수신(비암호화) 로 바꿈 즉 http 요청을 하는것  즉 해당소스코드에서 https:-> http 로 바꾸고 verify 옵션없애줌 



2. Bash_Operator 로 json 파일을 저장하는 자동화부분에서 JSON 파트가 APPLCATION_ERROR 만 뜨게된다...

해결: Bash_operator 내부에 쌍따옴표  " 안에 명령어를 작성하는경우가 " 있다. curk -k -o '디렉토리경로' 그리고 '{url주소}' 를 적게될텐데 꼭 작은 따옴표로 적어주자  

3. airflow 의 timezone
- 기본적으로 airflow 는 UTC 를 사용한다. 
- 그렇다면 timezone을 Asia/Seoul 로 바꿔서 해결하면 되지않을까?  
- 대답은 No 이다. 이유는 start_date timezone을 서울로바꾼다고해도 airflow 내부에서 다시 UTC 로 변환해서 진행한다.

4. airflow 계속 켜두어야하는데 노트북에 상당한 무리가간다. 
- 간단한 해결책으로는 AWS EC2 에 배포하여 상시 켜두고싶은데 과금이생길까봐 살짝 두려움..
