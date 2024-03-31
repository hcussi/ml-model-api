import os
import json
from confluent_kafka import Producer
import socket

from chatgpt.models import MlJob

KAFKA_BOOTSTRAP_SERVERS = os.environ.get('KAFKA_BOOTSTRAP_SERVERS')


class ProducerMl:
    def __init__(self) -> None:
        conf = {'bootstrap.servers': f'{KAFKA_BOOTSTRAP_SERVERS}', 'client.id': socket.gethostname()}
        self.producer = Producer(conf)


class ProducerMlPromptCreated(ProducerMl):

    def publish(self, job: MlJob):
        self.producer.produce(
            'mlmodel.prompt_created',
            key=f'key.user_{job.user.id}.prompt_created',
            value=json.dumps(job, cls = MlJob.MlJobEncoder),
        )
