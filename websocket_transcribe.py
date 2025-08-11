from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import AsyncIterator
import asyncio
import json

from starlette.websockets import WebSocketState


app = FastAPI()

async def fake_transcriber(audio_chunks: AsyncIterator[bytes]):
    # Replace with your real STT stream (Whisper, SambaNova, etc.)
    i = 0 
    async for _ in audio_chunks:
        await asyncio.sleep(0.2)
        i+=1
        yield{"type": "partial", "text": f"Transcribing chunk {i}"}
    yield {"type": "final", "text": f"final Transcribing chunk was {i}"}    


@app.websocket("/stt")
async def stt(ws: WebSocket):
    await ws.accept()
    audio_q: asyncio.Queue[bytes] = asyncio.Queue()
    stop = asyncio.Event()

    async def recv_audio():
        try:
            while not stop.is_set():
                msg = await ws.receive_bytes()
                if not msg:
                    stop.set()
                    break
                await audio_q.put(msg)
        except WebSocketDisconnect:
            print("client disconnected")
            stop.set()
        finally: 
            await audio_q.put(b"")

    
    async def iter_audio():
        while True:
            chunk = await audio_q.get()
            if chunk == b"":
                break
            yield chunk


    recv_task = asyncio.create_task(recv_audio())
    try:
        async for hyp in fake_transcriber(iter_audio()):
            if ws.application_state != WebSocketState.CONNECTED:
                break
            try:
                await ws.send_text(json.dumps(hyp))
            except WebSocketDisconnect:
                break
            except RuntimeError:
                break
    finally:
        stop.set()
        
        await asyncio.gather(recv_task, return_exceptions=True)
        # Gracefully close the WebSocket to avoid reserved status close codes
        if ws.application_state == WebSocketState.CONNECTED:
            try:
                await ws.close(code=1000)
            except Exception:
                pass