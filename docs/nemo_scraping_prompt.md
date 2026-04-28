# 네모 스크래핑 프롬프트

여기에 스크래핑 관련 프롬프트 또는 문서를 작성하세요.
## 1) HTTP 요청정보와 헤더
Request URL
https://www.nemoapp.kr/api/store/search-list?Subway=222&Radius=1000&CompletedOnly=false&NELat=37.52414970837205&NELng=127.05773954072409&SWLat=37.46772194890557&SWLng=126.97422665668671&Zoom=15&SortBy=29&PageIndex=0
Request Method
GET
Status Code
200 OK
Remote Address
3.168.178.110:443
Referrer Policy
strict-origin-when-cross-origin

referer
https://www.nemoapp.kr/store

## 2) Payload 정보
Subway=222&Radius=1000&CompletedOnly=false&NELat=37.52414970837205&NELng=127.05773954072409&SWLat=37.46772194890557&SWLng=126.97422665668671&Zoom=15&SortBy=29&PageIndex=0

## 3) 응답의 일부를 Response 에서 일부를 복사해서 넣어주기 (전체는 토큰 수 제한으로
어렵습니다.)
items 하단의 모든 데이터를 수집할 것

'''json
{
    "items": [
        {
'''
## 4) 한페이지가 성공적으로 수집되는지 확인하기 sqliteldb에 저장하기

* 수집한 데이터는 data 폴더에 저장하고, 소스코드는 src 폴더에 저장할것