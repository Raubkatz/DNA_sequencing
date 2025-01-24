"""
▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
█░░░░░░░░▀█▄▀▄▀██████░▀█▄▀▄▀██████
░░░░ ░░░░░░░▀█▄█▄███▀░░░ ▀█▄█▄███

This script performs clustering and analysis of DNA sequences based on their similarity.
It processes sequence data, calculates pairwise distances, clusters similar sequences,
and generates a detailed report in both human-readable and JSON formats.

### Features
1. **Distance Calculation**:
   - Measures similarity between sequences using a weighted combination of letter differences and positional differences.

2. **Clustering**:
   - Groups sequences into clusters based on a user-defined distance threshold.
   - Provides detailed progress tracking for clustering operations.

3. **Cluster Analysis**:
   - Computes average distances within clusters.
   - Saves cluster details, including the number of entries and the sequences in each cluster, as a text report and a JSON file.

### Approach
- Each sequence is compared to others to calculate pairwise distances.
- Sequences are grouped into clusters if their distance is below a threshold.
- Results are saved for further downstream analysis or visualization.

### Parameters
- `INPUT_FOLDER`: Path to the folder containing analyzed sequence JSON files.
- `OUTPUT_FILE`: Path to save the clustering results.
- `DISTANCE_THRESHOLD`: Maximum distance between sequences to consider them part of the same cluster.
- `LETTER_WEIGHT`: Weight for letter differences in distance calculation.
- `POSITION_WEIGHT`: Weight for positional differences in distance calculation.

### Example Usage
Run the script to cluster sequences stored in `ANALYZED_DATA` with a distance threshold of 21.
Results will be saved in the `CLUSTERED_DATA` folder as `clusters.txt` and `clusters.json`.
"""
import os
import json
from itertools import combinations
from collections import defaultdict
import time

def calculate_distance(seq1, seq2, pos1, pos2, letter_weight=2, position_weight=1):
    """
    Calculate the distance between two sequences based on differences in letters
    and their respective positions.

    Parameters:
        seq1 (str): First sequence.
        seq2 (str): Second sequence.
        pos1 (int): Starting position of the first sequence.
        pos2 (int): Starting position of the second sequence.
        letter_weight (int): Weight for letter differences.
        position_weight (int): Weight for positional differences.

    Returns:
        int: Calculated distance.
    """
    letter_diff = sum(1 for a, b in zip(seq1, seq2) if a != b) + abs(len(seq1) - len(seq2))
    position_diff = abs(pos1 - pos2)
    return letter_weight * letter_diff + position_weight * position_diff

def cluster_sequences(recordings, distance_threshold, letter_weight=2, position_weight=1):
    """
    Cluster sequences based on their distances.

    Parameters:
        recordings (list): List of dictionaries with sequence data.
        distance_threshold (int): Threshold for clustering.
        letter_weight (int): Weight for letter differences.
        position_weight (int): Weight for positional differences.

    Returns:
        dict: Clusters with their entries.
    """
    print("Starting clustering process...")
    clusters = []
    unclustered = set(range(len(recordings)))

    total_pairs = len(recordings) * (len(recordings) - 1) // 2
    print(f"Total pairs to test: {total_pairs}")

    iteration = 1
    total_checked = 0
    while unclustered:
        print(f"Iteration {iteration}: {len(unclustered)} sequences remaining to cluster.")
        start_time = time.time()
        current_cluster = []
        to_check = [unclustered.pop()]  # Start with an unclustered point

        while to_check:
            idx = to_check.pop()
            current_cluster.append(idx)
            to_remove = set()

            for other_idx in unclustered:
                dist = calculate_distance(
                    recordings[idx]['sequence'],
                    recordings[other_idx]['sequence'],
                    recordings[idx]['start_position'],
                    recordings[other_idx]['start_position'],
                    letter_weight,
                    position_weight
                )
                total_checked += 1
                if total_checked % 100 == 0:
                    print(f"Checked {total_checked}/{total_pairs} pairs... ({(total_checked / total_pairs) * 100:.2f}%)")

                if dist <= distance_threshold:
                    to_check.append(other_idx)
                    to_remove.add(other_idx)

            unclustered -= to_remove

        clusters.append(current_cluster)
        iteration_time = time.time() - start_time
        print(f"Iteration {iteration} complete. Cluster size: {len(current_cluster)}. Time taken: {iteration_time:.2f}s")
        iteration += 1

    print("Clustering process complete.")
    return clusters

