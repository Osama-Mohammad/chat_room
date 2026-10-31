import numpy as np
from pathlib import Path
from rq import get_current_job
from sse_starlette.sse import EventSourceResponse,ServerSentEvent
from redis import Redis
import os
import json

redis_conne = Redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379"))
def process_msg(room_id:int,msg:str,user_id:int,user_name:str):
    data= {
        "user_id" : user_id,
        "msg" : msg,
        "user_name":user_name,
        "room_id":room_id
    }
    redis_conne.publish(channel=f"room_{room_id}",message=json.dumps(data))

    return  "Message Sent"