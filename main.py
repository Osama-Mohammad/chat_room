# main.py
import time
import json
import asyncio
from tasks import *
from rq import Queue
from rq.job import Job
from helpers import * 
from redis import Redis
import redis.asyncio as aioredis
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette.sse import EventSourceResponse,ServerSentEvent
from fastapi import FastAPI, UploadFile, File, Form, HTTPException


app =FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["http://127.0.0.1:5500"], allow_methods=["*"],allow_headers=["*"],)

redis_conne = Redis(host="localhost",port=6379)
redis_conn_a = aioredis.Redis(host="localhost",port=6379)

queue = Queue("messages",redis_conne)


@app.get("/room/{room_id}/messages")
async def room(room_id: int,user_name:str):
    async def event_generator():
        pubsub = redis_conn_a.pubsub()
        online_key = f"room:{room_id}:online"
        try:
            await pubsub.subscribe(f"room_{room_id}")
            now = int(time.time())
            # on connect
            await redis_conn_a.zadd(online_key, {
                user_name:now
            })
            await publish_presence(redis_conn_a,room_id, online_key)

            while True:
                message = await pubsub.get_message(ignore_subscribe_messages=True)
                if message is not None:
                    d = json.loads(message["data"])
                    event_type = "presence" if d.get("type") == "presence" else "message"
                    yield ServerSentEvent(
                        event=event_type,
                        data=json.dumps(d)   # data must be a string
                    )
                else:
                    await asyncio.sleep(0.5)
        finally:
            # on disconnect
            await redis_conn_a.zrem(online_key, user_name)
            await publish_presence(redis_conn_a,room_id, online_key)

            
            await pubsub.unsubscribe()
            await pubsub.aclose()


    return EventSourceResponse(event_generator())

@app.post("/room/{room_id}/messages")
async def post_msg(room_id:int,msg:str,user_id:int,user_name:str):
    job = queue.enqueue(process_msg,room_id,msg,user_id,user_name)
    return {"job_id": job.id, "status": "queued"}


@app.get("/room/{room_id}/check_presence")
async def check_presence(room_id:int):
    online_key = f"room:{room_id}:online"
    now = int(time.time())
    timeout = 10
    await redis_conn_a.zremrangebyscore(online_key,0,now-timeout)
    members = await redis_conn_a.zrange(online_key,0,-1)
    payload = {
        "type": "presence",
        "count": len(members),
        "members": [m.decode() for m in members]
    }
    await redis_conn_a.publish(f"room_{room_id}",json.dumps(payload))
    return payload

@app.post("/room/{room_id}/heartbead")
async def heart_beat(room_id:int,user_name:str):
    online_key = f"room:{room_id}:online"
    now = int(time.time())
    await redis_conn_a.zadd(online_key,{user_name:now,}) 
    return {
        "status": "alive"
    }
@app.on_event("shutdown")
async def shut_down():
     await redis_conn_a.aclose()
     redis_conne.close()