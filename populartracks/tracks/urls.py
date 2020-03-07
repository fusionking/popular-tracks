from django.urls import path

from tracks.views import SetTokenView, GetTracksView


urlpatterns = [
    path('tracks/<genre>/', GetTracksView.as_view(),
         name='tracks'),
    path('set-token/', SetTokenView.as_view(), name='set-token')
]
