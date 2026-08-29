import logging
import os
import uuid
from logging.handlers import RotatingFileHandler

import requests
from flask import current_app
from PIL import Image
from werkzeug.utils import secure_filename

logger = logging.getLogger("eventhub")


def setup_logging(app):

    log_path = app.config["LOG_FILE"]
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    handler = RotatingFileHandler(log_path, maxBytes=512_000, backupCount=3, encoding="utf-8")
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    handler.setFormatter(formatter)

    logger.setLevel(logging.INFO)
    if not any(isinstance(h, RotatingFileHandler) for h in logger.handlers):
        logger.addHandler(handler)

    return logger


def save_profile_picture(file_storage, upload_folder):
    ext = os.path.splitext(secure_filename(file_storage.filename))[1].lower()
    filename = f"{uuid.uuid4().hex}{ext}"
    os.makedirs(upload_folder, exist_ok=True)
    filepath = os.path.join(upload_folder, filename)

    image = Image.open(file_storage)
    image.thumbnail((400, 400))
    if image.mode in ("RGBA", "P") and ext in (".jpg", ".jpeg"):
        image = image.convert("RGB")
    image.save(filepath)

    return filename


def get_weather(location):
    api_key = current_app.config.get("OPENWEATHER_API_KEY")
    if not api_key:
        logger.error("API request error: OPENWEATHER_API_KEY is not configured")
        return None

    try:
        response = requests.get(
            current_app.config["OPENWEATHER_URL"],
            params={"q": location, "appid": api_key, "units": "metric", "lang": "en"},
            timeout=5,
        )
        response.raise_for_status()
        data = response.json()
        weather = data.get("weather", [{}])[0]
        return {
            "temp": round(data.get("main", {}).get("temp", 0)),
            "feels_like": round(data.get("main", {}).get("feels_like", 0)),
            "description": weather.get("description", "").capitalize(),
            "icon": weather.get("icon"),
            "city": data.get("name", location),
        }
    except requests.exceptions.RequestException as exc:
        logger.error("API request error: weather lookup failed for %r: %s", location, exc)
        return None
    except (KeyError, ValueError, IndexError) as exc:
        logger.error("API request error: unexpected weather payload for %r: %s", location, exc)
        return None
