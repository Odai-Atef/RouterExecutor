import json
import sys
from dotenv import load_dotenv
from confluent_kafka import Producer, Consumer, KafkaError, KafkaException
import socket
import os

load_dotenv()


class RouterExecutor:
    service_topic = None
    conf = {'bootstrap.servers': os.environ.get("KAFKA_BROKERS"),
            'security.protocol': 'SASL_SSL',
            'sasl.mechanisms': 'PLAIN',
            'sasl.username': os.environ.get("KAFKA_USERNAME"),
            'sasl.password': os.environ.get("KAFKA_PASSWORD"),

            'client.id': socket.gethostname()}

    consumer_conf = {
        'group.id': "my-group",
        'auto.offset.reset': 'earliest',
        'enable.auto.commit': True,
    }

    def __init__(self, service_topic: str):
        self.service_topic = service_topic
        self.consumer_conf.update(self.conf)

        self.producer = Producer(self.conf)
        self.consumer = Consumer(self.consumer_conf)
        self.topics = [self.service_topic]

    # Create a kafka confluence consumer
    def produce(self, message: dict):
        if self.producer is None:
            print("Create Producer")
            self.producer = Producer(self.conf)
        self.producer.produce("prompt_router", key="key", value=json.dumps(message))
        self.producer.flush()
        return True

    def next_topic(self, message):
        if self.producer is None:
            self.producer = Producer(self.conf)
        # Loop Throw prompt until find status waiting
        topic = ''
        for model in message["router"]:
            if model["status"] == "waiting":
                topic = model["topic_name"]
                break
        if topic == '':
            topic = message["prompt"]["final_destination_topic"]
        self.producer.produce(topic, key="key", value=json.dumps(message))
        self.producer.flush()

        return True

    # Create a kafka confluence consumer
    def consume(self, cb=None):
        if self.consumer is None:
            self.consumer = Consumer(self.conf)

        try:
            self.consumer.subscribe(self.topics)

            while True:
                msg = self.consumer.poll(timeout=1.0)
                if msg is None: continue

                if msg.error():
                    if msg.error().code() == KafkaError.PARTITION_EOF:
                        # End of partition event
                        sys.stderr.write('%% %s [%d] reached end at offset %d\n' %
                                         (msg.topic(), msg.partition(), msg.offset()))
                else:
                    if cb is not None:
                        val = json.loads(msg.value())
                        cb(val)
        except KeyboardInterrupt:
            sys.stderr.write('%% Aborted by user\n')
        finally:
            # Close down consumer to commit final offsets.
            self.consumer.close()
