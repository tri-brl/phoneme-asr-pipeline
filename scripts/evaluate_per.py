#!/usr/bin/env python3
import argparse
import json
import difflib

def load_jsonl(path):
    with open(path, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f]

def edit_distance(ref, hyp):
    # Simple Levenshtein distance using difflib
    sm = difflib.SequenceMatcher(None, ref, hyp)
    return 1 - sm.ratio()

def main():
    parser = argparse.ArgumentParser(description="Evaluate phoneme error rate (PER)")
    parser.add_argument("--ref", type=str, required=True,
                        help="Reference manifest JSONL with ground truth phonemes")
    parser.add_argument("--hyp", type=str, required=True,
                        help="Hypotheses JSONL with predicted phonemes")
    parser.add_argument("--out", type=str, required=True,
                        help="Output JSON file with PER results")
    args = parser.parse_args()

    refs = {entry["utt_id"]: entry.get("ref_phon", "") for entry in load_jsonl(args.ref)}
    hyps = {entry["utt_id"]: entry.get("hyp_phon", "") for entry in load_jsonl(args.hyp)}

    total_err = 0.0
    total_len = 0
    per_scores = {}

    for utt_id, ref_phon in refs.items():
        hyp_phon = hyps.get(utt_id, "")
        if not ref_phon:
            continue
        # Compute PER as edit distance / length of reference
        dist = edit_distance(ref_phon, hyp_phon)
        per = dist
        per_scores[utt_id] = per
        total_err += dist
        total_len += 1

    avg_per = total_err / total_len if total_len > 0 else 0.0

    results = {
        "utterance_count": total_len,
        "average_per": avg_per,
        "per_scores": per_scores
    }

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"✅ Wrote PER results for {total_len} utterances to {args.out}")
    print(f"Average PER: {avg_per:.4f}")

if __name__ == "__main__":
    main()
