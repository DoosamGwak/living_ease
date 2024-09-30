from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
import json
from .models import Question
from .serializers import QuestionSerializer
from .bots import pet_match_bot, center_recommendation

# Create your views here.
class QuestionListView(ListAPIView):
    queryset = Question.objects.all().order_by("type","title")
    serializer_class = QuestionSerializer


class AIRecoomand(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        match = pet_match_bot(request.data, request.user)
        return Response(json.loads(match.content))
    

class MetchingCenter(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        response = center_recommendation(request.data.get("animal_name"))
        if response.get("error"):
            return Response(response, status=400)
        return Response(response)