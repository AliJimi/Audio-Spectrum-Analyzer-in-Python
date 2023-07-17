import settings


def microphone_stream(pyaudio_instance):
    pyaudio_instance.open(
        format=settings.FORMAT,
        channels=settings.CHANNELS,
        rate=settings.RATE,
        input=True,
        output=True,
        frames_per_buffer=settings.CHUNK
    )


def mp3_stream(pyaudio_instance):
    pyaudio_instance.open(
        format=settings.FORMAT,
        channels=settings.CHANNELS,
        rate=settings.RATE,
        input=True,
        output=True,
        frames_per_buffer=settings.CHUNK
    )
