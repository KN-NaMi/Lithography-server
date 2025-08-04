from utils.nami_protocol import NaMiDevice

def run():
    device = NaMiDevice()
    device.start_udp_discovery()

if __name__ == "__main__":
    run()