import os
import json
from confluent_kafka import Producer
import socket

from chatgpt.models import MlJob

KAFKA_HOST = os.environ.get('KAFKA_HOST')
KAFKA_PORT = os.environ.get('KAFKA_PORT')


class ProducerMl:
    def __init__(self) -> None:
        conf = {'bootstrap.servers': f'{KAFKA_HOST}:{KAFKA_PORT}', 'client.id': socket.gethostname()}
        self.producer = Producer(conf)


class ProducerMlPromptCreated(ProducerMl):

    def publish(self, job: MlJob):
        self.producer.produce(
            'mlmodel.prompt_created',
            key=f'key.user_{job.user.id}.prompt_created',
            value=json.dumps(job, cls = MlJob.MlJobEncoder),
        )
