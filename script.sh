#!/bin/bash

#data=("../sim/hopping_model_1_1" "MSC1-T-stack1-Nov29-2018_iso" "particles_trimmed.tif" "gaps_actual.tif" "gaps_50x.tif" "thresh_vessels.tif" "tissue_boundary.tif")

#data=("../sim/hopping_model_${i}_${j}/" "MSC${i}-T-stack${j}-Nov29-2018_iso" "particles_trimmed.tif" "gaps_actual.tif" "gaps_50x.tif" "thresh_vessels.tif" "tissue_boundary.tif")
#python2 main.py -m parent_model -p ${data[@]}

for i in 0 1 2; do
  for j in 0 1 2 3; do
    if ([ ${i} -eq 158 ] && [ ${j} -eq 2 ]) || ([ ${i} -eq 159 ] && [ ${j} -eq 1 ]) || ([ ${i} -eq 159 ] && [ ${j} -eq 2 ]) || ([ ${i} -eq 160 ] && [ ${j} -eq 1 ]); then
      echo $i $k "hello"
    else
      echo $i $k "world"
    fi
  done
done
