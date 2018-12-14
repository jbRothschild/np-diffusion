#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=40
#SBATCH --time=24:00:00
#SBATCH --job-name np_diffusion

#run this code using jbroths:~$ sbatch *script_name.sh*

# DIRECTORY TO RUN - $SLURM_SUBMIT_DIR is directory job was submitted from
cd $SLURM_SUBMIT_DIR/model

# load modules (must match modules used for compilation)
module load cmake
module load intel/2018.2
module load anaconda2/5.1.0

# Turn off implicit threading in Python, R
export OMP_NUM_THREADS=3

# Commands to be run now

for i in 158 159 160; do
  for j in 1 2 3 4; do
    for k in 5; do
      if ([ ${i} -eq 158 ] && [ ${j} -eq 2 ]) || ([ ${i} -eq 159 ] && [ ${j} -eq 1 ]) || ([ ${i} -eq 159 ] && [ ${j} -eq 2 ]) || ([ ${i} -eq 160 ] && [ ${j} -eq 1 ]); then
        data=("../sim/parent_model_${i}_${j}_gaps${k}_0050/" "MSC${i}-T-stack${j}-Nov29-2018_iso" "particles_trimmed.tif" "gaps_actual.tif" "gaps_50x.tif" "thresh_vessels.tif" "tissue_boundary.tif" ${k} 2.234)
      else
        data=("../sim/parent_model_${i}_${j}_gaps${k}_0050/" "MSC${i}-T-stack${j}-Nov29-2018_iso" "particles_trimmed.tif" "gaps_actual.tif" "gaps_50x.tif" "thresh_vessels.tif" "tissue_boundary.tif" ${k} 2.0)
      fi
      (python2 main.py -m parent_model -p ${data[@]}) &
    #(make sim model="parent_model" param=("../sim/hopping_model_${i}_${j}/" "MSC${i}-T-stack${j}-Nov29-2018_iso" "particles_trimmed.tif gaps_actual.tif" "gaps_50x.tif" "thresh_vessels.tif" "tissue_boundary.tif")) &
    #(make sim model=parent_model param=( ../sim/parent_model_'$i'_'$j'/ MSC'$i'-T-stack'$j'-Nov29-2018_iso particles_trimmed.tif gaps_actual.tif gaps_50x.tif thresh_vessels.tif tissue_boundary.tif) ) &
    done
  done
done

# macrophage model
#for i in 10 60 300 1800; do
#  (python2 main.py -m macrophage_model -p "../sim/macrophage_model_${i}/" ${i} 86400 3600) &
#done

# custom model
#python2 main.py -m custom_model

wait
