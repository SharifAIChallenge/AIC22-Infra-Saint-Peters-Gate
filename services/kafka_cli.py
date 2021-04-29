import enum
import os
from json import dumps

from kafka import KafkaProducer
from gateway.settings import KAFKA_ENDPOINT, arenas
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


class Topics(enum.Enum):
    STORE_CODE = os.getenv('KAFKA_TOPIC_STORE_CODE')
    PLAY_GAME = os.getenv('KAFKA_TOPIC_MATCH')


class KafkaClient:
    @staticmethod
    def register_match(priority, message) -> bool:
        try:
            arena = settings.arenas[priority]
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
