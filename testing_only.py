# cli_transcribe.py
import argparse, whisper  # pip install -U openai-whisper
from media_resolver import resolve_media

parser = argparse.ArgumentParser(description="Transcribe local or YouTube media.")
parser.add_argument("source", help="Path to media file or YouTube URL")
args = parser.parse_args()

audio_file = resolve_media(args.source)
print("Audio ready →", audio_file)

model = whisper.load_model("base")       # or call OpenAI Whisper API
result = model.transcribe(str(audio_file))
print(result["text"])
