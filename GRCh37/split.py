#!/usr/bin/env python

"""
Splits genomic.fna into chromosomes/chr1.fna, chromosomes/chr2.fna, etc.

Relies on chromosomes.yaml to specify which FASTA sequences to extract.
"""

from Bio import SeqIO
from pathlib import Path

import yaml
import argparse

def main(*, genome_fasta, chromosomes_meta, output_dir):
    output_dir = Path(output_dir)

    with open(chromosomes_meta) as f:
        chromosome_metadata = yaml.safe_load(f)

    chromosome_metadata = {
        i["id"]: i
        for i in chromosome_metadata
    }

    output_dir.mkdir(parents=True, exist_ok=True)

    with open(genome_fasta) as f:
        for record in SeqIO.parse(f, "fasta"):
            if record.id in chromosome_metadata:
                chromosome_name = chromosome_metadata[record.id]["chr"]
                out_fname = output_dir / f"chr{chromosome_name}.fna"
                print(f"Writing {record.id} to {out_fname}...")
                SeqIO.write([record], out_fname, "fasta")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--genome")
    parser.add_argument("--chromosomes")
    parser.add_argument("--output-dir")

    args = parser.parse_args()

    main(genome_fasta=args.genome,
         chromosomes_meta=args.chromosomes,
         output_dir=args.output_dir
         )
