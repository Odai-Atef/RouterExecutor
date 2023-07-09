import json

from RouterExecutor.RouterExecutor import RouterExecutor
from RouterExecutor.RouterManager import RouterManager

service_name = "prompt_router"  # Change this to the name of your service
service_topic = "prompt_router"  # Change this to the name of your service


def call_back(message):
    manager = RouterManager(service_name=service_name, message=message)
    # Question
    question = manager.get_question()
    print('New Message: ', question)

    # Logic
    is_retrival = True

    # Update Current Model
    manager.update_model(done=True, result={'is_retrival': True})

    # Set Models
    if is_retrival:
        manager.add_model('retriever', 'retriever')

    # Send to next topic
    router.next_topic(manager.router)


router = RouterExecutor(service_topic=service_topic)
router.consume(cb=call_back)
