
import whisper


model = whisper.load_model("turbo")

def audio_transcript(audio_file):
    return model.transcribe(audio_file)["text"]
