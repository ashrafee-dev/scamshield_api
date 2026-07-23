
from io import BytesIO
import numpy as np
import ffmpeg
import whisper


model = whisper.load_model("turbo")

def audio_transcript(audio_file: BytesIO) -> str:
    pcm_bytes, stderr = (
    ffmpeg
    .input("pipe:")
    .output("pipe:", format="f32le", acodec="pcm_f32le", ac=1, ar=16000)
    .run(input=audio_file.getvalue(), capture_stdout=True, capture_stderr=True)
)
    pcm_array = np.frombuffer(pcm_bytes, dtype= np.float32 )
    text = model.transcribe(pcm_array)["text"]

    assert isinstance(text, str)
    return text
