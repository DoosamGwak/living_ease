from langchain_openai import ChatOpenAI
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from petmily import settings


store = {}


# 세션 ID를 기반으로 세션 기록을 가져오는 함수
def get_session_history(session_ids: str) -> BaseChatMessageHistory:
    if session_ids not in store:
        chat_history = ChatMessageHistory()
        # 새로운 ChatMessageHistory 객체를 생성하여 store에 저장
        store[session_ids] = chat_history
    return store[session_ids]


model = ChatOpenAI(temperature=0.7, openai_api_key=settings.OPENAI_API_KEY)
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "너는 Q&A에 능숙한 어시스턴트야. 이 사이트는 {site_description}에 설명하는 것처럼 작동하는 사이트야. 이 설명 안에서만 대답해줘.",
        ),
        # 대화 기록을 변수로 사용, history 가 MessageHistory 의 key 가 됨
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),  # 사용자 입력을 변수로 사용
    ]
)

runnable = prompt | model

# RunnableWithMessageHistory 객체 생성
with_message_history = RunnableWithMessageHistory(
    runnable,  # 실행할 Runnable 객체
    get_session_history,  # 세션 기록을 가져오는 함수
    input_messages_key="input",  # 입력 메시지의 키 (사용자 입력)
    history_messages_key="history",  # 기록 메시지의 키 (대화 히스토리)
)
