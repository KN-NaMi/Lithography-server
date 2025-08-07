#!/usr/bin/env python3
import gi
import os

gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')
from gi.repository import Gst, GstRtspServer, GLib

Gst.init(None)

server = GstRtspServer.RTSPServer()
factory = GstRtspServer.RTSPMediaFactory()

print("Starting RTSP server...")

# Use a simple test pattern first to verify the server works
pipeline = "( videotestsrc ! video/x-raw,width=640,height=480,framerate=30/1 ! videoconvert ! x264enc tune=zerolatency bitrate=1000 speed-preset=superfast ! rtph264pay name=pay0 pt=96 )"

print(f"Using pipeline: {pipeline}")

factory.set_launch(pipeline)
factory.set_shared(True)
server.get_mount_points().add_factory("/test", factory)
server.attach(None)

print("RTSP server started at rtsp://<Jetson_IP>:8554/test")
print("Stream URL: rtsp://<Jetson_IP>:8554/test")
loop = GLib.MainLoop()
loop.run()
