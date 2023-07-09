from RouterExecutor.RouterExecutor import RouterExecutor
from multiprocessing.pool import ThreadPool as Pool
pool_size = 20  # your "parallels"


# Run RouterExecutor

# In[ ]:

router = RouterExecutor('prompt_router')
message = {
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
            "status": "waiting",
            "result": {},
            "execution_time": 0
        }
    ]
}
# define worker function before a Pool is instantiated
def worker(item):
    try:
        message['prompt']['messages'][0]['content'] = f'Question {item}'
        router.produce(message)
        print(
            f'Produced message: {message["prompt"]["messages"][0]["content"]} to topic: {message["router"][0]["topic_name"]}')
    except:
        print('error with item')

pool = Pool(pool_size)



for i in range(250):
    pool.apply_async(worker, (i,))


pool.close()
pool.join()