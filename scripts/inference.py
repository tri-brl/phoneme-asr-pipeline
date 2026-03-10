import json, os
import torch
import soundfile as sf
import numpy as np
import librosa
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC

MODEL_NAME = "facebook/wav2vec2-lv-60-espeak-cv-ft"

def load_model():
    processor = Wav2Vec2Processor.from_pretrained(MODEL_NAME)
    model = Wav2Vec2ForCTC.from_pretrained(MODEL_NAME)
    model.eval()
    return processor, model

def run_inference(wav_path, processor, model):
    # Load audio
    speech, sr = sf.read(wav_path)

    # Convert stereo to mono if needed
    if speech.ndim > 1:
        speech = speech.mean(axis=1)

    # Resample to 16kHz if needed
    target_sr = 16000
    if sr != target_sr:
        speech = librosa.resample(speech.astype(np.float32), orig_sr=sr, target_sr=target_sr)
        sr = target_sr

    # Prepare inputs
    inputs = processor(speech, sampling_rate=sr, return_tensors="pt", padding=True)
    with torch.no_grad():
        logits = model(inputs.input_values).logits
    predicted_ids = torch.argmax(logits, dim=-1)
    transcription = processor.batch_decode(predicted_ids)[0]
    return transcription.strip()

def main():
    os.makedirs("data/manifests/en", exist_ok=True)
    processor, model = load_model()

    with open("data/manifests/en/noisy.jsonl", "r") as fin, \
         open("data/manifests/en/hypotheses.jsonl", "w") as fout:
        for line in fin:
            entry = json.loads(line)
            wav_path = entry["wav_path"]
            hyp_phon = run_inference(wav_path, processor, model)
            entry["hyp_phon"] = hyp_phon
            fout.write(json.dumps(entry) + "\n")

    print("Inference complete. Results saved to data/manifests/en/hypotheses.jsonl")

if __name__ == "__main__":
    main()
