# ESMFold Apptainer Container 

This repository hosts a prebuilt **Apptainer/Singularity container** for [ESMFold](https://github.com/facebookresearch/esm), a protein structure prediction model developed by Meta.

---

## 🔄 Files in this repository

- `sha256sum.txt` – SHA256 checksum for verifying the container  
- `esmfold.sif` – Downloaded separately (see below)
- `Dockerfile` - Dockerfile to build the esmfold container in docker
- `fold.py` - python script to fold proteins, using FASTA as input
- `fold_chunk.py` - idem to fold.py but uses chunking to reduce maximum vram usage
- `esmdocker.sh` - basic shell script to run esmfold container with fold.py
---

## ✅ Getting Started

1. **Clone the this repository:**

   ```bash
   git clone https://github.com/victornemeth/esmfoldapptainer.git
   cd esmfoldapptainer
   ```

2. **Download the prebuilt `esmfold.sif` container from Zenodo:**

   ```bash
   wget -O esmfold.sif "https://zenodo.org/records/15318546/files/esmfold.sif?download=1"
   ```

   Or download it manually here:  
   👉 [Download esmfold.sif (8.4GB)](https://zenodo.org/records/15318546/files/esmfold.sif?download=1)

3. **Run ESMFold using the Apptainer container:**

   ```bash
	apptainer exec --nv esmfold.sif python3 fold.py input.fasta -o output
   ```

   > 🧠 This will use GPU acceleration (`--nv`)

---

## 🔄 Building the Container Yourself (Optional)

If you prefer building from source using Docker:

```bash
docker build -t esmfold .
singularity build esmfold.sif docker-daemon://esmfold:latest
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
