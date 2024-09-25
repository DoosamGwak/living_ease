from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
import json
from .models import Question
from .serializers import QuestionSerializer
from .bots import pet_match_bot

# Create your views here.
class QuestionListView(ListAPIView):
    queryset = Question.objects.all().order_by("type","title")
    serializer_class = QuestionSerializer


class AIRecoomand(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        match = pet_match_bot(request.data)
        return Response(json.loads(match.content))