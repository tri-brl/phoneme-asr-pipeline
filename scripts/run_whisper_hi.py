#!/usr/bin/env python3
import argparse
import json
import torch
import whisper
from tqdm import tqdm
import os
import sys
import gc
from multiprocessing import Pool

# Optional phonemizer
try:
    from phonemizer.backend import EspeakBackend
    phonemizer_backend = EspeakBackend
    HAS_PHONEMIZER = True
except ImportError:
    HAS_PHONEMIZER = False
    phonemizer_backend = None

def load_config(path):
    if path and os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def process_language(args_tuple):
    lang, manifest_path, out_path, model_size, limit, log_path, no_phonemizer, device, batch_size, chunk_id, total_chunks = args_tuple

    if log_path:
        log_file = open(log_path, "a", encoding="utf-8")
        sys.stdout = log_file
        sys.stderr = log_file
        print(f"🔎 Logging enabled for {lang}. Writing to {log_path}")

    # Read manifest
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest_entries = [json.loads(line) for line in f]

    if limit is not None:
        manifest_entries = manifest_entries[:limit]
        print(f"⚡ [{lang}] Processing only first {limit} utterances")

    # Split manifest into chunks for multiprocessing
    if total_chunks > 1:
        chunk_size = len(manifest_entries) // total_chunks
        start = chunk_id * chunk_size
        end = (chunk_id + 1) * chunk_size if chunk_id < total_chunks - 1 else len(manifest_entries)
        manifest_entries = manifest_entries[start:end]
        print(f"🧩 [{lang}] Worker {chunk_id+1}/{total_chunks} processing {len(manifest_entries)} utterances")

    # Resume support
    processed_ids = set()
    results = []
    if os.path.exists(out_path):
        with open(out_path, "r", encoding="utf-8") as fout:
            for line in fout:
                entry = json.loads(line)
                results.append(entry)
                processed_ids.add(entry["utt_id"])
        print(f"🔄 [{lang}] Resuming: {len(processed_ids)} utterances already processed")

    # Initialize phonemizer
    if HAS_PHONEMIZER and not no_phonemizer:
        phonemizer = phonemizer_backend(language=lang, punctuation_marks=".,;:!?")
    else:
        phonemizer = None

    # Load Whisper model ONCE
    print(f"🚀 Loading Whisper model {model_size} on {device}")
    model = whisper.load_model(model_size, device=device)

    # Global progress bar across all utterances in this chunk
    total = len(manifest_entries)
    with tqdm(total=total, desc=f"Transcribing {lang} chunk {chunk_id+1}/{total_chunks}", unit="utt") as pbar:
        for entry in manifest_entries:
            wav_path = entry["wav_path"]
            utt_id = entry["utt_id"]

            if utt_id in processed_ids:
                pbar.update(1)
                continue

            try:
                # Force Hindi transcription explicitly
                output = model.transcribe(wav_path, language="hi")
                hyp_text = output["text"].strip()

                if phonemizer and hyp_text:
                    try:
                        hyp_phon = phonemizer.phonemize([hyp_text], strip=True)[0]
                    except Exception as e:
                        print(f"Phonemizer error [{lang}] {utt_id}: {e}")
                        hyp_phon = ""
                else:
                    hyp_phon = ""

                results.append({
                    "utt_id": utt_id,
                    "hyp_text": hyp_text,
                    "hyp_phon": hyp_phon
                })

                with open(out_path, "a", encoding="utf-8") as fout:
                    fout.write(json.dumps(results[-1], ensure_ascii=False) + "\n")

            except Exception as e:
                print(f"Error processing {utt_id} [{lang}]: {e}")
                continue

            pbar.update(1)

    print(f"✅ Finished {lang} chunk {chunk_id+1}/{total_chunks}. Wrote {len(results)} hypotheses to {out_path}")

    if log_path:
        log_file.close()

    # Free memory
    del model
    gc.collect()
    if device == "cuda":
        torch.cuda.empty_cache()

def main():
    parser = argparse.ArgumentParser(description="Run Whisper inference on audio")
    parser.add_argument("--manifest", type=str, default=None,
                        help="Path to manifest JSONL file")
    parser.add_argument("--out", type=str, default=None,
                        help="Output JSONL file for hypotheses")
    parser.add_argument("--model", type=str, default=None,
                        help="Whisper model size override")
    parser.add_argument("--limit", type=int, default=None,
                        help="Limit utterances")
    parser.add_argument("--log", type=str, default=None,
                        help="Log file")
    parser.add_argument("--no-phonemizer", action="store_true",
                        help="Disable phoneme conversion")
    parser.add_argument("--config", type=str, default=None,
                        help="Optional JSON config file")
    parser.add_argument("--lang", type=str, default=None,
                        help="Single language code")
    parser.add_argument("--batch-size", type=int, default=200,
                        help="Utterances per batch")
    parser.add_argument("--chunks", type=int, default=1,
                        help="Split manifest into N chunks for parallel workers")
    args = parser.parse_args()

    config = load_config(args.config)
    manifest_path = args.manifest or config.get("manifest", None)
    out_path = args.out or config.get("out", None)
    model_size = args.model or config.get("model", None)
    limit = args.limit or config.get("limit", None)
    log_path = args.log or config.get("log", None)
    no_phonemizer = args.no_phonemizer or config.get("no_phonemizer", False)
    lang = args.lang or config.get("lang", None)
    batch_size = args.batch_size or config.get("batch_size", 200)
    chunks = args.chunks or 1

    has_gpu = torch.cuda.is_available()
    default_device = "cuda" if has_gpu else "cpu"
    model_size = model_size if model_size else ("base" if has_gpu else "tiny")

    if not lang:
        lang = "hi"
    out_path = out_path if out_path else f"results/{lang}_whisper.jsonl"
    manifest_path = manifest_path if manifest_path else f"data/manifests/{lang}/noisy.jsonl"

    if chunks > 1:
        tasks = []
        for i in range(chunks):
            chunk_out = out_path.replace(".jsonl", f"_chunk{i+1}.jsonl")
            tasks.append((lang, manifest_path, chunk_out,
                          model_size, limit, log_path, no_phonemizer,
                          default_device, batch_size, i, chunks))
        with Pool(processes=chunks) as pool:
            pool.map(process_language, tasks)
    else:
        process_language((lang, manifest_path, out_path, model_size, limit,
                          log_path, no_phonemizer, default_device, batch_size, 0, 1))

if __name__ == "__main__":
    main()
