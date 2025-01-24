"""
▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
█░░░░░░░░▀█▄▀▄▀██████░▀█▄▀▄▀██████
░░░░ ░░░░░░░▀█▄█▄███▀░░░ ▀█▄█▄███

This script generates synthetic DNA sequences for testing, simulation, or educational purposes.
It creates one original sequence and a series of perturbed versions to simulate mutations or
experimental variations. The perturbed sequences are stored in a directory named `SYNTHETIC_DATA`.

### Features
1. **DNA Sequence Generation**:
   - Generates a random DNA sequence of a specified length using the nucleotides A, C, T, and G.

2. **Perturbation**:
   - Introduces controlled randomness into the sequence, either by removing or replacing nucleotides
     with a given probability.

3. **Storage**:
   - Saves the original sequence and its perturbed variants as text files in a dedicated folder.
     The original sequence is saved as `000.txt`, and perturbed sequences follow the format `001.txt`, `002.txt`, etc.

### Approach
- The script uses Python's `random` module to generate and modify DNA sequences.
- Perturbations are applied at the nucleotide level, either removing or substituting letters based on a probability.
- Outputs are neatly organized in a folder for further analysis or experimentation.

### Parameters
- `SEQUENCE_LENGTH`: Length of the original DNA sequence.
- `NUM_PERTURBATIONS`: Number of perturbed sequences to generate.
- `PERTURBATION_PROBABILITY`: Probability for each nucleotide to be perturbed.

### Example Usage
Run the script directly to generate an original sequence of 100,000 nucleotides, perturb it 26 times
with a 5% mutation probability, and save all sequences in the `SYNTHETIC_DATA` folder.
"""

import os
import random

def generate_dna_sequence(length):
    """Generate a random DNA sequence of given length."""
    return ''.join(random.choice("ACTG") for _ in range(length))

def perturb_sequence(sequence, probability):
    """Perturb a DNA sequence by changing or removing letters with a given probability."""
    perturbed = []
    for char in sequence:
        if random.random() < probability:
            if random.random() < 0.25:  # 50% chance to delete
                continue
            else:  # 50% chance to replace
                perturbed.append(random.choice("ACTG".replace(char, "")))
        else:
            perturbed.append(char)
    return ''.join(perturbed)

def save_sequences(folder, base_sequence, num_perturbations, perturb_prob):
    """Save the original and perturbed sequences in a specified folder."""
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Save the original sequence
    with open(os.path.join(folder, "000.txt"), "w") as f:
        f.write(base_sequence)

    # Save perturbed sequences
    for i in range(1, num_perturbations + 1):
        perturbed_sequence = perturb_sequence(base_sequence, perturb_prob)
        filename = f"{i:03}.txt"
        with open(os.path.join(folder, filename), "w") as f:
            f.write(perturbed_sequence)

if __name__ == "__main__":
    # Parameters
    SEQUENCE_LENGTH = 100000  # Length of the original DNA sequence
    NUM_PERTURBATIONS = 26  # Number of perturbed sequences to generate
    PERTURBATION_PROBABILITY = 0.05  # 5% probability to change each letter

    # Generate and save sequences
    original_sequence = generate_dna_sequence(SEQUENCE_LENGTH)
    save_sequences("SYNTHETIC_DATA", original_sequence, NUM_PERTURBATIONS, PERTURBATION_PROBABILITY)
    print("DNA sequences generated and saved in the SYNTHETIC_DATA folder.")
