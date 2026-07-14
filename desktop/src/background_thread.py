import asyncio
import io
import threading
from PIL import Image

from .state import State
from .windows import get_spotify_media, convert_thumbnail_to_bytes


def init_background_thread(state: State):
    state.background_stop_event = threading.Event()
    state.background_thread = threading.Thread(
        target=_background_thread,
        args=[state],
        daemon=True,
    )


def _background_thread(state: State):
    while not state.background_stop_event.is_set():
        _background_thread_task(state)
        # wait 3 seconds, or until background_stop_event
        state.background_stop_event.wait(timeout=3)


def _background_thread_task(state: State):
    media = asyncio.run(get_spotify_media())
    if media is None or media.thumbnail is None:
        # logging.info("No media thumbnail found")
        state.image = None
        return
    # logging.info(f"Thumbnail found ({media.title} - {media.artist})")
    # convert to image
    image_bytes = asyncio.run(convert_thumbnail_to_bytes(media.thumbnail))
    state.image = Image.open(io.BytesIO(image_bytes))
    state.image.load()
