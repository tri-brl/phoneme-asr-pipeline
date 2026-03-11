#!/usr/bin/env python3
import argparse
import json
import os

def split_manifest(infile, outdir, chunk_size):
    # Read all lines from the input manifest
    with open(infile, "r", encoding="utf-8") as f:
        lines = f.readlines()

    total = len(lines)
    os.makedirs(outdir, exist_ok=True)

    # Calculate number of chunks
    chunks = (total + chunk_size - 1) // chunk_size
    print(f"Splitting {total} lines into {chunks} chunks of ~{chunk_size} each")

    for i in range(chunks):
        start = i * chunk_size
        end = min((i + 1) * chunk_size, total)
        chunk_lines = lines[start:end]

        outfile = os.path.join(outdir, f"chunk{i+1}.jsonl")
        with open(outfile, "w", encoding="utf-8") as fout:
            fout.writelines(chunk_lines)

        print(f"Wrote {len(chunk_lines)} lines to {outfile}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Split a JSONL manifest into smaller chunks")
    parser.add_argument("--infile", required=True, help="Input manifest JSONL")
    parser.add_argument("--outdir", required=True, help="Output directory for chunks")
    parser.add_argument("--chunk-size", type=int, default=2000, help="Number of lines per chunk")
    args = parser.parse_args()

    split_manifest(args.infile, args.outdir, args.chunk_size)
