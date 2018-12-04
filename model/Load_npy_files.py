import numpy as np
import skimage as io
from matplotlib import pyplot as plt
import glob 
import matplotlib

file_path = "C:\\Users\\admin\\git\\np-diffusion\\data\\sim_macrophage_model_test_[test]\\diff_60.0sec.npy"
macro_loc =  "C:\\Users\\admin\\git\\np-diffusion\\data\\sim_macrophage_model_test_[test]\\macro_location.npy"
a = np.load(file_path)
b = np.load(macro_loc)
print(np.sum(a))
print(np.shape(b))