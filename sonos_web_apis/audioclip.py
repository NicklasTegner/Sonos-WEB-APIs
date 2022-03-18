from .types import SonosAudioClipPriority
from .types import SonosAudioClipType

class AudioClip:
    def __init__(self, app_id:str=None, clip_type:SonosAudioClipType=None, http_authorization_header:str=None, name:str=None, priority:SonosAudioClipPriority=None, stream_url:str=None, volume:int=None):
        self._app_id = app_id
        self._clip_type = clip_type
        self._http_authorization_header = http_authorization_header
        self._name = name
        self._priority = priority
        self._stream_url = stream_url
        self._volume = volume
