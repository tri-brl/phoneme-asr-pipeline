#!/usr/bin/env python3
import argparse
import json
import matplotlib.pyplot as plt

def load_curves(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    # If the file is a dict (like metrics.json), wrap it in a list
    if isinstance(data, dict):
        return [data]
    return data  # already a list of dicts

def main():
    parser = argparse.ArgumentParser(description="Plot PER vs SNR from one or more JSON files")
    parser.add_argument("--per", type=str, nargs="+", required=True,
                        help="One or more JSON files with PER results aggregated by SNR")
    parser.add_argument("--out", type=str, required=True,
                        help="Output PNG file for the plot")
    args = parser.parse_args()

    plt.figure(figsize=(6,4))

    for path in args.per:
        curves = load_curves(path)
        snr_levels = [c["snr_db"] for c in curves if "snr_db" in c]
        per_values = [c["per"] for c in curves if "per" in c]

        label = path.split("/")[-1]
        plt.plot(snr_levels, per_values, marker="o", linestyle="-", label=label)

    plt.xlabel("SNR (dB)")
    plt.ylabel("Average PER")
    plt.title("PER vs SNR")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(args.out)
    print(f"Plot saved to {args.out}")

if __name__ == "__main__":
    main()
