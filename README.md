# RouterExecutor

This library is for manging routing between services.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install RouterExecutor
```

## Usage (Prompt Routing Service)

To add model for e.g. Retriever use this function manager.add_model() and pass the name of the service and topic.

```python

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

```

## Any Service e.g: Retriever

```python

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


```


# JSON Structure
This library will handle the json.

### First JSON
```json
{
    "prompt": {
        "messages": [
            {
                "role": "user",
                "content": "Question 1"
            }
        ],
        "id": 183039,
        "type": "general",
        "capture_date": "2023-07-09T11:14:13.357353Z",
        "progress": 0,
        "final_destination_topic":"result"
    },
    "router": [
        {
            "model_name": "prompt_router",
            "topic_name": "prompt_router",
            "status": "waiting",
            "result": {},
            "execution_time": 0
        }
    ]
}
```

### Final JSON

```json
{
  "prompt": {
    "messages": [
      {
        "role": "user",
        "content": "Question 1"
      }
    ],
    "id": 183039,
    "type": "general",
    "capture_date": "2023-07-09T11:14:13.357353Z",
    "progress": 0,
    "final_destination_topic": "result"
  },
  "router": [
    {
      "model_name": "prompt_router",
      "topic_name": "prompt_router",
      "status": "done",
      "result": {
        "is_retrival": true
      },
      "execution_time": 0.00006413459777832031
    },
    {
      "model_name": "retriever",
      "topic_name": "retriever",
      "status": "done",
      "result": [
        "retriever",
        "retriever",
        "retriever"
      ],
      "execution_time": 0.00003695487976074219
    }
  ]
}
```
