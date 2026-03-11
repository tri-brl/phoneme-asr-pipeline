# phoneme-asr-pipeline

pipeline for phoneme-level and word-level ASR evaluation on Hindi and English, tracked with DVC.

---

## setup

tested on Ubuntu 20.04 / WSL2, Python 3.9+. GPU recommended but CPU works too.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

or with conda:

```bash
conda env create -f environment.yml
conda activate phoneme-asr
```

main dependencies: `torch`, `torchaudio`, `transformers`, `phonemizer`, `dvc`, `matplotlib`, `seaborn`, `tqdm`

---

## repo structure

- `scripts/` - all pipeline scripts (inference, evaluation, plotting)
- `data/` - manifests and audio
- `results/` - outputs and plots
- `dvc/` - pipeline metadata

---

## running the pipeline

**1. data prep**

```bash
python scripts/convert_mp3_to_wav.py data/raw/ data/wav/
python scripts/generate_manifest.py data/wav/ data/manifest.json
```

**2. inference**

```bash
python scripts/run_whisper_hi.py --manifest data/manifest.json --output results/whisper_hi/
python scripts/run_wav2vec2.py --manifest data/manifest.json --output results/wav2vec2/
```

both scripts support chunked runs and resume if a job dies halfway through.

**3. evaluation**

```bash
# word-level WER
python scripts/evaluate.py --pred results/whisper_hi/preds.json --ref data/manifest.json --metric wer

# phoneme-level PER
python scripts/evaluate.py --pred results/whisper_hi/preds.json --ref data/manifest.json --metric per
```

**4. plots**

```bash
python scripts/plot_results.py --input results/ --output results/plots/
```

---

## reproducibility

```bash
dvc repro   # re-run full pipeline
dvc status  # check what's stale
```

---

## results

| model         | WER (%) | PER (%) |
|---------------|---------|---------|
| Hindi Whisper | 12.5    | 18.3    |
| Wav2Vec2      | 14.1    | 20.7    |

![WER comparison](results/wer_plot.png)
![PER vs SNR](results/per_vs_snr_multi.png)
![PER vs SNR mean](results/per_vs_snr_mean.png)

---

## notes

- `phonemizer` needs `espeak` installed at the system level (`sudo apt install espeak`)
- long jobs should be run in chunks using the resume flag
- to re-run from scratch: start from `data/raw/`, convert, generate manifests, run inference, evaluate, plot
- I used AI to help me with formatting this report, as well as with some of my graphs

repo: https://github.com/tri-brl/phoneme-asr-pipeline
