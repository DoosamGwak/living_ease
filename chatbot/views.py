from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .chatbot import with_message_history, get_session_history
import uuid
import os
from django.conf import settings
from langchain.memory.buffer import ConversationBufferMemory

def load_site_description(file_name):
    file_path = os.path.join(settings.BASE_DIR, 'chatbot', file_name)
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read().strip()

site_description = load_site_description('site_description.txt')


class ChatbotView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self, request):
        user_input = request.data.get("input")
        session_id = request.data.get("session_id")
        
        if not user_input:
            return Response({"detail": "input이 필요합니다."}, status=status.HTTP_400_BAD_REQUEST)

        if not session_id:
            session_id = str(uuid.uuid4())
        user = request.user

        # 세션 기록 가져오기
        session_history = get_session_history(session_id)

        # 유저 환영 메시지 추가
        if len(session_history.messages) == 0:
            session_history.add_ai_message(f"안녕하세요 {user.nickname}님, 무엇을 도와드릴까요?")
            
        result = with_message_history.invoke(
            {
                "input": user_input,
                "session_ids": session_id,
                "site_description": site_description,
                "history": session_history.messages
            },
            {
                "configurable": {
                    "session_id": session_id,
                }
            }
        )


        return Response({"response": result.content, "session_id": session_id,"user": user.nickname}, status=status.HTTP_200_OK)