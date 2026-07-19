
import whisper


model = whisper.load_model("turbo")

def audio_transcript(audio_file: str) -> str:
    text = model.transcribe(audio_file)["text"]
    assert isinstance(text, str)
    return text
