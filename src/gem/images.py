import requests

from src.config import PHOTO_SERVICE_API_KEY, PHOTO_SERVICE_URL, ALBUM_ID


def load_image_and_get_url(filename: str) -> str:
    response = requests.post(PHOTO_SERVICE_URL, headers={
        "Authorization": f"Bearer {PHOTO_SERVICE_API_KEY}",
    }, files={
        "image": open(filename, "rb"),
        "album": ALBUM_ID
    })
    return response.json()["data"]["link"]