def analyze_clusters(clusters, recordings, output_file):
    """
    Analyze and save clusters in a human-readable format.

    Parameters:
        clusters (list): Clusters with indices.
        recordings (list): List of recording dictionaries.
        output_file (str): Path to save the cluster analysis.
    """
    print("Analyzing clusters...")
    cluster_data = []
    for i, cluster in enumerate(clusters, start=1):
        print(f"Analyzing Cluster {i} with {len(cluster)} entries...")
        cluster_sequences = [recordings[idx] for idx in cluster]
        avg_distance = sum(
            calculate_distance(
                rec1['sequence'],
                rec2['sequence'],
                rec1['start_position'],
                rec2['start_position']
            ) for rec1, rec2 in combinations(cluster_sequences, 2)
        ) / max(1, len(cluster) * (len(cluster) - 1) / 2)

        cluster_data.append({
            "cluster_id": i,
            "num_entries": len(cluster),
            "avg_distance": avg_distance,
            "entries": [
                {
                    "sequence_id": entry['sequence_id'],
                    "start_position": entry['start_position'],
                    "sequence": entry['sequence']
                } for entry in cluster_sequences
            ]
        })

    cluster_data.sort(key=lambda x: x['num_entries'], reverse=True)

    with open(output_file, "w") as f:
        for cluster in cluster_data:
            f.write(f"Cluster {cluster['cluster_id']}\n")
            f.write(f"Number of Entries: {cluster['num_entries']}\n")
            f.write(f"Average Distance: {cluster['avg_distance']:.2f}\n")
            f.write("Entries:\n")
            for entry in cluster['entries']:
                f.write(f"  Sequence ID: {entry['sequence_id']}, Start: {entry['start_position']}, Sequence: {entry['sequence']}\n")
            f.write("\n")

    # Save as JSON
    json_output_file = output_file.replace('.txt', '.json')
    with open(json_output_file, "w") as json_file:
        json.dump(cluster_data, json_file, indent=4)

    print("Analysis complete. Results saved.")

if __name__ == "__main__":
    print("Program starting...")

    INPUT_FOLDER = "ANALYZED_DATA"
    OUTPUT_FILE = "CLUSTERED_DATA/clusters.txt"
    DISTANCE_THRESHOLD = 21 #21good
    LETTER_WEIGHT = 4
    POSITION_WEIGHT = 1

    if not os.path.exists("CLUSTERED_DATA"):
        os.makedirs("CLUSTERED_DATA")

    print("Loading recordings...")
    all_recordings = []
    for file in os.listdir(INPUT_FOLDER):
        if file.endswith(".json"):
            with open(os.path.join(INPUT_FOLDER, file), "r") as f:
                for recording in json.load(f):
                    recording['sequence_id'] = file.split(".")[0]  # Add sequence ID
                    all_recordings.append(recording)

    print(f"Loaded {len(all_recordings)} recordings.")

    # Perform clustering
    start_time = time.time()
    clusters = cluster_sequences(all_recordings, DISTANCE_THRESHOLD, LETTER_WEIGHT, POSITION_WEIGHT)
    clustering_time = time.time() - start_time
    print(f"Clustering completed in {clustering_time:.2f}s.")

    # Save clusters
    analyze_clusters(clusters, all_recordings, OUTPUT_FILE)
    print("Program finished. Results saved in CLUSTERED_DATA folder.")
