# bluepill.py

import threading
import time
from datetime import datetime

import pyautogui
from pynput import keyboard, mouse


PAUSE_SECONDS = 10
MOVEMENT_INTERVAL_SECONDS = 20

MESSAGES = {
    "es": {
        "running": "BluePill 2.0 está ejecutándose.",
        "activity_pause": "La actividad humana pausa el movimiento automático durante 10 segundos.",
        "exit_hint": "Presione Esc + E en cualquier momento para detener BluePill.",
        "human_activity": "Movimiento humano detectado, presione Esc + e para detener el movimiento automático.",
        "movement_start": "Movimiento iniciado  a las {}",
        "movement_done": "Movimiento realizado a las {}",
        "stopped": "BluePill detenido.",
    },
    "en": {
        "running": "BluePill 2.0 is running.",
        "activity_pause": "Human activity pauses automatic movement for 10 seconds.",
        "exit_hint": "Press Esc + E at any time to stop BluePill.",
        "human_activity": "Human movement detected, press Esc + E to stop automatic movement.",
        "movement_start": "Movement started at {}",
        "movement_done": "Movement made at {}",
        "stopped": "BluePill stopped.",
    },
}


def run(interval_seconds: int = MOVEMENT_INTERVAL_SECONDS, language: str = "es"):
    pyautogui.FAILSAFE = False
    messages = MESSAGES.get(language, MESSAGES["es"])

    stop_event = threading.Event()
    pause_until = 0.0
    state_lock = threading.Lock()

    # Coordinates expected from BluePill itself. Mouse events that do not match
    # this position are considered real user activity.
    expected_mouse_position = None
    synthetic_keyboard = False
    esc_pressed = False

    def pause_for_user_activity():
        nonlocal pause_until
        now = time.monotonic()
        should_notify = False

        with state_lock:
            # Print the notice once when a new human-activity pause begins.
            if now >= pause_until:
                should_notify = True
            pause_until = max(pause_until, now + PAUSE_SECONDS)

        if should_notify:
            print("\n{}\n".format(messages["human_activity"]), flush=True)

    def on_mouse_activity(x, y, *args):
        nonlocal expected_mouse_position
        with state_lock:
            expected = expected_mouse_position

        # Ignore the exact cursor position BluePill just requested.
        if expected is not None and (int(x), int(y)) == expected:
            return

        pause_for_user_activity()

    def on_key_press(key):
        nonlocal esc_pressed

        with state_lock:
            is_synthetic = synthetic_keyboard

        if is_synthetic:
            return

        if key == keyboard.Key.esc:
            esc_pressed = True
            pause_for_user_activity()
            return

        try:
            if esc_pressed and key.char and key.char.lower() == "e":
                width, height = pyautogui.size()
                pyautogui.moveTo(width // 2, height // 2)
                stop_event.set()
                return False
        except AttributeError:
            pass

        pause_for_user_activity()

    def on_key_release(key):
        nonlocal esc_pressed
        if key == keyboard.Key.esc:
            esc_pressed = False

    mouse_listener = mouse.Listener(
        on_move=on_mouse_activity,
        on_click=on_mouse_activity,
        on_scroll=on_mouse_activity,
    )
    keyboard_listener = keyboard.Listener(
        on_press=on_key_press,
        on_release=on_key_release,
    )

    mouse_listener.start()
    keyboard_listener.start()

    print(messages["running"])
    print(messages["activity_pause"])
    print(messages["exit_hint"] + "\n")

    def user_is_active():
        with state_lock:
            return time.monotonic() < pause_until

    def wait_interruptibly(seconds):
        end = time.monotonic() + seconds
        while not stop_event.is_set() and time.monotonic() < end:
            time.sleep(min(0.05, end - time.monotonic()))

    try:
        while not stop_event.is_set():
            if user_is_active():
                wait_interruptibly(0.05)
                continue

            print(messages["movement_start"].format(datetime.now().time()))

            movement_interrupted = False
            for i in range(0, 50):
                if stop_event.is_set() or user_is_active():
                    movement_interrupted = True
                    break

                target = (0, i * 4)
                with state_lock:
                    expected_mouse_position = target
                pyautogui.moveTo(*target)

            if movement_interrupted:
                with state_lock:
                    expected_mouse_position = None
                continue

            with state_lock:
                expected_mouse_position = (1, 1)
            pyautogui.moveTo(1, 1)

            if stop_event.is_set() or user_is_active():
                with state_lock:
                    expected_mouse_position = None
                continue

            with state_lock:
                expected_mouse_position = None
                synthetic_keyboard = True
            try:
                pyautogui.press("shift")
            finally:
                with state_lock:
                    synthetic_keyboard = False

            print(messages["movement_done"].format(datetime.now().time()))
            print("---------------------------------")

            wait_interruptibly(interval_seconds)

    except KeyboardInterrupt:
        stop_event.set()
    finally:
        mouse_listener.stop()
        keyboard_listener.stop()
        # Matrix interface text is intentionally never translated.
        print("\nYou close your eyes… the Matrix fades away.")
        print(messages["stopped"] + "\n")
