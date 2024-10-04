from rest_framework import serializers
from .models import Question, Choice

class ChoiceSerializer(serializers.ModelSerializer):
    content_type = serializers.SerializerMethodField()
    
    def get_content_type(self, obj):
        return obj.get_content_type_display()
    
    class Meta:
        model = Choice
        fields = ("pk", "content_type", "content")
    

class QuestionSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    answer = serializers.SerializerMethodField()

    def get_type(self, obj):
        return obj.get_type_display()
    
    def get_answer(self, obj):
        serializer = ChoiceSerializer(obj.choices, many=True)
        serializer.bind('', self)
        return serializer.data
    
    class Meta:
        model = Question
        fields = ("pk", "type", "title", "content", "answer")
