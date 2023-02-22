from django.urls import path

from .api import CreateRoomAPIView, JoinRoomAPIView
from .views import TopView

urlpatterns = [
    path('', TopView.as_view(), name='top'),
    path("api/create-room", CreateRoomAPIView.as_view(),
         name="api_create_room"),
    path("api/join-room", JoinRoomAPIView.as_view(),
         name="api_join_room"),
]
