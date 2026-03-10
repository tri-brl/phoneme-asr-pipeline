import argparse
import json
import os
import torch
import soundfile as sf
import numpy as np
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
from g2p_en import G2p

def load_model(lang):
    if lang == "en":
        model_name = "facebook/wav2vec2-base-960h"
    elif lang == "hi":
        # Public Hindi model (community fork)
        model_name = "keshan/indicwav2vec-hindi"
    else:
        raise ValueError("Unsupported language: choose 'en' or 'hi'")
    processor = Wav2Vec2Processor.from_pretrained(model_name)
    model = Wav2Vec2ForCTC.from_pretrained(model_name)
    model.to("cpu")
    return processor, model

def transcribe(audio_path, processor, model):
    speech, sr = sf.read(audio_path)
    if sr != 16000:
        import librosa
        speech = librosa.resample(speech, orig_sr=sr, target_sr=16000)
    input_values = processor(speech, return_tensors="pt", sampling_rate=16000).input_values
    with torch.no_grad():
        logits = model(input_values).logits
    predicted_ids = torch.argmax(logits, dim=-1)
    transcription = processor.decode(predicted_ids[0])
    return transcription

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--lang", required=True, help="Language code: en or hi")
    parser.add_argument("--out", required=True, help="Output hypotheses JSONL path")
    args = parser.parse_args()

    manifest_path = f"data/manifests/{args.lang}/noisy.jsonl"
    processor, model = load_model(args.lang)

    g2p = G2p() if args.lang == "en" else None
    results = []

    with open(manifest_path, "r") as fin:
        for line in fin:
            entry = json.loads(line)
            audio_path = entry["wav_path"]
            ref_phon = entry["ref_phon"]

            hyp_text = transcribe(audio_path, processor, model)

            if args.lang == "en":
                hyp_phon = " ".join(g2p(hyp_text))
            else:
                # For Hindi, keep text for now (phoneme conversion can be added later)
                hyp_phon = hyp_text

            results.append({
                "utt_id": entry["utt_id"],
                "snr_db": entry["snr_db"],
                "audio_filepath": audio_path,
                "ref_phon": ref_phon,
                "hyp_phon": hyp_phon
            })

    os.makedirs("results", exist_ok=True)
    with open(args.out, "w") as fout:
        for r in results:
            fout.write(json.dumps(r) + "\n")

    print(f"Wav2Vec2 hypotheses saved to {args.out}")

if __name__ == "__main__":
    main()
