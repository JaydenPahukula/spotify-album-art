from winsdk.windows.media.control import (
    GlobalSystemMediaTransportControlsSessionManager,
    GlobalSystemMediaTransportControlsSessionMediaProperties,
)
from winsdk.windows.storage.streams import DataReader, IRandomAccessStreamReference


async def get_spotify_media() -> GlobalSystemMediaTransportControlsSessionMediaProperties | None:
    manager = await GlobalSystemMediaTransportControlsSessionManager.request_async()
    for session in manager.get_sessions():
        try:
            if session.source_app_user_model_id.lower() == "spotify.exe":
                # found spotify session
                return await session.try_get_media_properties_async()
        except Exception:
            pass
    # no spotify session
    return None


async def convert_thumbnail_to_bytes(thumbnail: IRandomAccessStreamReference) -> bytes:
    stream = await thumbnail.open_read_async()
    reader = DataReader(stream)
    await reader.load_async(stream.size)
    return bytes(reader.read_buffer(stream.size))
