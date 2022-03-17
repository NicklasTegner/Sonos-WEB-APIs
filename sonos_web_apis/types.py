from enum import Enum

class AudioClipType:
    """Indicates the type of sound that Sonos should play. Specify the audioClipType in the clipType key in the loadAudioClip command. For example, you can use this enumeration to play sounds built into the Sonos firmware. Currently there’s only one sound available, the CHIME sound.
    """
	# This is the default Sonos audioClipType.
    CHIME = "CHIME"
	
	# (Optional) This value indicates that you provided a custom streamUrl. You don’t need to provide this value as input to loadAudioClip as the presence of streamUrl implies a custom clipType.
    CUSTOM = "CUSTOM"

class AudioClipState(Enum):
    """Audio clips transition from pending (on load) to active to done. Sonos returns the state only in events.
    """
    ACTIVE = "ACTIVE" # Currently playing.
    DISMISSED = "DISMISSED" # Dismissed. / cancelled
    DONE = "DONE" # Playback complete.
    ERROR = "ERROR" # Playback encountered an error.
    INTERRUPTED = "INTERRUPTED" # Playback interrupted, for example, by a high priority audio clip.

class AudioClipPriority(Enum):
    """Sonos uses this enumeration to order concurrent clips.
    """
    LOW = "LOW" # Low priority clip. Sonos optionally mixes the clip over the content.
    HIGH = "HIGH" # High Priority clip. Sonos always pauses content and takes exclusive control of the speaker to play this clip.

class Capabilities(Enum):
    """The set of capabilities provided by the player. A player can and usualy has multiple capabilities.
    """
    PLAYBACK = "PLAYBACK" # The player can produce audio. You can target it for playback.
    CLOUD = "CLOUD" # The player can send commands and receive events over the internet.
    HT_PLAYBACK = "HT_PLAYBACK" # The player is a home theater source. It can reproduce the audio from a home theater system, typically delivered by S/PDIF or HDMI.
    HT_POWER_STATE = "HT_POWER_STATE" # The player can control the home theater power state. For example, it can switch a connected TV on or off.
    AIRPLAY = "AIRPLAY" # The player can host AirPlay streams. This capability is present when the device is advertising AirPlay support.
    LINE_IN = "LINE_IN" # The player has an analog line-in.
    AUDIO_CLIP = "AUDIO_CLIP" # The device is capable of playing audio clip notifications.
    VOICE = "VOICE" # The device supports the voice namespace (not yet implemented in the upstream api).
    SPEAKER_DETECTION = "SPEAKER_DETECTION" # The component device is capable of detecting connected speaker drivers.
    FIXED_VOLUME = "FIXED_VOLUME" # The device supports fixed volume.
