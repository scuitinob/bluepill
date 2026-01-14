# main.py

from banner import BLUEPILL_BANNER
import bluepill


def show_banner():
    print(BLUEPILL_BANNER)

if __name__ == "__main__":
    show_banner()
    bluepill.run()
