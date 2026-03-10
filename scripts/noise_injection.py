import json, os
import soundfile as sf
import numpy as np

def add_noise(signal, snr_db, rng):
    signal_power = np.mean(signal ** 2)
    snr_linear = 10 ** (snr_db / 10)
    noise_power = signal_power / snr_linear
    noise = rng.normal(0.0, np.sqrt(noise_power), size=signal.shape)
    return signal + noise

def add_noise_to_file(input_wav, output_wav, snr_db, seed=None):
    signal, sr = sf.read(input_wav)

    # Convert stereo to mono if needed
    if signal.ndim > 1:
        signal = signal.mean(axis=1)

    rng = np.random.default_rng(seed)
    noisy_signal = add_noise(signal, snr_db, rng)
    sf.write(output_wav, noisy_signal, sr)

def main():
    os.makedirs("data/manifests/en", exist_ok=True)
    os.makedirs("data/noisy/en", exist_ok=True)

    snr_levels = [0, 5, 10, 15, 20]  # adjust as needed
    rng = np.random.default_rng(42)

    with open("data/manifests/en/phonemes.jsonl", "r") as fin, \
         open("data/manifests/en/noisy.jsonl", "w") as fout:
        for line in fin:
            entry = json.loads(line)
            wav_path = entry["wav_path"]
            stem = os.path.splitext(os.path.basename(wav_path))[0]

            for snr in snr_levels:
                noisy_wav_path = f"data/noisy/en/{stem}_snr{snr}.wav"
                add_noise_to_file(wav_path, noisy_wav_path, snr, seed=42)
                noisy_entry = entry.copy()
                noisy_entry["wav_path"] = noisy_wav_path
                noisy_entry["snr_db"] = snr
                fout.write(json.dumps(noisy_entry) + "\n")

    print("Noise injection complete. Results saved to data/manifests/en/noisy.jsonl")

if __name__ == "__main__":
    main()
