FROM nvcr.io/nvidia/l4t-base:r35.2.1

# Zainstaluj GStreamer i wymagane biblioteki
RUN apt-get update && apt-get install -y \
    python3-gi \
    python3-gst-1.0 \
    libgstrtspserver-1.0-0 \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-bad \
    gstreamer1.0-plugins-ugly \
    gstreamer1.0-libav \
    gstreamer1.0-tools \
    libgstreamer1.0-dev \
    && apt-get clean

# Skopiuj Twój serwer RTSP
COPY main.py /main.py

# Ustaw domyślny start
CMD ["python3", "/main.py"]
