import asyncio
import json
import os

import websockets
from dotenv import load_dotenv
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles

load_dotenv()

DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")

if not DEEPGRAM_API_KEY:
    raise ValueError("DEEPGRAM_API_KEY is not set")


app = FastAPI()

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static",
)


DEEPGRAM_URL = "wss://agent.deepgram.com/v1/agent/converse"


async def connect_to_deepgram():

    deepgram_ws = await websockets.connect(
        DEEPGRAM_URL,
        additional_headers={"Authorization": f"Token {DEEPGRAM_API_KEY}"},
    )

    return deepgram_ws
