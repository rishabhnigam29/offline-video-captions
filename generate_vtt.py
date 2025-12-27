import subprocess
from pathlib import Path
import whisper
import soundfile as sf
import imageio_ffmpeg

# ================= CONFIG =================

INPUT_ROOT = Path("course")
OUTPUT_ROOT = Path("captions")

MODEL_SIZE = "small"     # tiny | base | small | medium | large
LANGUAGE = "en"

VIDEO_EXTENSIONS = {".mp4", ".mkv", ".mov", ".avi", ".webm"}

# ==========================================


def load_whisper():
    print("🔄 Loading Whisper model...")
    return whisper.load_model(MODEL_SIZE)


def extract_audio(video_path: Path, wav_path: Path):
    """
    Extract mono 16kHz WAV using pip-installed FFmpeg
    """
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

    cmd = [
        ffmpeg_exe,
        "-y",
        "-i", str(video_path),
        "-vn",
        "-ac", "1",
        "-ar", "16000",
        "-acodec", "pcm_s16le",
        str(wav_path)
    ]

    subprocess.run(cmd, check=True)


def format_timestamp(seconds: float) -> str:
    """
    WebVTT-compliant timestamp (dot milliseconds)
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{secs:06.3f}"


def write_vtt(segments, vtt_path: Path):
    with open(vtt_path, "w", encoding="utf-8") as f:
        f.write("WEBVTT\n\n")

        for seg in segments:
            text = seg["text"].strip()
            if not text:
                continue

            start = format_timestamp(seg["start"])
            end = format_timestamp(seg["end"])

            f.write(f"{start} --> {end}\n")
            f.write(f"{text}\n\n")


def transcribe_to_vtt(model, wav_path: Path, vtt_path: Path):
    # Load WAV safely (no FFmpeg here)
    audio, sr = sf.read(wav_path)
    audio = audio.astype("float32")

    result = model.transcribe(
        audio,
        fp16=False,
        language=LANGUAGE,
        condition_on_previous_text=False,
        no_speech_threshold=0.6
    )

    write_vtt(result["segments"], vtt_path)


def process_video(model, video_path: Path):
    relative = video_path.relative_to(INPUT_ROOT)
    output_dir = OUTPUT_ROOT / relative.parent
    output_dir.mkdir(parents=True, exist_ok=True)

    vtt_path = output_dir / f"{video_path.stem}.vtt"

    if vtt_path.exists():
        print(f"⏭️  Skipping: {relative}")
        return

    wav_path = video_path.with_suffix(".wav")

    print(f"🎧 Extracting audio: {relative}")
    extract_audio(video_path, wav_path)

    print(f"📝 Transcribing: {relative.name}")
    transcribe_to_vtt(model, wav_path, vtt_path)

    wav_path.unlink(missing_ok=True)

    print(f"✅ Created: {vtt_path.relative_to(OUTPUT_ROOT)}")


def scan_course(model):
    found = False
    for path in INPUT_ROOT.rglob("*"):
        if path.suffix.lower() in VIDEO_EXTENSIONS:
            found = True
            process_video(model, path)

    if not found:
        print("⚠️ No videos found.")


def main():
    print("=== STARTING CAPTION GENERATION ===")

    if not INPUT_ROOT.exists():
        raise FileNotFoundError("Course folder not found")

    OUTPUT_ROOT.mkdir(exist_ok=True)

    model = load_whisper()
    scan_course(model)

    print("\n🎉 All captions generated successfully.")


if __name__ == "__main__":
    main()
