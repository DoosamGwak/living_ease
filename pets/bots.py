from django.conf import settings
from openai import OpenAI
from accounts.models import User
import json
from .models import PetCode,  AIHistory
from .funtions import answer_insertt

CLIENT = OpenAI(api_key=settings.OPENAI_API_KEY)

def pet_match_bot(datas, userinfo):
    pet_infos = PetCode.objects.all()
    pet_dict = {}
    UID = User.objects.get(pk=userinfo.pk)
    answer_insertt(datas['user'], UID)
    answer_insertt(datas['pet'], UID)

    
    for pet_info in pet_infos:
        if pet_dict.get(pet_info.PCID.type):
            pet_dict[pet_info.PCID.type].append(pet_info.name)
        else:
            pet_dict[pet_info.PCID.type] = [pet_info.name]

    system_instructions = f"""
    반려견종을 2마리 추천해 줘
    추천해주는 견종은 소형견은 {pet_dict['소형견']}여기에서 
    중형견은 {pet_dict['중형견']}여기에서 
    대형견은 {pet_dict['대형견']}여기에서 
    있는 견종으로만 찾아줘
    이름과 카테고리는 내가 지정한 곳에서 넣어줘
    성격과 추천이유는 채택된 견종을 기준으로 말해줘
    출력은 json 형식에 맞춰줘
    예시로
    "num": "1"
    "name": "시츄",
    "category":"소형견",
    "personality":"시츄는 온순하고 사람을 좋아하는 성격을 가지고 있어 혼자 생활하는 분에게 좋은 동반자가 될 수 있어요. 털이 길어 손질이 필요하지만, 털 빠짐은 적습니다. 활동량도 보통 수준으로, 산책로가 있는 환경에서 적당히 산책을 즐길 수 있습니다.",
    "why": "시츄는 성격이 비교적 차분하고 훈련이 쉬워 초보자에게 적합한 견종입니다."
    "num": "2"
    "name": "래브라도 리트리버",
    "category":"대형견",
    "personality":"래브라도 리트리버는 매우 친근하고 상냥한 성격을 가지고 있으며, 사람과의 교감을 좋아하는 반려견입니다. 이들은 활발하고 에너지가 넘치지만, 고른 운동량을 받아야 건강하게 자라므로, 주변에 산책로가 있는 환경은 매우 좋습니다. 정원을 갖춘 곳이 없어도 아파트에서 충분히 생활 가능한 견종입니다.",
    "why": "래브라도 리트리버는 훈련이 수월해 초보자들에게 적합하며, 사회성이 뛰어나 가족 구성원과의 관계를 잘 유지할 수 있습니다. 또한 활동적인 성격 덕분에 산책을 즐기는 데 적합합니다."
    이렇게 json 형식에 맞춰서 출력해줘
    """
    
    completion = CLIENT.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content":system_instructions,
            },
            {
                "role": "user",
                "content": str(datas),
            },
        ],
        response_format={"type": "json_object"}
    )
    
    answer=json.loads(completion.choices[0].message.content)
    AIHistory.objects.create(UID=UID, question=datas, answer=answer)
    return completion.choices[0].message
