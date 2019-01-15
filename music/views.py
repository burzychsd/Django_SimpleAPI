from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import status
from .models import Song
from .serializer import SongsSerializer

# Create your views here.
class ListSongsView(generics.ListAPIView):
    queryset = Song.objects.all()
    serializer_class = SongsSerializer

    def post(self, request, *args, **kwargs):
        a_song = Song.objects.create(
            title=request.data['title'],
            artist=request.data['artist']
        )
        return Response(
            data=SongsSerializer(a_song).data,
            status=status.HTTP_201_CREATED
        )

class SongDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Song.objects.all()
    serializer_class = SongsSerializer

    def get(self, request, *args, **kwargs):
        try:
            a_song = self.queryset.get(id=kwargs['id'])
            return Response(SongsSerializer(a_song).data)
        except Song.DoesNotExist:
            return Response(
                data={
                    'message': 'Song with id: {} does not exist'.format(kwargs['id'])
                },
                status=status.HTTP_404_NOT_FOUND
            )
    
    def put(self, request, *args, **kwargs):
        try:
            a_song = self.queryset.get(id=kwargs['id'])
            serializer = SongsSerializer()
            updated_song = serializer.update(a_song, request.data)
            return Response(SongsSerializer(updated_song).data)
        except Song.DoesNotExist:
            return Response(
                data={
                    'message': 'Song with id: {} does not exist'.format(kwargs['id'])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, *args, **kwargs):
        try:
            a_song = self.queryset.get(id=kwargs['id'])
            a_song.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Song.DoesNotExist:
             return Response(
                data={
                    'message': 'Song with id: {} does not exist'.format(kwargs['id'])
                },
                status=status.HTTP_404_NOT_FOUND
            )
