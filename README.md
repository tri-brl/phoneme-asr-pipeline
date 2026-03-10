# Phoneme-ASR Pipeline

This repository contains a reproducible pipeline for phoneme-level Automatic Speech Recognition (ASR) evaluation.  
The pipeline is managed with **DVC** and produces **phoneme error rate (PER)** metrics bucketed by signal-to-noise ratio (SNR), along with plots for analysis.

---

## 📖 Project Overview
- Converts transcripts to phonemes.  
- Injects controlled noise at specified SNR levels.  
- Runs inference with Whisper.  
- Evaluates phoneme error rate (PER).  
- Generates plots of PER vs SNR for Hindi and combined datasets.  

---

## ⚙️ Requirements
- Python 3.10+  
- [DVC](https://dvc.org/) installed (`pip install dvc`)  
- Virtual environment recommended:
  ```bash
  python -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt
  ```
---

## 📂 Pipeline Stages
- **create_manifest** → builds dataset manifest
- **phoneme_conversion** → converts transcripts to phonemes
- **noise_injection** → injects noise at specified SNR
- **inference** → runs Whisper inference
- **merge_hi** → merges Hindi outputs
- **evaluate / evaluate_hi** → computes PER, bucketed by SNR
- **plot_results / plot_hi / plot_mean** → generate plots

---

## ▶️ Usage
- Clone the repository:
  ```bash
  git clone https://github.com/tri-brl/phoneme-asr-pipeline.git
  cd phoneme-asr-pipeline
  ```

- Set up environment:
  ```bash
  python -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt
  ```

- Run the pipeline:
  ```bash
  dvc repro
  ```

- Fetch outputs (if DVC remote is configured):
  ```bash
  dvc pull
  ```
---

## 📊 Outputs
- **Metrics**:
  - `results/hi_per.json`
  - `results/metrics.json`

- **Plots**:
  - `results/per_vs_snr_multi.png` → Hindi PER vs SNR
  - `results/per_vs_snr_mean.png` → Comparison across datasets

---

## 🔁 Reproducibility
- All stages are tracked by DVC.
- Results can be reproduced exactly with `dvc repro`.
- Large files are managed via DVC remote storage.

---

## ✍️ Author
- Prepared by Tori Baral
