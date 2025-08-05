import cv2
import asyncio
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, JSONResponse
from aiortc import RTCPeerConnection, RTCSessionDescription, VideoStreamTrack
from aiortc.contrib.media import MediaBlackhole
import av

app = FastAPI()
pcs = set()

RTSP_URL = "rtsp://127.0.0.1:8554/test"

class RTSPVideoStreamTrack(VideoStreamTrack):
    def __init__(self):
        super().__init__()
        self.cap = cv2.VideoCapture(RTSP_URL)

    async def recv(self):
        pts, time_base = await self.next_timestamp()

        ret, frame = self.cap.read()
        if not ret:
            await asyncio.sleep(0.1)
            return await self.recv()

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = av.VideoFrame.from_ndarray(frame, format="rgb24")
        frame.pts = pts
        frame.time_base = time_base
        return frame
    
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

    video_track = RTSPVideoStreamTrack()
    pc.addTrack(video_track)

    offer = RTCSessionDescription(sdp, type)
    await pc.setRemoteDescription(offer)
    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)

    return JSONResponse({
        "sdp": pc.localDescription.sdp,
        "type": pc.localDescription.type
    })
