from langchain_openai import ChatOpenAI
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from petmily import settings
from pets.models import PetCode


store = {}  # 세션별로 대화 기록을 저장하는 딕셔너리, 세션 ID를 키로 사용


# 세션 ID를 기반으로 세션 기록을 가져오는 함수
def get_session_history(session_ids: str) -> BaseChatMessageHistory:
    """
    주어진 세션 ID에 대한 대화 기록을 가져옴.
    세션 기록이 없으면 새롭게 생성하고 기본 메시지를 추가.
    """
    
    if session_ids not in store:  # 세션 ID가 store 딕셔너리에 없다면
        chat_history = ChatMessageHistory()  # 새 대화 기록 객체 생성
        # 새롭게 생성한 대화 기록에 AI의 기본 환영 메시지를 추가
        chat_history.add_ai_message("안녕하세요, 무엇을 도와드릴까요?")
        store[session_ids] = chat_history  # 새 대화 기록을 store에 세션 ID와 함께 저장
    return store[session_ids]  # 해당 세션 ID의 대화 기록 반환


# OpenAI의 GPT 모델을 설정하는 객체, temperature는 모델의 응답의 창의성을 결정 (0.7은 적당한 창의성)
model = ChatOpenAI(temperature=0.7, openai_api_key=settings.OPENAI_API_KEY)

# 대화 템플릿을 생성하는 객체. 시스템 메시지와 사용자의 메시지를 기반으로 대화의 틀을 만듦
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            # 시스템 메시지: 이 어시스턴트는 Q&A에 특화되어 있고, 사이트 설명을 바탕으로 답변해야 함
            "너는 Q&A에 능숙한 어시스턴트야. 이 사이트는 {site_description}에 설명하는 것처럼 작동하는 사이트야. 이 설명 안에서만 대답해줘.",
        ),
        # MessagesPlaceholder: 대화 기록을 변수로 사용, history가 대화 히스토리의 자리 표시자가 됨
        MessagesPlaceholder(variable_name="history"),
        # 사용자 입력을 변수로 사용하여 템플릿에 넣음
        ("human", "{input}"),  # 사용자의 질문/입력 부분
    ]
)

# prompt (대화 템플릿)과 모델을 파이프라인으로 연결 (대화 템플릿의 출력을 모델로 전달)
runnable = prompt | model

# 대화 히스토리를 관리하는 객체 생성
with_message_history = RunnableWithMessageHistory(
    runnable,  # 실행할 대화 템플릿과 모델 파이프라인을 runnable에 연결
    get_session_history,  # 세션 ID에 따른 대화 기록을 가져오는 함수 연결
    input_messages_key="input",  # 사용자 입력이 담기는 키 (사용자의 질문 메시지)
    history_messages_key="history",  # 대화 기록(히스토리)이 담기는 키
)


pet_infos = PetCode.objects.all()
pet_dict = {}
for pet_info in pet_infos:
    if pet_dict.get(pet_info.PCID.type):
        pet_dict[pet_info.PCID.type].append(pet_info.name)
    else:
        pet_dict[pet_info.PCID.type] = [pet_info.name]

prompt2 = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "너는 견종을 추천하는 유능한 어시스턴트야. 이 사이트는 {pet_description}에 설문내용에 대한 답변을 받아 견종을 추천 해주는 사이트야. 이 안에서만 대답해줘."
            f"추천시에는 반려견종을 2마리 추천해 줘 추천해주는 견종은 소형견은 {pet_dict['소형견']}여기에서  중형견은 {pet_dict['중형견']}여기에서  대형견은 {pet_dict['대형견']}여기에서  있는 견종으로만 찾아줘"
            "반드시 추천 견종은 지정해준 견종으로 추천을 해주고 더이상 추천할 견종이 없으면 없다고 솔직하게 말해줘"
            ,
        ),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"), 
    ]
)

runnable2 = prompt2 | model


with_message_history2 = RunnableWithMessageHistory(
    runnable2,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history",
)

