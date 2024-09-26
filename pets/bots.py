from django.conf import settings
from openai import OpenAI
import json
from .models import PetCode

CLIENT = OpenAI(api_key=settings.OPENAI_API_KEY)

def pet_match_bot(datas):
    pet_infos = PetCode.objects.all()
    pet_dict = {}
    for pet_info in pet_infos:
        if pet_dict.get(pet_info.PCID.type):
            pet_dict[pet_info.PCID.type].append(pet_info.name)
        else:
            pet_dict[pet_info.PCID.type] = [pet_info.name]

    system_instructions = f"""
    반려견종을 추천해 줘
    추천해주는 견종은 소형견은 {pet_dict['소형견']}여기에서 
    중형견은 {pet_dict['중형견']}여기에서 
    대형견은 {pet_dict['대형견']}여기에서 
    있는 견종으로만 찾아줘
    이름과 카테고리는 내가 지정한 곳에서 넣어줘
    성격과 추천이유는 채택된 견종을 기준으로 말해줘
    출력은 json 형식에 맞춰줘
    예시로
    "name": "시츄",
    "category":"소형견",
    "personality":"시츄는 온순하고 사람을 좋아하는 성격을 가지고 있어 혼자 생활하는 분에게 좋은 동반자가 될 수 있어요. 털이 길어 손질이 필요하지만, 털 빠짐은 적습니다. 활동량도 보통 수준으로, 산책로가 있는 환경에서 적당히 산책을 즐길 수 있습니다.",
    "why": "시츄는 성격이 비교적 차분하고 훈련이 쉬워 초보자에게 적합한 견종입니다."
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
    

    return completion.choices[0].message