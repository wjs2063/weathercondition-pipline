프로젝트 기간 2022-07-01~ ing

# weathercondition-pipline
기상청 공공데이터 OPEN API 를 이용한 날씨데이터 자동화 구축

공공데이터-->  https://www.data.go.kr/iim/api/selectAPIAcountView.do

API --> RESTAPI




## USAGE 

``` docker-compose up -d ```















### Error 

url: (60) SSL certificate problem: unable to get local issuer certificate  
[2022-07-03 03:27:54,307] {bash.py:173} INFO - More details here: https://curl.haxx.se/docs/sslcerts.html  
[2022-07-03 03:27:54,311] {bash.py:173} INFO -   
[2022-07-03 03:27:54,315] {bash.py:173} INFO - curl failed to verify the legitimacy of the server and therefore could not  

요약하자면 curl 로 해당 url 불러오는 과정에서 certificate 문제가 생겼음  SSL 인증서와 관련있어보인다.    
 
