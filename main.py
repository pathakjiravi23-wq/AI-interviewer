import asyncio

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles

from deepgram import connect_to_deepgram

app = FastAPI()

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static",
)


async def browser_to_deepgram(
    browser_ws: WebSocket,
    deepgram_ws,
):

    while True:

        data = await browser_ws.receive_bytes()

        await deepgram_ws.send(data)


async def deepgram_to_browser(
    deepgram_ws,
    browser_ws: WebSocket,
):

    async for message in deepgram_ws:

        if isinstance(message, bytes):

            # Audio from Deepgram
            await browser_ws.send_bytes(message)

        else:

            # Events/transcripts from Deepgram
            await browser_ws.send_text(message)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):

    await websocket.accept()

    print("Browser connected")

    deepgram_ws = await connect_to_deepgram()

    print("Connected to Deepgram Agent")

    try:

        await asyncio.gather(
            browser_to_deepgram(websocket, deepgram_ws),
            deepgram_to_browser(deepgram_ws, websocket),
        )

    except WebSocketDisconnect:

        print("Browser disconnected")

    finally:

        await deepgram_ws.close()
        print("Deepgram connection closed")
