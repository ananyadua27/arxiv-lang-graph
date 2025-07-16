from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import asyncio

from app.graph import graph_executor
from app.memory import save_state, get_state

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    session_id: str
    topic: str

@app.get("/")
async def root():
    return {"message": "Hello! The app is running."}

@app.post("/analyze")
async def analyze(query: Query):
    try:
        prev_state = await get_state(query.session_id)
        state = prev_state or {}
        state["topic"] = query.topic
        print(f"[analyze] Processing topic: {state['topic']}")

        result = await asyncio.to_thread(graph_executor.invoke, state)

        print("Workflow result:", result, flush=True)

        await save_state(query.session_id, result)
        return JSONResponse(content=jsonable_encoder(result))
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Error: {e}", flush=True)
        return JSONResponse(status_code=500, content={"error": str(e)})
