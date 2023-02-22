import requests
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView


class CreateRoomAPIView(APIView):
    def post(self, request, *args, **kwargs):
        agora_whiteboard_api_base = 'https://api.netless.link/v5'
        room_resp = requests.post(
            f"{agora_whiteboard_api_base}/rooms",
            headers={
                "token": settings.AGORA_SDK_TOKEN,
                "Content-Type": "application/json",
                "region": settings.AGORA_WHITEBOARD_REGION
            },
            json={
                "isRecord": False,
            }
        )

        # {
        #     "uuid": "4a50xxxxxx796b", // The room UUID
        #     "teamUUID": "RMmLxxxxxx15aw",
        #     "appUUID": "i54xxxxxx1AQ",
        #     "isBan": false,
        #     "createdAt": "2021-01-18T06:56:29.432Z",
        #     "limit": 0
        # }
        room_data = room_resp.json()

        token_resp = requests.post(
            f"{agora_whiteboard_api_base}/tokens/rooms/{room_data['uuid']}",
            headers={
                "token": settings.AGORA_SDK_TOKEN,
                "Content-Type": "application/json",
                "region": settings.AGORA_WHITEBOARD_REGION
            },
            json={"lifespan": 3600000, "role": "admin"}
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
                'uuid': room_data['uuid'],
                'roomToken': room_token,
            }
        })
