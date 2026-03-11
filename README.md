# phoneme-asr-pipeline

DVC pipeline that converts text to phonemes, adds noise at different SNR levels, runs wav2vec2 inference, and computes PER. produces plots of PER vs SNR per language + a cross-language mean.

## setup

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

## run

dvc repro

outputs go to `results/`.
