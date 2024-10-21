from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import json
from .models import Question
from .serializers import QuestionSerializer, AIHistorySerializer
from .bots import pet_match_bot
from .funtions import center_recommendation


# Create your views here.
# 설문 내역 조회
class QuestionListView(ListAPIView):
    queryset = Question.objects.all().order_by("type", "title")
    serializer_class = QuestionSerializer

# AI 추천 조회 및 추천
class AIRecoomand(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        ai_answer = request.user.aihistorys.all()
        if len(ai_answer) == 0:
            return Response({"detail": "추천받은 내용이 없습니다."}, status=400)
        ai_answer = ai_answer.last().answer.replace("'", '"')
        return Response(json.loads(ai_answer))

    def post(self, request):
        if not request.data or not request.user:
            return Response({"detail": "설문 내용이 비어있습니다."}, status=400)
        match = pet_match_bot(request.data, request.user)
        return Response(json.loads(match.content))

# 견종 에 따른 보호소 위치 조회
class MetchingCenter(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        response = center_recommendation(request.data)
        if response.get("detail"):
            return Response(response, status=400)
        return Response(response)
    

# AI 답변 내용 저장
class AIAnserWrite(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not request.data:
            return Response({"detail": "내용이 비어있습니다."}, status=400)
        
        data = {
            "UID": request.user.pk,
            "question": request.data.get("pet1").get("question"),
            "answer": json.dumps(request.data)
        }
        
        serializer = AIHistorySerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status=201)
        
