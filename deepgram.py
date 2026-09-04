import json
import websockets

from config import DEEPGRAM_API_KEY, DEEPGRAM_URL

AGENT_SETTINGS = {
    "type": "Settings",
    "audio": {
        "input": {
            "encoding": "linear16",
            "sample_rate": 16000,
        },
        "output": {
            "encoding": "linear16",
            "sample_rate": 24000,
        },
    },
    "agent": {
        "language": "en",
        "listen": {
            "provider": {
                "type": "deepgram",
                "model": "nova-3",
            }
        },
        "think": {
            "provider": {
                "type": "open_ai",
                "model": "gpt-4o-mini",
            },
            "prompt": "You are a helpful voice assistant.",
        },
        "speak": {
            "provider": {
                "type": "deepgram",
                "model": "aura-2-thalia-en",
            }
        },
    },
}


async def connect_to_deepgram():

    deepgram_ws = await websockets.connect(
        DEEPGRAM_URL,
        additional_headers={"Authorization": f"Token {DEEPGRAM_API_KEY}"},
    )

    # Configure the Deepgram Agent
    await deepgram_ws.send(json.dumps(AGENT_SETTINGS))

    return deepgram_ws
