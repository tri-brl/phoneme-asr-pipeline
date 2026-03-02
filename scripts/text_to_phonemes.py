import json, os

# Simple phoneme mapping (toy example)
phoneme_map = {
    "hello": ["HH", "AH", "L", "OW"],
    "world": ["W", "ER", "L", "D"]
}

def text_to_phonemes(text):
    words = text.lower().split()
    phonemes = []
    for w in words:
        phonemes.extend(phoneme_map.get(w, [w]))  # fallback: keep word if not mapped
    return phonemes

def main():
    os.makedirs("data/manifests/en", exist_ok=True)
    with open("data/manifests/en/clean.jsonl", "r") as fin, \
         open("data/manifests/en/phonemes.jsonl", "w") as fout:
        for line in fin:
            entry = json.loads(line)
            entry["phonemes"] = text_to_phonemes(entry["ref_text"])
            fout.write(json.dumps(entry) + "\n")

    print("Phoneme manifest created at data/manifests/en/phonemes.jsonl")

if __name__ == "__main__":
    main()
