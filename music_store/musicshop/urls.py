from django.urls import path
from .views import BaseView, ArtistDetailsView, AlbumDetailsView, LoginView, RegistrationView

urlpatterns = [
    path('', BaseView.as_view(), name='base'),
    path('lobin/', LoginView.as_view(), name='login'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('<str:artist_slug>/', ArtistDetailsView.as_view(), name='artist_detail'),
    path('<str:album_slug>/', AlbumDetailsView.as_view(), name='album_detail'),

]