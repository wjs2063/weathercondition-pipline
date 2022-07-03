프로젝트 기간 2022-07-01~ ing

# weathercondition-pipline
기상청 공공데이터 OPEN API 를 이용한 날씨데이터 자동화 구축

공공데이터-->  https://www.data.go.kr/iim/api/selectAPIAcountView.do

API --> RESTAPI

API_KEY: 위 사이트에서 발급받은 개인 API_KEY 


task:
1.download_weather_information : rest_api로 부터 json파일 저장  
2.get_weathers                 : 로컬의 json파일로부터 dataframe 생성후 csv파일로 누적저장  
3.notify                       : webserver 에서 모니  



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


2. Bash_Operator 로 json 파일을 저장하는 자동화부분에서 JSON 파트가 APPLCATION_ERROR 만 뜨게된다...

해결: Bash_operator 내부에 쌍따옴표  " 안에 명령어를 작성하는경우가 " 있다. curk -k -o '디렉토리경로' 그리고 '{url주소}' 를 적게될텐데 꼭 작은 따옴표로 적어주자  

3. airflow 의 timezone
- 기본적으로 airflow 는 UTC 를 사용한다. 
- 그렇다면 timezone을 Asia/Seoul 로 바꿔서 해결하면 되지않을까?  
- 대답은 No 이다. 이유는 start_date timezone을 서울로바꾼다고해도 airflow 내부에서 다시 UTC 로 변환해서 진행한다. 
