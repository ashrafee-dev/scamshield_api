import asyncio

from websockets.asyncio.client import connect

async def test1(audio):
    url = "ws://localhost:8000/ws"
    async with connect(url) as websockets:
        await websockets.send(audio)


if __name__ == "__main__":
    with open("test_audio.m4a") as audio:
        asyncio.run(test1(audio))
