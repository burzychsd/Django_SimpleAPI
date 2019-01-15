from rest_framework import serializers
from .models  import  Song

class SongsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ('title', 'artist')

class TokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=255)