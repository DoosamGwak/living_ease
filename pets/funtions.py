from django.conf import settings
import json
import requests
from .models import Answer,  Question
from .data_petcode import DATA_PET
from .gecode import SIDOGUN


DATA = settings.DATA_API_KEY


# 설문 리스트에 대한 답변 저장
def answer_insertt(qustions, UID):
    for key,data  in qustions.items():
        if not key.find("question"): continue
        numbers = int(''.join(map(str, [int(num) for num in key if num.isdigit()])))
        qid =  Question.objects.filter(pk=numbers)
        if qid.exists():
            Answer.objects.create(QID=qid[0], UID=UID, content=data)


# 공공 API를 활용하여 견종별 분양소 조회
def center_recommendation(data):
    animal_name = data.get("animal_name")
    page = data.get("page") if  data.get("page") else 1
    if DATA_PET.get(animal_name):
        animal_code = DATA_PET[animal_name]
    else:
        return {"detail" : "조회 하려는 견종은 현재 제공하고 있지 않습니다."}

    # petcode 조회
    # url = "http://apis.data.go.kr/1543061/abandonmentPublicSrvc/kind"
    # params ={"serviceKey" : DATA,  "up_kind_cd" : "417000", "_type" : "json" }
    # response = requests.get(url, params=params)


    # petcode를 통한 상세조회
    url = "http://apis.data.go.kr/1543061/abandonmentPublicSrvc/abandonmentPublic"
    params ={"serviceKey" : DATA,  "upkind" : "417000", "kind" : animal_code, "state" : "notice", "_type" : "json","numOfRows": 5, "pageNo":page }
    if data.get("address"):
        check_address = data.get("address").split()
        params["upr_cd"] = SIDOGUN[check_address[0]]["uprCd"]
        if check_address[0][-1] == "도":
            params["org_cd"] = SIDOGUN[check_address[0]][check_address[1]]["orgCd"]

    response = requests.get(url, params=params)

    answer = json.loads(response.text)["response"]["body"]["items"]
    if len(answer) > 0:
        answer["pageNo"] = json.loads(response.text)["response"]["body"]["pageNo"]
        answer["totalCount"] = json.loads(response.text)["response"]["body"]["totalCount"]
        for i, k in enumerate(answer["item"]):
            answer["item"][i]= {
                "name": animal_name,
                "popfile": k.get("popfile"),
                "age": k.get("age"),
                "sexCd": k.get("sexCd"),
                "careNm":  k.get("careNm"),
                "careAddr":k.get("careAddr")
            }
    else:
        answer = {
            "detail": "해당 견종은 현재 해당 지역에 공고중이 아닙니다."
        }

    return answer

