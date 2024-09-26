from rest_framework import serializers
from .models import Question

class QuestionSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()

    def get_type(self, obj):
        return obj.get_type_display()
    
    class Meta:
        model = Question
        fields = ("pk", "type", "title", "content", )

