#!/usr/bin/env python3
import argparse
import json
import csv
import os

def main():
    parser = argparse.ArgumentParser(description="Convert Common Voice TSV to JSONL manifest")
    parser.add_argument("--tsv", required=True, help="Input Common Voice TSV file (e.g. validated.tsv)")
    parser.add_argument("--out", required=True, help="Output manifest JSONL")
    parser.add_argument("--audio-dir", required=True, help="Path to audio files directory (clips/)")
    parser.add_argument("--lang", required=True, help="Language code (e.g. hi)")
    args = parser.parse_args()

    with open(args.tsv, "r", encoding="utf-8") as fin, \
         open(args.out, "w", encoding="utf-8") as fout:
        reader = csv.DictReader(fin, delimiter="\t")
        for i, row in enumerate(reader):
            utt_id = f"{args.lang}_utt_{i:06d}"
            wav_path = os.path.join(args.audio_dir, row["path"])
            text = row.get("sentence", "").strip()
            entry = {
                "utt_id": utt_id,
                "wav_path": wav_path,
                "text": text,
                "snr_db": 20  # placeholder if you don’t have SNR
            }
            fout.write(json.dumps(entry, ensure_ascii=False) + "\n")

if __name__ == "__main__":
    main()
