#!/usr/bin/env python3
import os
import argparse
import json
from phonemizer import phonemize

# Force phonemizer to use the correct espeak-ng library
os.environ["ESPEAK_LIBRARY"] = "/lib/x86_64-linux-gnu/libespeak-ng.so.1"

def main():
    parser = argparse.ArgumentParser(description="Phonemize hypotheses in a JSONL file")
    parser.add_argument("--infile", required=True, help="Input JSONL file with hypotheses")
    parser.add_argument("--outfile", required=True, help="Output JSONL file with phonemized hypotheses")
    parser.add_argument("--lang", required=True, help="Language code (e.g. 'hi' for Hindi)")
    args = parser.parse_args()

    with open(args.infile, "r", encoding="utf-8") as fin, \
         open(args.outfile, "w", encoding="utf-8") as fout:

        for line in fin:
            entry = json.loads(line)
            hyp = entry.get("hyp", "")
            if hyp.strip():
                hyp_phon = phonemize(
                    hyp,
                    language=args.lang,
                    backend="espeak",
                    strip=True,
                    njobs=1
                )
                entry["hyp_phon"] = hyp_phon
            else:
                entry["hyp_phon"] = ""
            fout.write(json.dumps(entry, ensure_ascii=False) + "\n")

if __name__ == "__main__":
    main()
