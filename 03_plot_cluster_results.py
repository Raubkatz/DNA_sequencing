import os
import matplotlib.pyplot as plt
import seaborn as sns
import json
import numpy as np

def plot_clusters(cluster_file, output_folder, num_clusters=10, color_map=None):
    """
    Plot the sequences in clusters as color-coded visualizations.

    Parameters:
        cluster_file (str): Path to the cluster analysis JSON file.
        output_folder (str): Directory to save the plots.
        num_clusters (int): Number of clusters to visualize.
        color_map (dict): Custom mapping of letters to hexadecimal colors.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    with open(cluster_file, "r") as f:
        cluster_data = json.load(f)

    # Use default colors if no color map is provided
    if color_map is None:
        default_colors = sns.color_palette("hsv", 26)  # One color per letter
        color_map = {chr(65 + i): f"#{int(c[0]*255):02x}{int(c[1]*255):02x}{int(c[2]*255):02x}" for i, c in enumerate(default_colors)}

    for cluster in cluster_data[:num_clusters]:
        cluster_id = cluster['cluster_id']
        entries = cluster['entries']

        fig, ax = plt.subplots(figsize=(10, 0.5 * len(entries)))

        # Determine the minimum starting position to adjust the x-axis
        min_start_pos = min(entry['start_position'] for entry in entries)

        for i, entry in enumerate(entries):
            sequence = entry['sequence']
            start_pos = entry['start_position'] - min_start_pos  # Adjust start position
            sequence_id = entry['sequence_id']

            # Create a color bar for the sequence
            for j, letter in enumerate(sequence):
                color = color_map.get(letter.upper(), "#000000")  # Default to black if not in color map
                ax.barh(i, 1, left=start_pos + j, color=color, edgecolor='none', height=0.8)

                # Add the letter inside the colored box
                ax.text(start_pos + j + 0.5, i, letter, ha='center', va='center', fontsize=8, color='white')

            # Annotate sequence ID and start position
            ax.text(-5, i, f"{sequence_id} (Start: {entry['start_position']})", ha='right', va='center', fontsize=8)

        ax.set_title(f"Cluster {cluster_id}: {len(entries)} entries")
        ax.set_yticks(range(len(entries)))
        ax.set_yticklabels([f"{entry['sequence_id']}" for entry in entries], fontsize=8)
        ax.set_xlabel("Position")
        ax.set_xlim(0, max(entry['start_position'] + len(entry['sequence']) - min_start_pos for entry in entries) + 10)

        plt.tight_layout()

        # Save the plot
        plot_file_base = os.path.join(output_folder, f"cluster_{cluster_id}")
        plt.savefig(f"{plot_file_base}.png", format="png", dpi=300)
        plt.savefig(f"{plot_file_base}.eps", format="eps", dpi=300)
        plt.close()

if __name__ == "__main__":
    CLUSTER_FILE = "CLUSTERED_DATA/clusters.json"
    OUTPUT_FOLDER = "CLUSTER_PLOTS"
    NUM_CLUSTERS = 10

    # Custom color map for letters (optional)
    CUSTOM_COLOR_MAP = {
        "A": "#FF5733",
        "C": "#33FF57",
        "G": "#3357FF",
        "T": "#FFFF33",
        "N": "#999999"  # Example for 'N' or ambiguous bases
    }

    plot_clusters(CLUSTER_FILE, OUTPUT_FOLDER, NUM_CLUSTERS, CUSTOM_COLOR_MAP)
    print(f"Plots saved in {OUTPUT_FOLDER}")
