import json
import sys
import time

from dotenv import load_dotenv
from confluent_kafka import Producer, Consumer, KafkaError, KafkaException
import socket
import os

load_dotenv()


class RouterManager:
    start_execution = None
    service_name = ''
    router = {}
    model_object = {
        "model_name": "",
        "topic_name": "",
        "status": "waiting",
        "result": {},
        "execution_time": ""
    }

    def __init__(self, service_name: str, message: dict):
        self.service_name = service_name
        self.router = message
        # Time when the execution started
        self.start_execution = time.time()

    def get_question(self):
        return self.router['prompt']['messages'][0]['content']

    def update_model(self, done: bool = True, result=None):
        if result is None:
            result = {}
        status = "done" if done else "waiting"
        # Get by name
        index = next((index for (index, d) in enumerate(self.router["router"]) if d["model_name"] == self.service_name),
                     None)

        model = self.router["router"][index]
        model["status"] = status
        model["result"] = result
        model["execution_time"] = time.time() - self.start_execution

    def add_model(self, model_name: str, topic_name: str):
        model = self.model_object
        model["model_name"] = model_name
        model["topic_name"] = topic_name
        self.router["router"].append(model)
