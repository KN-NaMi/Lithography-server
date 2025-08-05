import asyncio
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, JSONResponse
from aiortc import RTCPeerConnection, RTCSessionDescription, VideoStreamTrack
import av

app = FastAPI()
pcs = set()

RTSP_URL = "rtsp://127.0.0.1:8554/test"


class RTSPVideoStreamTrack(VideoStreamTrack):
    """
    MediaStreamTrack do przesyłania obrazu z RTSP z niskim opóźnieniem.
    """
    def __init__(self):
        super().__init__()
        self.container = av.open(
            RTSP_URL,
            options={
                "fflags": "nobuffer",
                "flags": "low_delay",
                "rtsp_transport": "tcp",
                "stimeout": "5000000",  # timeout na połączenie w μs
            },
        )
        self.video_stream = self.container.streams.video[0]
        self.decoder = self.container.decode(self.video_stream)

    async def recv(self):
        pts, time_base = await self.next_timestamp()

        try:
            frame = next(self.decoder)
            frame.pts = pts
            frame.time_base = time_base
            return frame
        except StopIteration:
            await asyncio.sleep(0.01)
            return await self.recv()


@app.get("/ping")
async def ping():
    return JSONResponse({"message": "pong"})


@app.get("/")
async def index():
    with open("api/client.html") as f:
        return HTMLResponse(f.read())


@app.post("/offer")
async def offer(sdp: str = Form(...), type: str = Form(...)):
    pc = RTCPeerConnection()
    pcs.add(pc)

    @pc.on("connectionstatechange")
    async def on_connectionstatechange():
        print("Connection state:", pc.connectionState)
        if pc.connectionState == "failed":
            await pc.close()
            pcs.discard(pc)

    # Dodaj ścieżkę wideo
    pc.addTrack(RTSPVideoStreamTrack())

    # Ustaw opis
    offer = RTCSessionDescription(sdp, type)
    await pc.setRemoteDescription(offer)
    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)

    return JSONResponse({
        "sdp": pc.localDescription.sdp,
        "type": pc.localDescription.type
    })
