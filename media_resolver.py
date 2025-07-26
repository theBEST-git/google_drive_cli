"""
Utility helpers for pulling audio from
 • local audio/video files, or
 • YouTube URLs.

Return value is always a local audio file path (WAV 16 kHz mono),
ready for any STT transcriber (OpenAI Whisper, Vosk, etc.).

Note:
You have to install FFmpeg system-wide in order to use the functions properly.
This feature aims to convert all video/audio/youtube url into a local audio file path (WAV 16 kHz mono).
Then extract the text from these files and store them on the google drive.
In this way, users will be able to ask the AI agent anything about the meetings or lectures, for example, if these are recordeed.
PROMISING!!!
"""

from __future__ import annotations
import os, re, subprocess, tempfile
from pathlib import Path
from typing import Final

import yt_dlp
import ffmpeg

AUDIO_EXTS: Final = {".mp3", ".wav", ".m4a", ".flac", ".ogg"}
VIDEO_EXTS: Final = {".mp4", ".mov", ".mkv", ".webm"}

YOUTUBE_REGEX: Final = re.compile(
    r"^(https?://)?(www\.|m\.)?(youtube\.com|youtu\.be)/"
)

# ------------------------------------------------------------------ #
# Public helper                                                       #
# ------------------------------------------------------------------ #

def resolve_media(source: str) -> Path:
    """
    Accept a local path or YouTube URL and return a Path to a local
    16-kHz mono WAV file suitable for speech-to-text.

    Raises ValueError on unsupported file types.
    """
    if YOUTUBE_REGEX.match(source):
        audio_mp3 = _download_youtube_audio(source)
        wav_path = _convert_to_wav(audio_mp3)
        return wav_path

    p = Path(source).expanduser().resolve()
    if not p.exists():
        raise FileNotFoundError(p)
    if p.suffix.lower() in AUDIO_EXTS:
        return _ensure_wav(p)
    if p.suffix.lower() in VIDEO_EXTS:
        audio_wav = _extract_audio(p)
        return audio_wav

    raise ValueError("Unsupported media type: " + p.name)


# ------------------------------------------------------------------ #
# Internals                                                           #
# ------------------------------------------------------------------ #

def _download_youtube_audio(url: str) -> Path:
    """Download best-quality audio from YouTube → returns .mp3 Path."""
    td = Path(tempfile.mkdtemp(prefix="ytdlp_"))
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": str(td / "%(id)s.%(ext)s"),
        "quiet": True,
        "noprogress": True,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return td / f"{info['id']}.mp3"


def _extract_audio(video_path: Path) -> Path:
    """Use ffmpeg to pull mono 16-kHz WAV from a video file."""
    out_wav = Path(tempfile.mktemp(suffix=".wav"))
    (
        ffmpeg
        .input(str(video_path))
        .output(str(out_wav), ac=1, ar=16000, **{"loglevel": "error"})
        .overwrite_output()
        .run()
    )
    return out_wav


def _ensure_wav(audio_path: Path) -> Path:
    """Convert any audio type to 16-kHz mono WAV if needed."""
    if audio_path.suffix.lower() == ".wav":
        return audio_path
    return _convert_to_wav(audio_path)


def _convert_to_wav(src: Path) -> Path:
    out_wav = Path(tempfile.mktemp(suffix=".wav"))
    (
        ffmpeg
        .input(str(src))
        .output(str(out_wav), ac=1, ar=16000, **{"loglevel": "error"})
        .overwrite_output()
        .run()
    )
    return out_wav

print("--------------------MEDIA RESOLVERS ARE READY--------------------")