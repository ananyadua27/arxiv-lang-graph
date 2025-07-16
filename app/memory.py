# app/memory.py
import redis.asyncio as redis
import os
import json
from dotenv import load_dotenv
from app.config import REDIS_URL

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
redis_client = redis.from_url(REDIS_URL, encoding="utf-8", decode_responses=True)

async def save_state(session_id: str, state: dict):
    await redis_client.set(session_id, json.dumps(state))

async def get_state(session_id: str) -> dict:
    data = await redis_client.get(session_id)
    if data:
        return json.loads(data)
    return {}

async def clear_state(session_id: str):
    await redis_client.delete(session_id)

