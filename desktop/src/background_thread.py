import asyncio
import io
import threading

from PIL import Image
from src.state import state
from src.windows import convert_thumbnail_to_bytes, get_spotify_media
from winsdk.windows.media.control import (
    GlobalSystemMediaTransportControlsSessionMediaProperties,
)


def initialize_background_thread():
    state.background_stop_event = threading.Event()
    state.background_thread = threading.Thread(
        target=_background_thread,
        daemon=True,
    )
    state.background_thread.start()


def _background_thread():
    while not state.background_stop_event.is_set():
        _background_thread_task()
        # wait 3 seconds, or until background_stop_event
        state.background_stop_event.wait(timeout=3)


def _background_thread_task():
    media = asyncio.run(get_spotify_media())

    if media is None or media.thumbnail is None:
        if state.last_media_key is not None:
            state.last_media_key = None
            state.image = None
            # clear the panel
            # TODO
        return

    # check if changed
    key = _get_media_key(media)
    if key == state.last_media_key:
        return
    state.last_media_key = key

    # new thumbnail image
    image_bytes = asyncio.run(convert_thumbnail_to_bytes(media.thumbnail))
    state.image = Image.open(io.BytesIO(image_bytes))
    state.image.load()
    state.image = state.image.convert("RGB").resize((64, 64))
    # convert image to bytes
    data = bytearray()
    for r, g, b in state.image.getdata():
        rgb565 = ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)
        data.append(rgb565 & 0xFF)
        data.append((rgb565 >> 8) & 0xFF)
    # send image to the panel
    # TODO  send(bytes(data))


# get a key that tries to uniquely identify the current media, so we can tell if the media changed
def _get_media_key(media: GlobalSystemMediaTransportControlsSessionMediaProperties) -> str:
    return f"{media.title},{media.artist},{media.album_title},{media.track_number},{media.subtitle}"
