from django.urls import path

from tracks.views import GetTokenView, GetTracksView


urlpatterns = [
    path('tracks/<genre>/', GetTracksView.as_view(),
         name='tracks'),
    path('get-token/', GetTokenView.as_view(), name='get-token')
]
