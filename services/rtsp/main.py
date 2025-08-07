#!/usr/bin/env python3
import gi
import os

gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')
from gi.repository import Gst, GstRtspServer, GLib

Gst.init(None)

server = GstRtspServer.RTSPServer()
factory = GstRtspServer.RTSPMediaFactory()

# Try to find available video devices
video_devices = []
for i in range(16):
    device_path = f"/dev/video{i}"
    if os.path.exists(device_path):
        video_devices.append(device_path)

if video_devices:
    # Use the first available video device
    video_device = video_devices[0]
    print(f"Using video device: {video_device}")
    
    # Use v4l2src for better compatibility with Docker containers
    pipeline = f"( v4l2src device={video_device} ! video/x-raw,width=1920,height=1080,framerate=30/1 ! videoconvert ! x264enc tune=zerolatency bitrate=4000 speed-preset=superfast ! rtph264pay name=pay0 pt=96 )"
else:
    print("No video devices found, using fallback pipeline")
    # Fallback pipeline without specific device
    pipeline = "( videotestsrc ! video/x-raw,width=1920,height=1080,framerate=30/1 ! videoconvert ! x264enc tune=zerolatency bitrate=4000 speed-preset=superfast ! rtph264pay name=pay0 pt=96 )"

factory.set_launch(pipeline)
factory.set_shared(True)
server.get_mount_points().add_factory("/test", factory)
server.attach(None)

print("RTSP server started at rtsp://<Jetson_IP>:8554/test")
loop = GLib.MainLoop()
loop.run()
