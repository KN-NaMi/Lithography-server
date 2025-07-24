from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
import cv2
import os
import time

app = FastAPI()

IMAGE_PATH = "current_image.jpg"


def image_stream():
    while True:
        if os.path.exists(IMAGE_PATH):
            with open(IMAGE_PATH, "rb") as f:
                frame = f.read()
            yield (b"--frame\r\n"
                   b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")
        time.sleep(0.05)


@app.get("/stream")
def stream():
    return StreamingResponse(image_stream(), media_type="multipart/x-mixed-replace; boundary=frame")


@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Plik nie jest obrazem")
    with open(IMAGE_PATH, "wb") as f:
        f.write(await file.read())
    return {"message": "Obraz został przesłany pomyślnie"}


def gstreamer_pipeline(
    sensor_id=0,
    capture_width=1920,
    capture_height=1080,
    display_width=1920,
    display_height=1080,
    framerate=30,
    flip_method=0
):
    return (
        f"nvarguscamerasrc sensor-id={sensor_id} ! "
        f"video/x-raw(memory:NVMM), width={capture_width}, height={capture_height}, "
        f"format=NV12, framerate={framerate}/1 ! "
        f"nvvidconv flip-method={flip_method} ! "
        f"video/x-raw, width={display_width}, height={display_height}, format=BGRx ! "
        f"videoconvert ! video/x-raw, format=BGR ! appsink"
    )


def csi_camera_stream():
    cap = cv2.VideoCapture(gstreamer_pipeline(), cv2.CAP_GSTREAMER)
    if not cap.isOpened():
        raise RuntimeError("Nie można otworzyć kamery CSI!")

    while True:
        ret, frame = cap.read()
        if not ret:
            continue
        _, jpeg = cv2.imencode('.jpg', frame)
        frame_bytes = jpeg.tobytes()
        yield (b"--frame\r\n"
               b"Content-Type: image/jpeg\r\n\r\n" + frame_bytes + b"\r\n")

    cap.release()


@app.get("/csi")
def csi_stream():
    return StreamingResponse(csi_camera_stream(), media_type="multipart/x-mixed-replace; boundary=frame")
