#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=40
#SBATCH --time=0:30:00
#SBATCH --job-name np_diffusion

#run this code using jbroths:~$ sbatch *script_name.sh*

# DIRECTORY TO RUN - $SLURM_SUBMIT_DIR is directory job was submitted from
cd $SLURM_SUBMIT_DIR/model

# load modules (must match modules used for compilation)
module load cmake
module load intel/2018.2
module load anaconda2/5.1.0

# Turn off implicit threading in Python, R
export OMP_NUM_THREADS=40

# Commands to be run now
for i in 158 159 160; do
  for j in 1 2 3; do
    data=("../sim/hopping_model_${i}_${j}/" "MSC${i}-T-stack${j}-Nov29-2018_iso" "particles_trimmed.tif" "gaps_actual.tif" "gaps_50x.tif" "thresh_vessels.tif" "tissue_boundary.tif")
    python2 main.py -m parent_model -p ${data[@]}
    #(make sim model="parent_model" param=("../sim/hopping_model_${i}_${j}/" "MSC${i}-T-stack${j}-Nov29-2018_iso" "particles_trimmed.tif gaps_actual.tif" "gaps_50x.tif" "thresh_vessels.tif" "tissue_boundary.tif")) &
    #(make sim model=parent_model param=( ../sim/parent_model_'$i'_'$j'/ MSC'$i'-T-stack'$j'-Nov29-2018_iso particles_trimmed.tif gaps_actual.tif gaps_50x.tif thresh_vessels.tif tissue_boundary.tif) ) &
  done
done
wait
