import json, os
import editdistance

def main():
    os.makedirs("results", exist_ok=True)
    total_ed = 0
    total_len = 0
    num_samples = 0

    with open("data/manifests/en/hypotheses.jsonl", "r") as fin:
        for line in fin:
            entry = json.loads(line)
            ref = entry["ref_text"].lower()
            hyp = entry["hypothesis"].lower()
            ed = editdistance.eval(ref, hyp)
            total_ed += ed
            total_len += len(ref)
            num_samples += 1

    wer = total_ed / total_len if total_len > 0 else 0.0
    metrics = {
        "num_samples": num_samples,
        "total_edit_distance": total_ed,
        "total_ref_length": total_len,
        "WER": wer
    }

    with open("results/metrics.json", "w") as fout:
        json.dump(metrics, fout, indent=2)

    print("Evaluation complete. Metrics saved to results/metrics.json")

if __name__ == "__main__":
    main()
