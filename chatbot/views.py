from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .chatbot import with_message_history
import uuid
import os
from django.conf import settings

# 파일에서 사이트 설명을 불러오는 함수
def load_site_description(file_name):
    """
    지정된 파일에서 사이트 설명을 읽어오는 함수.
    파일 경로는 BASE_DIR/chatbot/ 아래에 위치하며, UTF-8 인코딩으로 파일을 읽음.
    """
    # settings.BASE_DIR을 기준으로 'chatbot' 폴더 안의 파일 경로를 지정
    file_path = os.path.join(settings.BASE_DIR, 'chatbot', file_name)
    
    # 파일을 읽기 모드로 열고 내용을 반환 (UTF-8로 인코딩, strip()으로 공백 제거)
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read().strip()

# 사이트 설명 파일을 로드하여 변수에 저장 ('site_description.txt' 파일 사용)
site_description = load_site_description('site_description.txt')


# 사용자의 입력을 처리하고 AI 응답을 반환하는 APIView 클래스
class ChatbotView(APIView):
    def post(self, request):
        """
        POST 요청으로 들어온 사용자의 입력을 받아 처리하고, AI의 응답을 반환하는 메소드.
        """
        # 클라이언트가 보낸 데이터에서 'input' 값을 가져옴
        user_input = request.data.get("input")

        # 'input' 값이 없으면 400 Bad Request와 함께 에러 메시지를 반환
        if not user_input:
            return Response({"detail": "input이 필요합니다."}, status=status.HTTP_400_BAD_REQUEST)

        # 세션 ID를 자동으로 생성하여 사용 (UUID4 형식)
        session_id = str(uuid.uuid4())

        # with_message_history 객체를 통해 대화 처리를 수행
        result = with_message_history.invoke(
            {
                "input": user_input,  # 사용자의 입력을 전달
                "session_ids": session_id,  # 생성된 세션 ID 전달
                "site_description": site_description  # 로드된 사이트 설명 전달
            },
            {
                "configurable": {
                    "session_id": session_id,  # 세션 ID를 설정 가능하게 전달
                }
            }
        )

        # AI의 응답과 세션 ID를 반환, 200 OK 상태 코드와 함께 전송
        return Response({"response": result.content, "session_id": session_id}, status=status.HTTP_200_OK)