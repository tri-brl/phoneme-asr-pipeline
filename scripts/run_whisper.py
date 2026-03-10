import whisper
import json
import os
from g2p_en import G2p

# Load Whisper model (choose "base", "small", "medium", "large")
model = whisper.load_model("base")
g2p = G2p()

# Path to your noisy manifest
manifest_path = "data/manifests/en/noisy.jsonl"

results = []
with open(manifest_path, "r") as fin:
    for line in fin:
        entry = json.loads(line)
        audio_path = entry["wav_path"]
        ref_phon = entry["ref_phon"]

        # Run Whisper transcription
        result = model.transcribe(audio_path, language="en")
        hyp_text = result["text"]

        # Convert text to phonemes
        hyp_phon = " ".join(g2p(hyp_text))

        results.append({
            "utt_id": entry["utt_id"],
            "snr_db": entry["snr_db"],
            "audio_filepath": audio_path,
            "ref_phon": ref_phon,
            "hyp_phon": hyp_phon   # evaluator expects this field
        })

# Save hypotheses
os.makedirs("results", exist_ok=True)
with open("results/whisper_hypotheses.jsonl", "w") as fout:
    for r in results:
        fout.write(json.dumps(r) + "\n")

print("Whisper hypotheses saved to results/whisper_hypotheses.jsonl")
