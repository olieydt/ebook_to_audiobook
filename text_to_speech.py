import torch
import tempfile
import logging
import subprocess
import os
from pathlib import Path
from TTS.api import TTS

class TextToAudio:
    def __init__(self):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC_ph", progress_bar=False).to(device)
    
    def convert_to_audio(self, title: str, text: str, output_path: str):
        with tempfile.TemporaryDirectory() as tmp_dir_name:
            tmp_file_name = Path(tmp_dir_name) / "temp.wav"
            logging.debug(f"Saving file to output: {tmp_file_name}")
            self.tts.tts_to_file(text=text, file_path=tmp_file_name)
            command = [
                "ffmpeg",
                "-i", tmp_file_name,
                "-codec:a", "libmp3lame",
                "-b:a", "64k",
                "-ac", "1", 
                os.path.join(output_path, f"{title.replace(':', '')}.mp3")
            ]

            try:
                subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            except subprocess.CalledProcessError as e:
                logging.critical(f"Error during conversion: {e.stderr.decode()}")
                raise e
