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
