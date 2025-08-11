from fastapi import FastAPI
from fastapi.responses import StreamingResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

import asyncio
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],
    allow_methods =["GET"],
    allow_headers=["*"]
)



async def event_stream():
    for i in range (10):
        await asyncio.sleep(1)
        yield f"data: {json.dumps({'tick': i})} \n\n"
    yield "event: end\r\ndata: {} \n\n"


@app.get("/stream")
async def stream():
    headers = {
        # "Cache-Control": "no-cache",
        # "Connection": "keep-alive",
        # "X-Accel-Buffering": "no",
    }
    return StreamingResponse(event_stream(), media_type="text/event-stream", headers=headers)



#this is fine to send html or js but doesn't show console messages
# just for referenece, not actually using it 
@app.get("/client")
def client():
    html =  """
    <!DOCTYPE html>
    <html><body>
      <h1>SSE demo (same origin)</h1>
      <script>
        console.log("BOOT");
        const es = new EventSource("/stream");
        es.onmessage = e => console.log("Message:", JSON.parse(e.data));
        es.addEventListener("end", () => { console.log("Stream ended"); es.close(); });
      </script>
    </body></html>
    """
    return HTMLResponse(html)