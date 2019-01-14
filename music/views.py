from rest_framework import generics
from .models import Song
from .serializer import SongsSerializer

# Create your views here.
class ListSongsView(generics.ListAPIView):
    queryset = Song.objects.all()
    serializer_class = SongsSerializer
