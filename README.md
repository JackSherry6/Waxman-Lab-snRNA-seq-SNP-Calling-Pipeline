# Waxman Lab snRNA-seq SNP Calling Pipeline

This pipeline performs processing of snRNA-seq data to identify unknown single nucleotide polymorphisms (SNPs), including alignment, quality control, read filtering, variant calling, and normalization. 

## Table of Contents
1. Features
2. Requirements
3. Installation
4. Usage
5. Configuration
6. Input and Output
7. Contributing
8. License

## Features
- Modular Nextflow pipeline with clearly separated steps:
  - Read preprocessing and quality control
  - Alignment to reference genome
  - Duplicate marking and filtering
  - SNP calling and variant filtering
  - Normalization and annotation
  - Supports BU HPC cluster execution.
- Docker/Singularity container support for reproducibility.
- Automatic logging and error handling.
- Scalable to large snRNA-seq datasets.

## Requirements
- Create a conda environment with nextflow (ex. nextflow_latest)
- Modules already installed on BU Shared Computing cluster (SCC)
 
## Installation
  - Clone this repository in the SCC
  - git clone 'https://github.com/JackSherry6/Waxman-Lab-snRNA-seq-SNP-Calling-Pipeline.git'
 
## Usage
Basic execution: 
module load conda
conda activate nextflow_latest (or whatever you named your conda environment with nextflow)
nextflow run main.nf -profile conda,cluster

## Configuration
- Lines for configuration in config file:
  - Lines here:

## Input and Output
- Input:
  - Folder of cram/crai files (specify location in configs)
  - Reference fasta file (specify location in configs)
  - Reference fasta index file (specify location in configs)
  - Reference fasta dictionary file (specify location in configs)
- Output:
  - See results folder after program runs

## Contributing 
- Email me at jgsherry@bu.edu for additional information or contributing information
