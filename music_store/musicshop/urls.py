from django.urls import path
from .views import BaseView, ArtistDetailsView, AlbumDetailsView, LoginView, RegistrationView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', BaseView.as_view(), name='base'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('<str:artist_slug>/', ArtistDetailsView.as_view(), name='artist_detail'),
    path('<str:album_slug>/', AlbumDetailsView.as_view(), name='album_detail'),

]