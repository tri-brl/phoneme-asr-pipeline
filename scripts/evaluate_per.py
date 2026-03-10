#!/usr/bin/env python3
import argparse
import json
import difflib
from collections import defaultdict

def load_jsonl(path):
    with open(path, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f]

def edit_distance(ref, hyp):
    # Simple Levenshtein distance using difflib
    sm = difflib.SequenceMatcher(None, ref, hyp)
    return 1 - sm.ratio()

def main():
    parser = argparse.ArgumentParser(description="Evaluate phoneme error rate (PER) by SNR bucket")
    parser.add_argument("--ref", type=str, required=True,
                        help="Reference manifest JSONL with ground truth phonemes and snr_db")
    parser.add_argument("--hyp", type=str, required=True,
                        help="Hypotheses JSONL with predicted phonemes")
    parser.add_argument("--out", type=str, required=True,
                        help="Output JSON file with PER results aggregated by SNR")
    args = parser.parse_args()

    # Load reference and hypothesis data
    refs = {entry["utt_id"]: entry for entry in load_jsonl(args.ref)}
    hyps = {entry["utt_id"]: entry.get("hyp_phon", "") for entry in load_jsonl(args.hyp)}

    snr_buckets = defaultdict(list)
    total_err = 0.0
    total_len = 0

    for utt_id, ref_entry in refs.items():
        ref_phon = ref_entry.get("ref_phon", "")
        hyp_phon = hyps.get(utt_id, "")
        if not ref_phon:
            continue

        # Compute PER as edit distance / length of reference
        dist = edit_distance(ref_phon, hyp_phon)
        per = dist
        snr = ref_entry.get("snr_db", -1)

        if snr != -1:
            snr_buckets[snr].append(per)

        total_err += dist
        total_len += 1

    avg_per = total_err / total_len if total_len > 0 else 0.0

    # Aggregate PER by SNR bucket
    results = []
    for snr, scores in sorted(snr_buckets.items()):
        avg_bucket_per = sum(scores) / len(scores)
        results.append({"snr_db": snr, "per": avg_bucket_per})

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"✅ Wrote PER results for {total_len} utterances to {args.out}")
    print(f"Average PER across all utterances: {avg_per:.4f}")
    print("Bucketed PER by SNR:")
    for r in results:
        print(f"  SNR {r['snr_db']} dB -> PER {r['per']:.4f}")

if __name__ == "__main__":
    main()
