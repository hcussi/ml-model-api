"""
https://docs.confluent.io/kafka-clients/python/current/overview.html#id1
"""
import json
import sys
import threading
import os
from django.utils import timezone
from confluent_kafka import Consumer, KafkaError, KafkaException, Message

from chatgpt.models import MlJob, MlModel, MlJobStatus
from chatgpt.ml_model import super_chat_gpt_like_model

KAFKA_HOST = os.environ.get('KAFKA_HOST')
KAFKA_PORT = os.environ.get('KAFKA_PORT')

# We want to run thread in an infinite loop
running: bool = True


class MlListener(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        # Create consumer
        self.consumer = Consumer({
            'bootstrap.servers': f'{KAFKA_HOST}:{KAFKA_PORT}',
            'auto.offset.reset': 'earliest',
            'group.id': 'mlprompt_created_group'
        })


class MlPromptCreatedListener(MlListener):
    def run(self) -> None:
        try:
            self.consumer.subscribe(['mlmodel.prompt_created'])
            while running:
                # Poll for message
                msg: Message | None = self.consumer.poll(timeout = 1.0)

                if msg is None:
                    continue

                # Handle Error
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        # End of partition event
                        sys.stderr.write(
                            '%% %s [%d] reached end at offset %d\n' %
                            (msg.topic(), msg.partition(), msg.offset())
                        )
                elif msg.error():
                    raise KafkaException(msg.error())
                else:
                    #  Committing on every message would produce a lot of overhead in practice
                    self.consumer.commit(asynchronous = False)
                    self.process(msg)

        finally:
            # Close down consumer to commit final offsets.
            self.consumer.close()

    def process(self, msg: Message) -> None:
        json_job = json.loads(msg.value().decode('utf-8'))

        job = MlJob.objects.get(pk = json_job['job_id'])

        mlmodel = MlModel.objects.create(
            user_id = job.user_id,
            prompt = job.prompt,
            response = super_chat_gpt_like_model(job.prompt),
            duration = (timezone.now() - job.start_time),
        )

        job.status = MlJobStatus.DONE
        job.mlmodel = mlmodel

        job.save(update_fields = ['status', 'mlmodel'])

