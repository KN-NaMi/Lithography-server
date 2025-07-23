import os

if not os.environ.get("DISPLAY"):
    print("Brak DISPLAY - wymuszam tryb headless")
    os.environ["SDL_VIDEODRIVER"] = "dummy"

os.environ["SDL_AUDIODRIVER"] = "dummy"


import pygame
import requests
import io
from PIL import Image
import time

API_IMAGE_URL = "http://api:8000/images/test.png"

def fetch_image(url):
    try:
        resp = requests.get(url)
        if resp.status_code == 200:
            return Image.open(io.BytesIO(resp.content))
    except Exception as e:
        print(f"Error fetching image: {e}")
    return None

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Image Viewer")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        img = fetch_image(API_IMAGE_URL)
        if img:
            img = img.resize((800, 600))
            mode = img.mode
            size = img.size
            data = img.tobytes()
            surface = pygame.image.fromstring(data, size, mode)
            screen.blit(surface, (0, 0))
            pygame.display.flip()

        time.sleep(2)

if __name__ == "__main__":
    main()
