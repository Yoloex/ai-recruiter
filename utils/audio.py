import io
import pydub
import pyaudio
import webrtcvad
import numpy as np


class AudioProcessor:
    def __init__(
        self, format=pyaudio.paInt16, channels=1, rate=16000, chunk_length=30
    ):
        self.format = format
        self.channels = channels
        self.rate = rate
        self.chunk_length = chunk_length
        self.silent_duration = 3  # In seconds
        self.chunk_size = int(
            chunk_length * self.rate / 1000
        )  # Will record milliseconds of chunk_length
        self.audio_interface = pyaudio.PyAudio()
        self.stream = None
        self.vad = webrtcvad.Vad(1)

    def record_until_silence(self):
        print("Recording ...")

        frames = []

        self.stream = self.audio_interface.open(
            format=self.format,
            channels=self.channels,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk_size,
        )

        silent_frames = 0

        while True:

            data = self.stream.read(self.chunk_size)

            is_speech = self.vad.is_speech(data, sample_rate=self.rate)

            if not is_speech:
                silent_frames += 1

            if silent_frames >= self.silent_duration / self.chunk_length * 1000:
                break

            frames.append(data)

        self.stream.stop_stream()
        self.stream.close()

        return b"".join(frames)

    def to_wav(self, audio_chunk):
        audio_segment = pydub.AudioSegment(
            data=audio_chunk,
            sample_width=self.audio_interface.get_sample_size(self.format),
            frame_rate=self.rate,
            channels=self.channels,
        )
        wav_io = io.BytesIO()
        audio_segment.export(wav_io, format="wav")

        return wav_io

    def close(self):
        self.audio_interface.terminate()
