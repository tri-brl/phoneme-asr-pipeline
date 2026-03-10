import json, os, subprocess

def text_to_phonemes(text, lang="en"):
    """
    Convert text to phonemes using espeak-ng.
    Requires espeak-ng installed and available in PATH.
    """
    try:
        # Run espeak-ng with phoneme output
        result = subprocess.run(
            ["espeak-ng", "-v", lang, "--ipa", text],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error converting text '{text}': {e}")
        return ""

def main():
    os.makedirs("data/manifests/en", exist_ok=True)
    with open("data/manifests/en/clean.jsonl", "r") as fin, \
         open("data/manifests/en/phonemes.jsonl", "w") as fout:
        for line in fin:
            entry = json.loads(line)
            ref_text = entry.get("ref_text", "")
            lang = entry.get("lang", "en")
            entry["ref_phon"] = text_to_phonemes(ref_text, lang)
            fout.write(json.dumps(entry) + "\n")

    print("Phoneme conversion complete. Results saved to data/manifests/en/phonemes.jsonl")

if __name__ == "__main__":
    main()
