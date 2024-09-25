from rest_framework.generics import ListAPIView
from .models import Question
from .serializers import QuestionSerializer

# Create your views here.
class QuestionListView(ListAPIView):
    queryset = Question.objects.all().order_by("type","title")
    serializer_class = QuestionSerializer