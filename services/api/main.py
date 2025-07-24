from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
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
