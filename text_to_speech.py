import torch
import tempfile
import logging
import subprocess
import os
from pathlib import Path
from enum import Enum


class Type(Enum):
    COQUI: 1
    WHISPER: 2


MODELS = {"COQUI": Type.COQUI, "WHIPSER": Type.WHISPER}


class TextToAudio:
    def __init__(self, type: Type):
        self.type = type
        device = "cuda" if torch.cuda.is_available() else "cpu"
        if type == Type.COQUI:
            from TTS.api import TTS

            self.tts = TTS(
                model_name="tts_models/en/ljspeech/tacotron2-DDC_ph", progress_bar=False
            ).to(device)
        else:
            from whisperspeech.pipeline import Pipeline

            self.tts = Pipeline(
                s2a_ref="collabora/whisperspeech:s2a-q4-tiny-en+pl.model"
            )

    def inner_convert(self, text: str, file_path: str):
        if self.type == Type.COQUI:
            return self.tts.tts_to_file(text=text, file_path=file_path)
        elif self.type == Type.WHISPER:
            return self.tts.generate_to_file(file_path, text)
        raise Exception("not implemented")

    def convert_to_audio(self, title: str, text: str, output_path: str):
        with tempfile.TemporaryDirectory() as tmp_dir_name:
            tmp_file_name = Path(tmp_dir_name) / "temp.wav"
            logging.debug(f"Saving file to output: {tmp_file_name}")
            self.inner_convert(text=text, file_path=tmp_file_name)
            command = [
                "ffmpeg",
                "-i",
                tmp_file_name,
                "-codec:a",
                "libmp3lame",
                "-b:a",
                "64k",
                "-ac",
                "1",
                os.path.join(output_path, f"{title.replace(':', '')}.mp3"),
            ]

            try:
                subprocess.run(
                    command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
                )
            except subprocess.CalledProcessError as e:
                logging.critical(f"Error during conversion: {e.stderr.decode()}")
                raise e
