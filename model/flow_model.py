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

    #--------------SIMULATION-------------
    #Same as Parent, except for update!


    def simulation_step(self):
        self.diffusion_location()
        self.flow_location()
        return 0
