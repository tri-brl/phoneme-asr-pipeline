import json, os

def main():
    manifest = [
        {
            "utt_id": "utt1",
            "lang": "en",
            "wav_path": "data/raw/en/sample1.wav",
            "ref_text": "hello world"
        }
    ]
    os.makedirs("data/manifests/en", exist_ok=True)
    with open("data/manifests/en/clean.jsonl", "w") as f:
        for entry in manifest:
            f.write(json.dumps(entry) + "\n")
    print("Manifest created at data/manifests/en/clean.jsonl")

if __name__ == "__main__":
    main()
