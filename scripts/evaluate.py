import json, os, argparse, editdistance

def compute_per(ref_phon, hyp_phon):
    ref_tokens = ref_phon.split()
    hyp_tokens = hyp_phon.split()
    distance = editdistance.eval(ref_tokens, hyp_tokens)
    N = len(ref_tokens) if len(ref_tokens) > 0 else 1
    return distance / N

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--hyp", required=True, help="Path to hypotheses JSONL")
    parser.add_argument("--out", required=True, help="Path to output metrics JSON")
    args = parser.parse_args()

    os.makedirs("results", exist_ok=True)
    total_per = 0.0
    count = 0
    per_by_snr = {}

    with open(args.hyp, "r") as fin:
        for line in fin:
            entry = json.loads(line)
            ref_phon = entry.get("ref_phon", "")
            hyp_phon = entry.get("hyp_phon", "")
            snr = entry.get("snr_db", "clean")

            per = compute_per(ref_phon, hyp_phon)
            total_per += per
            count += 1
            per_by_snr.setdefault(snr, []).append(per)

    avg_per = total_per / count if count > 0 else 0.0
    per_by_snr = {snr: sum(vals)/len(vals) for snr, vals in per_by_snr.items()}

    metrics = {"avg_per": avg_per, "per_by_snr": per_by_snr}
    with open(args.out, "w") as fout:
        json.dump(metrics, fout, indent=2)

    print(f"Evaluation complete. Results saved to {args.out}")

if __name__ == "__main__":
    main()
