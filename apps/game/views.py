from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from services.kafka_cli import KafkaClient

from .serializers import GameRegisterSerializer
import uuid
from apps import permissions


class PlayGameAPIView(GenericAPIView):
    # permission_classes = [permissions.IsBackend]
    serializer_class = GameRegisterSerializer

    def post(self, request):
        priority = request.GET.get('priority', '-1')
        if priority.isnumeric():
            priority = int(priority)
            if priority != 1:
                priority = 0

        game_id = uuid.uuid4()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        game_information = serializer.data
        game_information['game_id'] = str(game_id)
        KafkaClient.register_match(priority, game_information)
        return Response(data={'game_id': game_id}, status=status.HTTP_200_OK)
