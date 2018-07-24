#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=40
#SBATCH --time=2:00:00
#SBATCH --job-name np_diffusion

#run this code using jbroths:~$ sbatch *script_name.sh*

# DIRECTORY TO RUN - $SLURM_SUBMIT_DIR is directory job was submitted from
cd $SLURM_SUBMIT_DIR

# load modules (must match modules used for compilation)
module load make
module load intel/2018.2
module load python/2.7.14

# Turn off implicit threading in Python, R
export OMP_NUM_THREADS=1

# Commands to be run now
(make data DC=20 && echo "Diffusion at D coefficient 20 finished") &
(make data DC=0.01 && echo "Diffusion at D coefficient 0.01 finished") &
(make data DC=0.1 && echo "Diffusion at D coefficient 0.1 finished") &
(make data DC=1 && echo "Diffusion at D coefficient 1 finished") &
(make data DC=5 && echo "Diffusion at D coefficient 5 finished") &
(make data DC=10 && echo "Diffusion at D coefficient 20 finished") &
wait
