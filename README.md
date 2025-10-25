# Waxman Lab snRNA-seq SNP Calling Pipeline

This pipeline performs processing of snRNA-seq data to identify unknown single nucleotide polymorphisms (SNPs), including alignment, quality control, read filtering, variant calling, and normalization. 

## Table of Contents
1. Features
2. Requirements
3. Installation
4. Usage
5. Pipeline Structure
6. Configuration
7. Input and Output
8. Best Practices
9. Contributing
10. License

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
  - Modules already installed on BU Shared Computing cluster (SCC)
 
  ## Installation
  - Clone this repository in the SCC
  - git clone
  ''' https://github.com/JackSherry6/Waxman-Lab-snRNA-seq-SNP-Calling-Pipeline.git
