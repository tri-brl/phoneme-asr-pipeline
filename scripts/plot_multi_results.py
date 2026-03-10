import json
import matplotlib.pyplot as plt

def load_metrics(path):
    with open(path, "r") as fin:
        return json.load(fin)

def plot_curve(metrics, label, style="-"):
    per_by_snr = metrics.get("per_by_snr", {})
    # Convert keys to floats for plotting
    snrs = sorted([float(k) for k in per_by_snr.keys()])
    # Use the original string keys to fetch values
    values = [per_by_snr[str(int(snr))] for snr in snrs]
    plt.plot(snrs, values, marker="o", linestyle=style, label=label)

def main():
    # Add experiments here with labels and file paths
    experiments = {
        "English Wav2Vec2": ("results/en_metrics.json", "--"),
        "Hindi Wav2Vec2": ("results/hi_metrics.json", "-"),
        "English Whisper": ("results/whisper_metrics.json", ":")
    }

    plt.figure(figsize=(8,6))
    for label, (path, style) in experiments.items():
        metrics = load_metrics(path)
        print(f"Loaded {label}: {metrics['per_by_snr']}")
        plot_curve(metrics, label, style)

    plt.xlabel("SNR (dB)")
    plt.ylabel("Phoneme Error Rate (PER)")
    plt.title("PER vs SNR (Multiple Experiments)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig("results/per_vs_snr_multi.png")
    print("Plot saved to results/per_vs_snr_multi.png")

if __name__ == "__main__":
    main()
