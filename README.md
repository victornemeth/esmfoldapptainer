# ESMFold Apptainer Container 

This repository hosts a prebuilt **Apptainer/Singularity container** for [ESMFold](https://github.com/facebookresearch/esm), a protein structure prediction model developed by Meta.

---

## 🔄 Files in this repository

- `sha256sum.txt` – SHA256 checksum for verifying the container  
- `esmfold.sif` – Downloaded separately (see below)

---

## ✅ Getting Started

1. **Clone the this repository:**

   ```bash
   git clone https://github.com/victornemeth/esmfoldapptainer.git
   cd esmfoldapptainer
   ```

2. **Download the prebuilt `esmfold.sif` container from Zenodo:**

   ```bash
   wget -O esmfold.sif "https://zenodo.org/records/15194473/files/evo2.sif?download=1"
   ```

   Or download it manually here:  
   👉 [Download esmfold.sif (8.4GB)](https://zenodo.org/records/15194473/files/evo2.sif?download=1)

3. **Run Evo 2 using the Apptainer container:**

   ```bash
	apptainer exec --nv esmfold.sif python3 fold.py input.fasta -o output
   ```

   > 🧠 This will use GPU acceleration (`--nv`), bind your local code and model directories, and run inference using the `evo2_7b` model.

---

## 🔄 Building the Container Yourself (Optional)

If you prefer building from source using Docker:

```bash
git clone --branch add-dockerfile https://github.com/victornemeth/evo2.git
cd evo2
docker build -t evo2 .
singularity build evo2.sif docker-daemon://evo2:latest
```

---

## 🔒 Verifying the Container

To verify the container file:

```bash
diff <(sha256sum esmfold.sif) sha256sum.txt && echo "✅ Match!" || echo "❌ Mismatch!"
```

---

Note:


---

## 📄 License

This repo contains only the container checksum and basic fold script. For licensing and usage terms, refer to the [official ESM2 repository](https://github.com/facebookresearch/esm).
