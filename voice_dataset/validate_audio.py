from pathlib import Path
import wave
import csv

AUDIO_DIR = Path(__file__).parent / "audio"
METADATA_FILE = Path(__file__).parent / "metadata.csv"

SUPPORTED_EXTENSIONS = {".wav"}


def check_audio(file_path: Path):
    try:
        with wave.open(str(file_path), "rb") as audio:
            channels = audio.getnchannels()
            sample_rate = audio.getframerate()
            sample_width = audio.getsampwidth()
            frames = audio.getnframes()
            duration = frames / sample_rate if sample_rate else 0

        problems = []

        if channels != 1:
            problems.append(f"channels={channels}, expected 1")

        if sample_rate != 16000:
            problems.append(f"sample_rate={sample_rate}, expected 16000")

        if sample_width != 2:
            problems.append(f"sample_width={sample_width}, expected 16-bit")

        if duration < 1:
            problems.append(f"duration={duration:.2f}s, too short")

        if duration > 15:
            problems.append(f"duration={duration:.2f}s, too long")

        return {
            "name": file_path.name,
            "channels": channels,
            "sample_rate": sample_rate,
            "sample_width_bits": sample_width * 8,
            "duration": duration,
            "problems": problems,
        }

    except Exception as e:
        return {
            "name": file_path.name,
            "problems": [f"ERROR: {e}"],
        }


def check_metadata(audio_files):
    if not METADATA_FILE.exists():
        print("ERROR: metadata.csv not found")
        return

    listed_files = set()

    with open(METADATA_FILE, "r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f)

        header = next(reader, None)

        for row in reader:
            if len(row) < 2:
                continue

            filename = row[0].strip()
            text = ",".join(row[1:]).strip()

            listed_files.add(filename)

            if not text:
                print(f"WARNING: No transcript for {filename}")

    actual_files = {file.name for file in audio_files}

    missing_from_csv = actual_files - listed_files
    missing_audio = listed_files - actual_files

    if missing_from_csv:
        print("\nWAV files missing from metadata.csv:")
        for name in sorted(missing_from_csv):
            print("  ", name)

    if missing_audio:
        print("\nFiles listed in metadata.csv but not found:")
        for name in sorted(missing_audio):
            print("  ", name)


def main():
    audio_files = sorted(
        file for file in AUDIO_DIR.iterdir()
        if file.suffix.lower() in SUPPORTED_EXTENSIONS
    )

    if not audio_files:
        print("No WAV files found.")
        return

    print(f"\nFound {len(audio_files)} WAV files\n")
    print("-" * 70)

    valid_count = 0

    for file in audio_files:
        result = check_audio(file)

        print(
            f"{result['name']}: "
            f"{result.get('sample_rate', '?')} Hz, "
            f"{result.get('sample_width_bits', '?')}-bit, "
            f"{result.get('channels', '?')} channel(s), "
            f"{result.get('duration', 0):.2f}s"
        )

        if result["problems"]:
            for problem in result["problems"]:
                print(f"   ❌ {problem}")
        else:
            print("   ✅ OK")
            valid_count += 1

    print("\n" + "-" * 70)
    print(f"Valid files: {valid_count}/{len(audio_files)}")

    check_metadata(audio_files)


if __name__ == "__main__":
    main()