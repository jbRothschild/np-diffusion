!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=40
#SBATCH --time=24:00:00
#SBATCH --job-name np_diffusion

#run this code using jbroths:~$ sbatch *script_name.sh*

# DIRECTORY TO RUN - $SLURM_SUBMIT_DIR is directory job was submitted from
cd $SLURM_SUBMIT_DIR

# load modules (must match modules used for compilation)
module load cmake
module load intel/2018.2
module load anaconda2/5.1.0

# Turn off implicit threading in Python, R
export OMP_NUM_THREADS=1

# Commands to be run now
(make data param=1.) &
(make data param=10.) &
(make data param=60.) &
(make data param=300. && echo "DC=number of holes in simulation") &
wait
