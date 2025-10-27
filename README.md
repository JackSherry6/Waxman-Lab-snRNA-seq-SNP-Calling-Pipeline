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
- ```module load conda```
- ```conda activate <name_of_your_nexflow_conda_env>```
- Set params.samples to the location of the folder containing your files
- Set params.ref_genome, ref_index, ref_dict to their respective file locations
- Modify your group_labels.csv file according to your sample names and groups (use the same format as my example or modify my example)
- ```nextflow run main.nf -profile conda,cluster``` (should always run on the cluster, if you have no choice, then use conda,local)

## Configuration
- Lines for configuration in config file:
  - set samples, ref_genome, ref_index, ref_dict to locations
  - Set queueSize to appropriate size based on sample size (I use a quarter of the number of samples)
  - Optional: set resume to true in order to save progress during runs

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
