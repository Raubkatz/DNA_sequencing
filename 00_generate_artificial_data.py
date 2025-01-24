"""
▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
█░░░░░░░░▀█▄▀▄▀██████░▀█▄▀▄▀██████
░░░░ ░░░░░░░▀█▄█▄███▀░░░ ▀█▄█▄███
This script generates a synthetic DNA sequence and perturbs it to produce multiple sequences saved in a directory named SYNTHETIC_DATA.
Original sequence: file 000.txt
Perturbed sequences: 001.txt, 002.txt, and so on.
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
