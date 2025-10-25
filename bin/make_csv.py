#!/usr/bin/env python3
import csv
import sys

input_file = sys.argv[1]  # merged VCF
output_csv = sys.argv[2]

csv_columns = ['Sample', 'CHROM', 'POS', 'REF', 'ALT', 'QUAL', 'FILTER', 'AF', 'DP']

with open(input_file, 'r') as f, open(output_csv, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
    writer.writeheader()

    current_sample = None

    for line in f:
        line = line.strip()
        if not line:
            continue

        # Detect sample header
        if line.startswith('# From file:'):
            file_path = line.split(':', 1)[1].strip()
            current_sample = file_path.split('/')[-1].replace('_filtered.vcf', '')
            continue

        # Skip other headers starting with #
        if line.startswith('#'):
            continue

        # Parse VCF line safely
        fields = line.split('\t')
        if len(fields) < 8:
            continue  # skip malformed lines

        chrom = fields[0]
        pos = fields[1]
        ref = fields[3]
        alt = fields[4]
        qual = fields[5]
        filter_status = fields[6]
        info = fields[7]

        # Parse INFO field safely
        info_dict = dict()
        for item in info.split(';'):
            if '=' in item:
                key, value = item.split('=', 1)
                info_dict[key] = value

        af = info_dict.get('AF', '')
        dp = info_dict.get('DP', '')

        if not current_sample:
            current_sample = 'Unknown'

        writer.writerow({
            'Sample': current_sample,
            'CHROM': chrom,
            'POS': pos,
            'REF': ref,
            'ALT': alt,
            'QUAL': qual,
            'FILTER': filter_status,
            'AF': af,
            'DP': dp
        })
