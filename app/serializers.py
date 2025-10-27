from rest_framework import serializers

class ProfileSerializer(serializers.Serializer):
    degree = serializers.CharField(max_length=100)
    skills = serializers.CharField()
    interests = serializers.CharField()
