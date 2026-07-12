import asyncio
import io
import logging
import os
import sys
import threading
import signal
import pystray
from PIL import Image
from .windows import get_spotify_media, convert_thumbnail_to_bytes

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


class App:
    LOG_FILE_PATH = os.path.join(ROOT_DIR, "desktop", "main.log")
    ICON_PATH = os.path.join(ROOT_DIR, "desktop", "assets", "disk.png")

    def __init__(self, args):
        logging.basicConfig(
            level="INFO",
            format="%(asctime)s %(levelname)s: %(message)s",
            handlers=[
                logging.FileHandler(self.LOG_FILE_PATH),
                *([logging.StreamHandler(sys.stdout)] if args.debug else []),
            ],
        )

        # setup the background thread
        self.background_stop_event = threading.Event()
        self.background_thread = threading.Thread(
            target=self.background_thread_run,
            daemon=True,
        )

        # make tray icon
        self.tray_icon = pystray.Icon(
            "SpotifyAlbumArt",
            Image.open(self.ICON_PATH),
            "Spotify Album Art",
            menu=pystray.Menu(
                pystray.MenuItem("Button", self.test_button),
                pystray.MenuItem("Show Image", self.show_image),
                pystray.Menu.SEPARATOR,
                pystray.MenuItem("Exit", self.quit),
            ),
        )

        signal.signal(signal.SIGINT, self.quit)

    def run(self):
        logging.info("================ Starting ================")
        self.background_thread.start()
        self.tray_icon.run()

    def quit(self, sig=None, frame=None):
        logging.info("Exiting")
        logging.info(f"Exiting{self.background_thread.is_alive()}")

        # stop the background thread
        self.background_stop_event.set()
        self.background_thread.join()

        self.tray_icon.stop()

    def show_image(self):
        if self.image is None:
            pystray.Icon.notify(self.tray_icon, "No image found :(")
        else:
            self.image.show()

    def test_button(self):
        logging.info("Test button pressed")

    def background_thread_run(self):
        while not self.background_stop_event.is_set():
            self.background_thread_task()
            # wait 3 seconds, or until background_stop_event
            self.background_stop_event.wait(timeout=3)

    def background_thread_task(self):
        # try to get the current media thumbnail
        media = asyncio.run(get_spotify_media())
        if media is None or media.thumbnail is None:
            logging.info("No media thumbnail found")
            self.image = None
            return
        logging.info(f"Thumbnail found ({media.title} - {media.artist})")
        # convert to image
        image_bytes = asyncio.run(convert_thumbnail_to_bytes(media.thumbnail))
        self.image = Image.open(io.BytesIO(image_bytes))
        self.image.load()
