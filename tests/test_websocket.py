import asyncio

from websockets.asyncio.client import connect

async def test1(audio):
    url = "wss://localhost:8000/ws"
    async with connect(url) as websockets:
        await websockets.send("text")


if __name__ == "__main__":
    with open("test_audio.mp3") as audio:
        asyncio.run(test1(audio))
