# Synthetic DNA Sequence Analysis

Repository for the computational analysis and clustering of synthetic DNA sequences generated, dissected, and clustered based on biological motifs.

## Author: Dr. techn. Sebastian Raubitzek MSc. BSc.

## Overview

This repository provides a collection of Python scripts for generating synthetic DNA sequences, analyzing sequence motifs, and clustering recordings based on defined distance thresholds. The project is structured to enable efficient processing of DNA-like data and includes tools for generating synthetic datasets, dissecting sequences into meaningful motifs, and clustering recordings for downstream analysis.

The primary components of this project are:

1. **Synthetic Data Generation**: A script that generates synthetic DNA sequences and creates perturbed versions.
2. **Sequence Dissection**: A script that identifies motifs within the generated sequences, categorizing them by start and stop codons.
3. **Clustering**: A script that clusters the dissected motifs based on their sequence similarity and positional proximity.

## Repository Structure

├── README.md

├── 00_generate_artificial_data.py

├── 01_dissect_sequences.py

├── 02_cluster_recordings.py

├── SYNTHETIC_DATA 

│ └── ... contains generated synthetic sequences 

├── ANALYZED_DATA 

│ └── ... contains dissected sequence data 

├── CLUSTERED_DATA 

└── ... contains clustering results


## Script Descriptions

### 1. **00_generate_artificial_data.py**
   - **Purpose**: Generates a synthetic DNA sequence of configurable length and perturbs it to create variations. Each variation is saved in a folder for downstream processing.
   - **Output**: Synthetic sequences saved as text files in the `SYNTHETIC_DATA` folder.

### 2. **01_dissect_sequences.py**
   - **Purpose**: Dissects each sequence into triads (3-letter groups) and identifies motifs starting with specific codons (e.g., `ATG`, `ATA`) and ending with stop codons (`TGA`, `TAG`, `TAA`). Records sequences between start and stop codons along with their positions.
   - **Output**: JSON files containing recordings of motifs, saved in the `ANALYZED_DATA` folder.

### 3. **02_cluster_recordings.py**
   - **Purpose**: Clusters the dissected motifs based on their sequence similarity and positional proximity. Distance is calculated using a weighted combination of letter differences and positional offsets.
   - **Output**: Clustering results saved as a human-readable text file and a JSON file in the `CLUSTERED_DATA` folder. The text file includes detailed cluster information sorted by the number of entries.

## Prerequisites

Ensure you have the following dependencies installed:

- Python 3.6 or higher
- numpy
- pandas
- json

## Usage

1. **Generate Synthetic Data**:
   Run `00_generate_artificial_data.py` to create synthetic DNA sequences with perturbations.

2. **Dissect Sequences**:
   Use `01_dissect_sequences.py` to identify and record motifs within the generated sequences.

3. **Cluster Recordings**:
   Execute `02_cluster_recordings.py` to cluster motifs based on sequence similarity and positional proximity.

## Results

All results, including synthetic sequences, dissected motifs, and clustering outputs, are saved in appropriately named folders for easy access and further analysis.

- `SYNTHETIC_DATA`: Contains the generated synthetic sequences.
- `ANALYZED_DATA`: Contains JSON files with dissected motif recordings.
- `CLUSTERED_DATA`: Contains clustering results, including human-readable text and JSON files.

## License

This project is licensed under the terms of the [Creative Commons Attribution 4.0 International License (CC BY 4.0)](http://creativecommons.org/licenses/by/4.0/).
