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
    retrievals = [
        "retriever",
        "retriever",
        "retriever",
    ]

    #  Update Data
    manager.update_model(done=True, result=retrievals)

    # Send to next topic
    router.next_topic(manager.router)


router = RouterExecutor(service_name)
router.consume(cb=call_back)
