import redis.asyncio as aioredis
import json

async def publish_presence(redis_conn_a,room_id: int, online_key: str):
    count = await redis_conn_a.zcard(online_key)
    members = await redis_conn_a.zrange(online_key,0,-1)
    payload = {
        "type": "presence",
        "count": count,
        "members": [m.decode() for m in members],  # aioredis returns bytes
    }
    await redis_conn_a.publish(f"room_{room_id}", json.dumps(payload))

# async def get_presence(redis_conn_e,room_id,online_key):
#     count = await redis_conn_e.scard(online_key)
#     members = await redis_conn_e.smembers(online_key)
#     payload = {
#         "type":"presence",
#         "count":count,
#         "members" :[m.decode() for m in members]
#     }
#     await redis_conn_e.publish(f"room_{room_id}",json.dumps(payload))