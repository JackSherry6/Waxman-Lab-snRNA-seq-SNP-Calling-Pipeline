#!/usr/bin/env python3
import os
import re
import sys

def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]

# --- Command-line arguments ---
# Usage: python merge.py file1.vcf file2.vcf ... fileN.vcf output_file
if len(sys.argv) < 3:
    print("Usage: python merge.py <file1> <file2> ... <output_file>")
    sys.exit(1)

*input_files, output_file = sys.argv[1:]

# --- Merge logic ---
with open(output_file, "w") as fout:
    for filename in sorted(input_files, key=natural_sort_key):
        if not filename.endswith(".vcf"):
            continue

        with open(filename, "r") as fin:
            start_printing = False
            for line in fin:
                if line.startswith("#CHROM"):
                    fout.write(f"\n# From file: {filename}\n")
                    start_printing = True
                    continue
                if start_printing:
                    fout.write(line)
