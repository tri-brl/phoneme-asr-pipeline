import json
import matplotlib.pyplot as plt
import os

def main():
    os.makedirs("results", exist_ok=True)

    # Load metrics
    with open("results/metrics.json", "r") as fin:
        metrics = json.load(fin)

    per_by_snr = metrics.get("per_by_snr", {})
    snrs = sorted(per_by_snr.keys(), key=lambda x: float(x) if x != "clean" else float("inf"))
    values = [per_by_snr[snr] for snr in snrs]

    # Plot
    plt.figure(figsize=(8, 6))
    plt.plot(snrs, values, marker="o", linestyle="-", color="blue", label="PER vs SNR")
    plt.xlabel("SNR (dB)")
    plt.ylabel("Phoneme Error Rate (PER)")
    plt.title("PER vs. SNR")
    plt.grid(True)
    plt.legend()

    # Save plot
    out_path = "results/per_vs_snr.png"
    plt.savefig(out_path)
    print(f"Plot saved to {out_path}")

if __name__ == "__main__":
    main()
