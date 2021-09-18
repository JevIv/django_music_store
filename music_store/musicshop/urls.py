from django.urls import path
from .views import BaseView, ArtistDetailsView, AlbumDetailsView

urlpatterns = [
    path('', BaseView.as_view(), name='base'),
    path('<str:artist_slug>/', ArtistDetailsView.as_view(), name='artist_detail'),
    path('<str:album_slug>/', AlbumDetailsView.as_view(), name='album_detail'),

]