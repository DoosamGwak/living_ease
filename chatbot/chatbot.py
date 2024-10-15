from langchain_openai import ChatOpenAI
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from petmily import settings


store = {}


def get_session_history(session_ids: str) -> BaseChatMessageHistory:
    print(f"세션 ID: {session_ids}")
    if session_ids not in store:
        chat_history = ChatMessageHistory()
        chat_history.add_ai_message("안녕하세요, 무엇을 도와드릴까요?")
        store[session_ids] = chat_history
    return store[session_ids]


model = ChatOpenAI(temperature=0.7, openai_api_key=settings.OPENAI_API_KEY)
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "너는 Q&A에 능숙한 어시스턴트야. 이 사이트는 {site_description}에 설명하는 것처럼 작동하는 사이트야. 이 설명 안에서만 대답해줘.",
        ),

        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
    ]
)

runnable = prompt | model


with_message_history = RunnableWithMessageHistory(
    runnable,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history", 
)
