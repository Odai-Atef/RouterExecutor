from kafka import KafkaConsumer
from kafka import KafkaProducer
from decouple import AutoConfig
import os 


dir_path = os.path.abspath(os.curdir)
extra_tags={}
config = AutoConfig(search_path=dir_path)
consumer = None
producer = None
obj={"queue":{"topic_name":config("queue_topic_name"),"group_id":config("queue_group_id"),"servers":config("queue_servers"),"result_topic":config("queue_result_topic")}}

def create_consumer():
    if consumer == None:
        consumer = KafkaConsumer(obj['queue']['topic_name'], group_id=obj['queue']['group_id'])

def create_producer():
    if producer == None:
        producer = KafkaProducer(bootstrap_servers=obj['queue']['servers'])

def prepare_msg(result,router_json):
    topic = obj['queue']['result_topic']
    for index,router in enumerate(router_json):
        if router['queue']['topic_name'] == obj['queue']['topic_name']:
            router_json[index]['status']="Done"
            router_json[index]['result']=result
            if router_json[index+1] != None:
                topic=router_json[index+1]['queue']['topic_name']
                break

    return {"msg":router_json,"topic":topic}




def pull_message():
    create_consumer()
    return next(consumer)    

def push_message(msg,router_json):
    info=create_producer(msg,router_json)
    producer.send(info['topic'],info['msg'])
    return True

