import os
import json

# Optional: try to import pandas + phonemizer if available
try:
    import pandas as pd
    from phonemizer.backend import EspeakBackend
    phonemizer = EspeakBackend(language="hi", punctuation_marks=".,;:!?")
    HAS_PHONEMIZER = True
except ImportError:
    HAS_PHONEMIZER = False

train_dir = "data/audio/hi/train_wav"
test_dir = "data/audio/hi/test_wav"
train_meta = "data/audio/hi/dataset/train.csv"
test_meta = "data/audio/hi/dataset/test.csv"

manifest_path = "data/manifests/hi/noisy.jsonl"
os.makedirs(os.path.dirname(manifest_path), exist_ok=True)

entries = []
utt_id = 1

def add_entries_from_dir(directory, prefix, meta_csv=None):
    global utt_id
    transcripts = {}
    # If metadata CSV exists and pandas is available, load transcripts
    if meta_csv and os.path.exists(meta_csv) and HAS_PHONEMIZER:
        df = pd.read_csv(meta_csv)
        # Adjust column names if needed
        if "filename" in df.columns and "text" in df.columns:
            transcripts = dict(zip(df["filename"], df["text"]))
    else:
        if meta_csv and os.path.exists(meta_csv):
            print(f"Metadata {meta_csv} found but phonemizer/pandas not installed. Skipping transcripts.")

    for fname in sorted(os.listdir(directory)):
        if fname.endswith(".wav"):
            wav_path = os.path.join(directory, fname)
            transcript = transcripts.get(fname.replace(".wav", ".mp3"), "")
            if transcript and HAS_PHONEMIZER:
                ref_phon = phonemizer.phonemize(transcript, strip=True)[0]
            else:
                ref_phon = ""  # fallback if no transcript
            entry = {
                "utt_id": f"{prefix}_{utt_id:04d}",
                "wav_path": wav_path,
                "snr_db": 20,
                "ref_phon": ref_phon
            }
            entries.append(entry)
            utt_id += 1

# Collect entries from both train and test sets
add_entries_from_dir(train_dir, "hi_train", train_meta)
add_entries_from_dir(test_dir, "hi_test", test_meta)

# Write JSONL manifest
with open(manifest_path, "w", encoding="utf-8") as fout:
    for entry in entries:
        fout.write(json.dumps(entry, ensure_ascii=False) + "\n")

print(f"Manifest written to {manifest_path} with {len(entries)} entries.")
