# scripts/create_manifest.py
import os
import json

RAW_DIR = "data/raw/en"
OUT_FILE = "data/manifests/en/clean.jsonl"
SKIPPED_FILE = "results/skipped_files.txt"
TRANSCRIPT_FILE = os.path.join(RAW_DIR, "transcripts.txt")

def load_transcripts():
    mapping = {}
    if os.path.exists(TRANSCRIPT_FILE):
        with open(TRANSCRIPT_FILE, "r", encoding="utf-8") as f:
            for line in f:
                if "|" in line:
                    fname, text = line.strip().split("|", 1)
                    mapping[fname.strip()] = text.strip()
    return mapping

def main():
    transcripts = load_transcripts()
    entries = []
    skipped = []

    for i, fname in enumerate(sorted(os.listdir(RAW_DIR)), start=1):
        if fname.endswith(".wav"):
            if fname in transcripts:
                wav_path = os.path.join(RAW_DIR, fname)
                entry = {
                    "utt_id": f"utt{i}",
                    "lang": "en",
                    "wav_path": wav_path,
                    "ref_text": transcripts[fname]
                }
                entries.append(entry)
            else:
                skipped.append(fname)

    # Write manifest
    os.makedirs(os.path.dirname(OUT_FILE), exist_ok=True)
    with open(OUT_FILE, "w", encoding="utf-8") as f:
        for entry in entries:
            f.write(json.dumps(entry) + "\n")

    print(f"Manifest created at {OUT_FILE} with {len(entries)} entries.")

    # Log skipped files
    if skipped:
        os.makedirs(os.path.dirname(SKIPPED_FILE), exist_ok=True)
        with open(SKIPPED_FILE, "w", encoding="utf-8") as f:
            for fname in skipped:
                f.write(fname + "\n")

        print("⚠ Skipped files (no transcript found):")
        for fname in skipped:
            print(f"   - {fname}")
        print(f"Skipped files logged to {SKIPPED_FILE}")

if __name__ == "__main__":
    main()
