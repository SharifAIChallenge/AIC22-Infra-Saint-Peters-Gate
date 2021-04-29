from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
# from services.kafka_cli import KafkaClient

from .serializers import GameRegisterSerializer
import uuid
from apps import permissions



import enum
import os
from json import dumps

from kafka import KafkaProducer
from gateway.settings import KAFKA_ENDPOINT
from gateway.settings import (
    KAFKA_TOPIC_MATCH_0,
    KAFKA_TOPIC_MATCH_1,
    KAFKA_TOPIC_MATCH_0_PARTITIONS,
    KAFKA_TOPIC_MATCH_1_PARTITIONS
)

kafka_producer = KafkaProducer(
    bootstrap_servers=KAFKA_ENDPOINT,
    value_serializer=lambda x: dumps(x).encode('utf-8')
)


class Topic:
    def __init__(self, topic_name, total_partitions):
        self.total_partitions = total_partitions
        self.topic_name = topic_name
        self.cur = 0

    def get_partition(self):
        self.cur = (self.cur + 1) % self.total_partitions
        return self.cur


arenas = [
    Topic(KAFKA_TOPIC_MATCH_0, KAFKA_TOPIC_MATCH_0_PARTITIONS),
    Topic(KAFKA_TOPIC_MATCH_1, KAFKA_TOPIC_MATCH_1_PARTITIONS),
]


class Topics(enum.Enum):
    STORE_CODE = os.getenv('KAFKA_TOPIC_STORE_CODE')
    PLAY_GAME = os.getenv('KAFKA_TOPIC_MATCH')


class KafkaClient:
    @staticmethod
    def register_match(priority, message) -> bool:
        try:
            arena = arenas[priority]
            print(arena)
            # kafka_producer.send(topic=arena.topic_name, value=message)
            # logging.warning(f"{arena}")
            kafka_producer.send(topic=arena.topic_name, value=message,
                                partition=arena.get_partition())
            kafka_producer.flush()
            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def send_code(topic, message) -> bool:
        try:
            kafka_producer.send(topic=topic, value=message)
            kafka_producer.flush()
            return True
        except Exception as e:
            print(e)
            return False


class PlayGameAPIView(GenericAPIView):
    permission_classes = [permissions.IsBackend]
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
