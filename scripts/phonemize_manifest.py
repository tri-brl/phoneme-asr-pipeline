#!/usr/bin/env python3
import argparse
import json
from phonemizer.backend import EspeakBackend

def main():
    parser = argparse.ArgumentParser(description="Add ref_phon to manifest")
    parser.add_argument("--infile", required=True, help="Input manifest JSONL")
    parser.add_argument("--outfile", required=True, help="Output manifest JSONL with ref_phon")
    parser.add_argument("--lang", required=True, help="Language code (e.g. hi, en, fr)")
    args = parser.parse_args()

    phonemizer = EspeakBackend(language=args.lang, punctuation_marks=".,;:!?")

    with open(args.infile, "r", encoding="utf-8") as fin, \
         open(args.outfile, "w", encoding="utf-8") as fout:
        for line in fin:
            entry = json.loads(line)

            # Use "text" field from manifest as transcript
            transcript = entry.get("text", "")
            if transcript:
                try:
                    entry["ref_phon"] = phonemizer.phonemize([transcript], strip=True)[0]
                except Exception as e:
                    entry["ref_phon"] = ""
                    print(f"Phonemizer error {entry.get('utt_id')}: {e}")
            else:
                entry["ref_phon"] = ""

            fout.write(json.dumps(entry, ensure_ascii=False) + "\n")

if __name__ == "__main__":
    main()
