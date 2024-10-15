from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .chatbot import with_message_history
import uuid
import os
from django.conf import settings

def load_site_description(file_name):
    file_path = os.path.join(settings.BASE_DIR, 'chatbot', file_name)
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read().strip()

site_description = load_site_description('site_description.txt')


class ChatbotView(APIView):
    def post(self, request):
        user_input = request.data.get("input")

        if not user_input:
            return Response({"detail": "input이 필요합니다."}, status=status.HTTP_400_BAD_REQUEST)

        # 세션 ID를 자동으로 생성
        session_id = str(uuid.uuid4())


        result = with_message_history.invoke(
            {
                "input": user_input,
                "session_ids": session_id,
                "site_description": site_description 
            },
            {
                "configurable": {
                    "session_id": session_id,
                }
            }
        )


        return Response({"response": result.content, "session_id": session_id}, status=status.HTTP_200_OK)