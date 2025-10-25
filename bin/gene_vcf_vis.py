#!/usr/bin/env python3
"""
Robust per-gene VCF visualization.
Generates:
- Heatmap of genotypes
- Allele frequency plot
- Lollipop plot
- Placeholder PNG if no plots can be generated

Usage:
    python gene_vcf_vis.py --vcf_files file1.vcf file2.vcf ... --out_dir ./visualizations
"""

import os
import argparse
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import allel
import plotly.graph_objects as go

# ----------------------------
# Functions
# ----------------------------

def load_vcf(vcf_file):
    """Load a VCF file using scikit-allel with safety checks."""
    try:
        callset = allel.read_vcf(
            vcf_file,
            fields=['variants/CHROM', 'variants/POS', 'variants/REF', 'variants/ALT', 'calldata/GT']
        )
    except Exception as e:
        print(f"Failed to read VCF {vcf_file}: {e}")
        return None

    if callset is None or 'calldata/GT' not in callset or callset['calldata/GT'] is None:
        print(f"Skipping {vcf_file}: no GT field or empty VCF")
        return None

    return callset

def vcf_to_matrix(callset):
    """Convert VCF callset to genotype matrix (0=hom ref,1=het,2=hom alt)"""
    gt = allel.GenotypeArray(callset['calldata/GT'])
    geno_matrix = gt.to_n_alt()  # Number of ALT alleles
    samples = [f"S{i+1}" for i in range(geno_matrix.shape[1])]
    variants = [f"{callset['variants/CHROM'][i]}:{callset['variants/POS'][i]}" for i in range(geno_matrix.shape[0])]
    df = pd.DataFrame(geno_matrix.T, index=samples, columns=variants)
    return df

def plot_heatmap(df, gene_name, out_dir):
    if df.shape[1] == 0:
        return False
    plt.figure(figsize=(12, max(4, 0.3*df.shape[1])))
    sns.heatmap(df, cmap="viridis", cbar_kws={'label': 'ALT allele count'})
    plt.title(f"{gene_name} Genotype Heatmap")
    plt.xlabel("Variants")
    plt.ylabel("Samples")
    plt.tight_layout()
    os.makedirs(out_dir, exist_ok=True)
    plt.savefig(os.path.join(out_dir, f"{gene_name}_heatmap.png"))
    plt.close()
    return True

def plot_allele_freq(callset, gene_name, out_dir):
    gt = allel.GenotypeArray(callset['calldata/GT'])
    ac = gt.to_allele_counts()  # variants x alleles
    af = ac.to_frequencies()

    if af.shape[1] < 2:
        print(f"Skipping allele frequency plot for {gene_name}: no ALT alleles present.")
        return False

    pos = callset['variants/POS']
    plt.figure(figsize=(10,4))
    plt.bar(pos, af[:,1], width=1, color='skyblue', edgecolor='black')
    plt.title(f"{gene_name} Variant Allele Frequencies")
    plt.xlabel("Position")
    plt.ylabel("ALT Allele Frequency")
    plt.tight_layout()
    os.makedirs(out_dir, exist_ok=True)
    plt.savefig(os.path.join(out_dir, f"{gene_name}_allele_freq.png"))
    plt.close()
    return True

def plot_lollipop(callset, gene_name, out_dir):
    alt_counts = allel.GenotypeArray(callset['calldata/GT']).to_n_alt().sum(axis=1)
    if alt_counts.sum() == 0:
        print(f"Skipping lollipop plot for {gene_name}: no ALT alleles present.")
        return False

    pos = callset['variants/POS']
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=pos, y=alt_counts,
        mode='markers+lines',
        marker=dict(size=10, color='red'),
        line=dict(color='black', width=1)
    ))
    fig.update_layout(title=f"{gene_name} Lollipop Plot",
                      xaxis_title="Position",
                      yaxis_title="Number of ALT alleles",
                      showlegend=False)
    os.makedirs(out_dir, exist_ok=True)
    fig.write_html(os.path.join(out_dir, f"{gene_name}_lollipop.html"))
    return True

def create_placeholder_plot(gene_name, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    plt.figure(figsize=(4,2))
    plt.text(0.5, 0.5, f"No variants for {gene_name}", ha='center', va='center')
    plt.axis('off')
    plt.savefig(os.path.join(out_dir, f"{gene_name}_placeholder.png"))
    plt.close()

def process_gene_vcf(vcf_file, out_dir):
    gene_name = os.path.basename(vcf_file).replace(".vcf","")
    print(f"Processing {gene_name}")

    callset = load_vcf(vcf_file)
    if callset is None:
        create_placeholder_plot(gene_name, out_dir)
        return

    # Skip VCFs with 0 variants
    if callset['calldata/GT'].size == 0:
        print(f"Skipping {gene_name}: no variants found.")
        create_placeholder_plot(gene_name, out_dir)
        return

    plots_created = 0
    if plot_heatmap(vcf_to_matrix(callset), gene_name, out_dir):
        plots_created += 1
    if plot_allele_freq(callset, gene_name, out_dir):
        plots_created += 1
    if plot_lollipop(callset, gene_name, out_dir):
        plots_created += 1

    if plots_created == 0:
        create_placeholder_plot(gene_name, out_dir)

    print(f"Finished {gene_name}")

# ----------------------------
# Main CLI
# ----------------------------
def main():
    parser = argparse.ArgumentParser(description="Per-gene VCF visualization workflow")
    parser.add_argument("--vcf_files", nargs='+', required=True, help="List of VCF files to process")
    parser.add_argument("--out_dir", required=True, help="Output directory")
    args = parser.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)

    for vcf_file in args.vcf_files:
        process_gene_vcf(vcf_file, args.out_dir)

if __name__ == "__main__":
    main()
