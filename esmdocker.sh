#!/bin/sh
#
#
#PBS -l nodes=1:ppn=4:gpus=1
#PBS -l mem=27gb
#PBS -l walltime=10:00:00
#

cd YOURFOLDER

apptainer exec --nv $VSC_SCRATCH_KYUKON_VO/esmfold.sif python3 ./fold_chunk.py ./input.fasta -o output
