import sys, os, time
import numpy as np
from skimage import io

class Data:
    def __init__(self, data_folder="../ChanLab/", datafile="UT16-T-stack3-Sept10_iso_particles-cropped.tif",  ):
        self.raw_data = io.imread( data_folder + datafile )
        self.dataset = []
        self.raw_to_dataset()

    def raw_to_dataset( self ):
        self.no_noise_raw = np.copy( self.raw_data - (self.raw_data>0) * np.min(self.raw_data[self.raw_data>0]) )
        particle = np.sum(self.no_noise_raw)//131000000
        self.no_noise_raw = self.no_noise_raw//int(particle)
        for i in range( self.no_noise_raw.shape[0] ):
            for j in range( self.no_noise_raw.shape[1] ):
                for k in range( self.no_noise_raw.shape[0] ):
                    for number in range( self.no_noise_raw[i, j, k] ):
                        self.dataset.append( [i, j, k] )

    def analyze_raw_data( self ):
        self.no_noise_raw = np.copy( self.raw_data - (self.raw_data>0) * np.min(self.raw_data[self.raw_data>0]) )
        particle = np.sum(self.no_noise_raw)//131000000
        self.no_noise_raw = self.no_noise_raw//int(particle)
        #In this data should be 1.31*10**8 particles, 131000000

# Data(UT16-T-stack3-Sept10_iso_particles-cropped.tif, UT16-T-stack3-Sept10_iso_particles-cropped.tif)
