import json, os
import matplotlib.pyplot as plt

def main():
    os.makedirs("results", exist_ok=True)

    # Load metrics
    with open("results/metrics.json", "r") as fin:
        metrics = json.load(fin)

    wer = metrics.get("WER", 0.0)
    num_samples = metrics.get("num_samples", 0)

    # Simple bar plot
    plt.figure(figsize=(6,4))
    plt.bar(["WER"], [wer], color="skyblue")
    plt.title(f"Word Error Rate (WER) over {num_samples} samples")
    plt.ylabel("WER")
    plt.ylim(0, 1)

    plt.savefig("results/wer_plot.png")
    print("Plot saved to results/wer_plot.png")

if __name__ == "__main__":
    main()
