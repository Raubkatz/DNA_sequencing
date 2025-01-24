"""
▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
█░░░░░░░░▀█▄▀▄▀██████░▀█▄▀▄▀██████
░░░░ ░░░░░░░▀█▄█▄███▀░░░ ▀█▄█▄███

This script analyzes DNA sequences to identify and extract sub-sequences defined by specific start
and stop triads. It processes all sequence files in a specified input folder, searches for the defined
start-stop triad patterns, and outputs the results as JSON files in a designated output folder.

### Features
1. **Start-Stop Triad Analysis**:
   - Identifies sub-sequences that start with any of the given start triads and end with one of the stop triads.

2. **Output as JSON**:
   - Each identified sub-sequence is recorded with its start position and the extracted sequence in a JSON file.

3. **Batch Processing**:
   - Processes all `.txt` sequence files in the input folder, ensuring scalability for large datasets.

### Approach
- Iterates through sequences in steps of three (triads) to mimic codon-based reading in genetics.
- Starts recording a sub-sequence upon encountering a start triad and stops when a stop triad is found.
- Stores results as a structured JSON file for easy access and downstream analysis.

### Parameters
- `folder`: Path to the folder containing `.txt` sequence files.
- `start_triads`: List of triads that mark the beginning of a sub-sequence.
- `stop_triads`: List of triads that mark the end of a sub-sequence.
- `output_folder`: Path to the folder where results will be saved.

### Example Usage
Run the script to analyze sequences in the `SYNTHETIC_DATA` folder, using `ATG` and `ATA` as start triads,
and `TGA`, `TAG`, `TAA` as stop triads. The results will be saved as JSON files in the `ANALYZED_DATA` folder.
"""

import os
import json

def analyze_sequences(folder, start_triads, stop_triads, output_folder):
    """
    Analyze sequences in the given folder, finding start-stop sub-sequences.

    Parameters:
        folder (str): Path to the folder containing sequences.
        start_triads (list): List of start triads to look for.
        stop_triads (list): List of stop triads to look for.
        output_folder (str): Folder to save the resulting dictionaries.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    sequence_files = [f for f in os.listdir(folder) if f.endswith(".txt")]
    for seq_file in sequence_files:
        with open(os.path.join(folder, seq_file), "r") as file:
            sequence = file.read().strip()

        recordings = []
        is_recording = False
        current_recording = ""
        start_position = None

        for i in range(0, len(sequence), 3):
            triad = sequence[i:i+3]

            if len(triad) < 3:  # Skip incomplete triads
                continue

            if is_recording:
                current_recording += triad
                if triad in stop_triads:
                    is_recording = False
                    recordings.append({
                        "start_position": start_position,
                        "sequence": current_recording
                    })
                    current_recording = ""
                    start_position = None
            elif triad in start_triads:
                is_recording = True
                start_position = i
                current_recording += triad

        output_file = os.path.join(output_folder, f"{seq_file.split('.')[0]}_analysis.json")
        with open(output_file, "w") as out_file:
            json.dump(recordings, out_file, indent=4)

if __name__ == "__main__":
    # Define start and stop triads
    START_TRIADS = ["ATG", "ATA"]
    STOP_TRIADS = ["TGA", "TAG", "TAA"]

    # Folder paths
    INPUT_FOLDER = "SYNTHETIC_DATA"
    OUTPUT_FOLDER = "ANALYZED_DATA"

    # Analyze sequences
    analyze_sequences(INPUT_FOLDER, START_TRIADS, STOP_TRIADS, OUTPUT_FOLDER)
    print("Sequence analysis complete. Results saved in the ANALYZED_DATA folder.")
