import time
from utils.nami_protocol import NaMiDevice


def run():
    device = NaMiDevice()
    device.start()
    print("NaMiDevice started and listening for UDP discovery requests...")
    while True:
        time.sleep(1)

if __name__ == "__main__":
    run()