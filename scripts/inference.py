import json, os

def run_asr(noisy_text):
    # Toy example: pretend ASR just lowercases and strips noise markers
    return noisy_text.replace("*", "").lower()

def main():
    os.makedirs("data/manifests/en", exist_ok=True)
    with open("data/manifests/en/noisy.jsonl", "r") as fin, \
         open("data/manifests/en/hypotheses.jsonl", "w") as fout:
        for line in fin:
            entry = json.loads(line)
            entry["hypothesis"] = run_asr(entry["noisy_text"])
            fout.write(json.dumps(entry) + "\n")

    print("Inference results written to data/manifests/en/hypotheses.jsonl")

if __name__ == "__main__":
    main()
