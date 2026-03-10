import json
import matplotlib.pyplot as plt
import argparse

def load_per(path):
    with open(path, "r") as f:
        return json.load(f)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--per", nargs="+", required=True,
                        help="List of PER metric files (JSON)")
    parser.add_argument("--out", required=True,
                        help="Output plot filename")
    args = parser.parse_args()

    # Load all PER curves
    curves = [load_per(p) for p in args.per]

    # Assume each JSON has {"snr_db": [...], "per": [...]}
    snr_levels = curves[0]["snr_db"]
    per_values = [c["per"] for c in curves]

    # Compute mean PER across languages
    mean_per = [sum(vals)/len(vals) for vals in zip(*per_values)]

    # Plot each language curve
    for i, c in enumerate(curves):
        plt.plot(c["snr_db"], c["per"], label=f"Lang {i+1}")

    # Plot mean curve
    plt.plot(snr_levels, mean_per, label="Mean", linewidth=3, color="black")

    plt.xlabel("SNR (dB)")
    plt.ylabel("Phoneme Error Rate (PER)")
    plt.legend()
    plt.savefig(args.out)
