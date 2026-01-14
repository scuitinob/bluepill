#bluepill.py

import pyautogui
import time
from datetime import datetime

def run(interval_seconds: int = 5):
    pyautogui.FAILSAFE = False

    try:
        while(True):
            print("Movement start at {}".format(datetime.now().time()))
            for i in range(0,50):
                pyautogui.moveTo(0,i*4)
            pyautogui.moveTo(1,1)
            pyautogui.press("shift")
            print("Movement made at {}".format(datetime.now().time()))
            print("---------------------------------")
            time.sleep(20) #Tiempo de espera entre movimientos
    except KeyboardInterrupt:
        # salida limpia y elegante
        print("\nYou close your eyes… the Matrix fades away.")
        print("BluePill stopped.\n")