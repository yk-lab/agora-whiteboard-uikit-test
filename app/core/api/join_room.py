import requests
from django.conf import settings
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView


class JoinRoomAPIView(APIView):
    def post(self, request, *args, **kwargs):
        agora_whiteboard_api_base = 'https://api.netless.link/v5'
        room_id = request.data.get('roomId')
        if not room_id:
            raise serializers.ValidationError('roomId is invalid.')

        token_resp = requests.post(
            f"{agora_whiteboard_api_base}/tokens/rooms/{room_id}",
            headers={
                "token": settings.AGORA_SDK_TOKEN,
                "Content-Type": "application/json",
                "region": settings.AGORA_WHITEBOARD_REGION
            },
            json={"lifespan": 3600000, "role": "writer"}
        )

        # "NETLESSROOM_YWs9XXXXXXXXXXXZWNhNjk" // Room token
        room_token = token_resp.json()

        return Response({
            'sdkConfig': {
                'appIdentifier': settings.AGORA_WHITEBOARD_APP_IDENTIFIER,
                'region': settings.AGORA_WHITEBOARD_REGION,
            },
            'joinRoom': {
                'uid': request.user.id,
                'uuid': room_id,
                'roomToken': room_token,
            }
        })
