import argparse
import torch
import esm
import numpy as np
import biotite.structure.io as bsio
import matplotlib.pyplot as plt
import json
import os
from Bio import SeqIO  # BioPython for reading FASTA files

# Function to parse command-line arguments
def parse_arguments():
    parser = argparse.ArgumentParser(description="Run ESMFold on a FASTA file and save results.")
    parser.add_argument("fasta_file", type=str, help="Path to the input FASTA file")
    parser.add_argument(
        "-o", "--output_dir", type=str, default="output", help="Directory to save output files"
    )
    return parser.parse_args()

# Main function
def main():
    # Parse command-line arguments
    args = parse_arguments()
    fasta_file = args.fasta_file
    output_dir = args.output_dir

    # Load the ESMFold model
    model = esm.pretrained.esmfold_v1()
    model = model.eval().cuda()

    # Optionally, uncomment to set a chunk size for axial attention to reduce memory usage
    model.set_chunk_size(512)

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Process each sequence in the FASTA file
    for record in SeqIO.parse(fasta_file, "fasta"):
        sequence_id = record.id
        sequence = str(record.seq)

        print(f"Processing sequence: {sequence_id}")

        # Create a directory for this sequence
        sequence_dir = os.path.join(output_dir, sequence_id)
        os.makedirs(sequence_dir, exist_ok=True)

        with torch.no_grad():
            # Generate the PDB structure
            output = model.infer(sequence)
            pdb_output = model.infer_pdb(sequence)

        # Save the PDB output to a file
        pdb_file = os.path.join(sequence_dir, f"{sequence_id}.pdb")
        with open(pdb_file, "w") as f:
            f.write(pdb_output)

        # Save the pLDDT score to a file
        struct = bsio.load_structure(pdb_file, extra_fields=["b_factor"])
        b_factor_file = os.path.join(sequence_dir, f"pLDDT_{struct.b_factor.mean()}.pdb")
        with open(b_factor_file, "w") as f:
            f.write(str(struct.b_factor.mean()))

        # Compute PAE values from the model output
        pae = (output["aligned_confidence_probs"][0].cpu().numpy() * np.arange(64)).mean(-1) * 31
        mask = output["atom37_atom_exists"][0, :, 1] == 1
        mask = mask.cpu().numpy()  # Ensure mask is a NumPy array
        pae = pae[mask, :][:, mask]

        # Save PAE values to a JSON file
        pae_json = {
            "predicted_aligned_error": pae.tolist(),
            "max_predicted_aligned_error": float(pae.max())
        }

        json_file = os.path.join(sequence_dir, f"{sequence_id}_pae.json")
        with open(json_file, "w") as json_f:
            json.dump(pae_json, json_f, indent=4)

        # Generate and save the PAE heatmap
        plt.figure(figsize=(8, 6))
        plt.imshow(pae, cmap="viridis", interpolation="nearest")
        plt.colorbar(label="PAE (Å)")
        plt.title(f"Predicted Aligned Error (PAE) for {sequence_id}")
        plt.xlabel("Residue Index")
        plt.ylabel("Residue Index")
        plt.tight_layout()

        png_file = os.path.join(sequence_dir, f"{sequence_id}_pae.png")
        plt.savefig(png_file, dpi=300)  # High-resolution image
        plt.close()

        print(f"Saved outputs for {sequence_id} in {sequence_dir}")

    print(f"All sequences processed. Outputs are in the '{output_dir}' directory.")

if __name__ == "__main__":
    main()
