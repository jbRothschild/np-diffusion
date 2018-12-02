import sys, os, time
import numpy as np
import skimage.io as io

import parent_model as gm

from parameters import DIF_COEF, VISC, TOT_TIME, TIME_STEP, GLOB_DX, GLOB_DY, GLOB_DZ, LOAD_DIR, DOMAIN, VESSEL, HOLES, MPHAGE, NUCL

class Model(gm.Model):
    def __init__(self,  sim_dir='../sim/hopping_model', load_dir=LOAD_DIR, load_num="UT16-T-stack3-Sept10_iso_", load_datafile="particles-cropped.tif", d_co=DIF_COEF, vis=VISC, tot_time=TOT_TIME, dt=TIME_STEP, dx=GLOB_DX, dy=GLOB_DY, dz=GLOB_DZ, number_holes=0, domain=DOMAIN, vessel=VESSEL, holes=HOLES, mphage=MPHAGE, nucl=NUCL):

        gm.Model.__init__(self,  sim_dir='../sim/generic_model', load_dir=LOAD_DIR, load_num="UT16-T-stack3-Sept10_iso_", load_datafile="particles-cropped.tif", d_co=DIF_COEF, vis=VISC, tot_time=TOT_TIME, dt=TIME_STEP, dx=GLOB_DX, dy=GLOB_DY, dz=GLOB_DZ, number_holes=0, domain=DOMAIN, vessel=VESSEL, holes=HOLES, mphage=MPHAGE, nucl=NUCL)

    #--------------INITIALIZATION-------------
    #Same as Parent
    self.holes_loc = io.imread(self.holes).astype(float); self.holes_loc /= np.max(self.holes_loc)

    def initialize(self):
        self.create_source_location()
        self.create_diffusion_location()
        self.create_mphage_location()
        return 0

    #--------------SIMULATION-------------
    #Same as Parent, except for update!

    def update_simulation(self):
        #UPDATING HAPPENS HERE, can have multiple update I guess
        total = self.number_holes
        other = np.sum(self.holes_loc)
        self.source_loc *= 0.0

        for i in np.arange(0, self.holes_loc.shape[0]):
            for j in np.arange(0, self.holes_loc.shape[1]):
                for k in np.arange(0, self.holes_loc.shape[2]):
                    if (self.holes_loc[i,j,k] > 0.0 and total > 0):
                        prob = np.random.randint(0,other)
                        other -= 1.0
                        if prob < total:
                            self.source_loc[i,j,k] += 1.0
                            total -= 1
        return 0

    def simulation(self):
        self.diffusion_location()
        self.source_location()
        return 0
