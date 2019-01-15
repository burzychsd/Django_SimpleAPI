from django.urls import path
from .views import ListSongsView, SongDetailView, LoginView

urlpatterns = [
    path('songs/', ListSongsView.as_view(), name="songs-all"),
    path('songs/<int:id>', SongDetailView.as_view(), name="song-detail"),
     path('auth/login', LoginView.as_view(), name='auth-login')
]