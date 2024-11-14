import os
import io
import pyaudio
import numpy as np
from openai import OpenAI
from dotenv import load_dotenv
from utils.audio import AudioProcessor
from faster_whisper import WhisperModel


class Interviewer:
    def __init__(
        self,
    ):
        load_dotenv()

        self.preset = None
        self.client = OpenAI(api_key=os.environ.get("OPENSI_API_KEY"))
        self.model = WhisperModel("base", device="cuda", compute_type="float32")
        self.audio_processor = AudioProcessor()
        self.history = []
        self.done = False

    def set_preset(self, preset):
        self.preset = preset

        self.history.append(
            {
                "role": "system",
                "content": self.preset,
            },
        )

    @staticmethod
    def byteplay(bytestream):
        pya = pyaudio.PyAudio()
        stream = pya.open(
            format=pya.get_format_from_width(width=2),
            channels=1,
            rate=24000,
            output=True,
        )
        stream.write(bytestream)
        stream.stop_stream()
        stream.close()

    def tts(self, text):
        with self.client.audio.speech.with_streaming_response.create(
            model="tts-1",
            voice="alloy",
            input=text,
            response_format="wav",
        ) as response:

            buffer = io.BytesIO()

            for chunk in response.iter_bytes():
                buffer.write(chunk)

            buffer.seek(0)

            self.byteplay(buffer.getvalue())

    def response(self):
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=self.history,
                max_tokens=1024,
                n=1,
                stop=None,
            )

            response_text = response.choices[0].message.content

            return response_text

        except Exception as e:
            print("Error generating response\n{}".format(e))

            return "Sorry, can't catch"

    def stt(self):
        try:
            data = self.audio_processor.record_until_silence()
            wav_data = self.audio_processor.to_wav(data)

            segments, _ = self.model.transcribe(wav_data, language="en")

            text = " ".join([segment.text for segment in segments])

        except Exception as e:
            print("Error transcribing\n{}".format(e))
            text = ""

        return text

    def is_done(self, message):
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": "Given this response, {}, does it seem like the person wants to end the conversation immediately? only give a 'yes' or a 'no' in that exact format".format(
                        message
                    ),
                }
            ],
            max_tokens=128,
            n=1,
            stop=None,
        )

        return response.choices[0].message.content.lower() == "yes"
