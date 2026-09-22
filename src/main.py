# main.py

import json
from pathlib import Path

from banner import BLUEPILL_BANNER
import bluepill


DEFAULT_CONFIG = {
    "language": "es",
    "movement_interval": 20,
}

ALLOWED_INTERVALS = {20, 30, 60, 120, 180, 300}

MESSAGES = {
    "es": {
        "config_warning": "Configuración inválida. Se utilizarán los valores por defecto.",
    },
    "en": {
        "config_warning": "Invalid configuration. Default values will be used.",
    },
}


def show_banner():
    print(BLUEPILL_BANNER)


def load_config():
    config_path = Path(__file__).resolve().parent.parent / "config.json"
    config = DEFAULT_CONFIG.copy()

    try:
        with config_path.open("r", encoding="utf-8") as config_file:
            loaded = json.load(config_file)

        language = str(loaded.get("language", config["language"])).lower()
        interval = int(loaded.get("movement_interval", config["movement_interval"]))

        if language not in MESSAGES or interval not in ALLOWED_INTERVALS:
            raise ValueError("Unsupported configuration value")

        config["language"] = language
        config["movement_interval"] = interval
    except (OSError, ValueError, TypeError, json.JSONDecodeError):
        print(MESSAGES[config["language"]]["config_warning"])

    return config


if __name__ == "__main__":
    show_banner()
    settings = load_config()
    bluepill.run(
        interval_seconds=settings["movement_interval"],
        language=settings["language"],
    )
