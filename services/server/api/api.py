from fastapi import FastAPI, APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
import time
import os

app = FastAPI()
mask_router = APIRouter(prefix="/mask")

image_version = 0

@app.get("/ping")
async def ping():
    return JSONResponse({"message": "pong"})

@mask_router.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    global image_version
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="The uploaded file is not an image.")
    with open("mask.png", "wb") as f:
        f.write(await file.read())
    current_time = time.time()
    os.utime("mask.png", (current_time, current_time))
    image_version += 1
    return {"message": "Image uploaded successfully.", "version": image_version}

@mask_router.get("/")
async def image():
    if not os.path.exists("mask.png"):
        raise HTTPException(status_code=404, detail="Image not found")
    
    file_mtime = os.path.getmtime("mask.png")
    
    response = StreamingResponse(open("mask.png", "rb"), media_type="image/png")
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    response.headers["Last-Modified"] = time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime(file_mtime))
    response.headers["ETag"] = f'"{int(file_mtime)}"'
    return response

@mask_router.get("/stream")
async def stream_image():
    """Stream image with version parameter for cache busting"""
    global image_version
    if not os.path.exists("mask.png"):
        raise HTTPException(status_code=404, detail="Image not found")
    
    response = StreamingResponse(open("mask.png", "rb"), media_type="image/png")
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

@mask_router.get("/version")
async def get_version():
    """Get current image version for cache busting"""
    global image_version
    return {"version": image_version}

@mask_router.get("/viewer")
async def image_viewer():
    """Serve the HTML viewer file"""
    if not os.path.exists("static/viewer.html"):
        raise HTTPException(status_code=404, detail="Viewer file not found")
    
    with open("static/viewer.html", "r") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

app.include_router(mask_router)