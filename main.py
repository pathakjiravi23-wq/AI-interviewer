import asyncio
import json

from fastapi import FastAPI

from deepgram import connect_to_deepgram


app = FastAPI()


@app.get("/")
async def root():
    return {"status": "ok"}


async def receive_from_deepgram(deepgram_ws):

    async for message in deepgram_ws:

        if isinstance(message, bytes):

            print("Received audio from Deepgram")

        else:

            data = json.loads(message)

            print("Received from Deepgram:")
            print(data)


@app.websocket("/deepgram")
async def deepgram_connection():

    deepgram_ws = await connect_to_deepgram()

    print("Connected to Deepgram Agent")

    try:

        await receive_from_deepgram(deepgram_ws)

    finally:

        await deepgram_ws.close()
        print("Deepgram connection closed")