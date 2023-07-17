import pyaudio

CHUNK = 1024 * 2  # samples per frame
FORMAT = pyaudio.paInt16  # audio format (bytes per sample?)
CHANNELS = 1  # single channel for microphone
RATE = 44100  # samples per second
# Signal range is -32k to 32k
# limiting amplitude to +/- 4k
AMPLITUDE_LIMIT = 4096
