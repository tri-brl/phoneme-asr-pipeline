import json, os, random

def add_noise_to_text(text):
    # Toy example: randomly insert a symbol to simulate noise
    noisy = ""
    for ch in text:
        noisy += ch
        if random.random() < 0.1:  # 10% chance
            noisy += "*"
    return noisy

def main():
    os.makedirs("data/manifests/en", exist_ok=True)
    with open("data/manifests/en/phonemes.jsonl", "r") as fin, \
         open("data/manifests/en/noisy.jsonl", "w") as fout:
        for line in fin:
            entry = json.loads(line)
            entry["noisy_text"] = add_noise_to_text(entry["ref_text"])
            fout.write(json.dumps(entry) + "\n")

    print("Noisy manifest created at data/manifests/en/noisy.jsonl")

if __name__ == "__main__":
    main()
