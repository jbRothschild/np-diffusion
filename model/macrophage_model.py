import sys, os, time
import numpy as np
import skimage.io as io

import parent_model as gm

from parameters import DIF_COEF, VISC, TOT_TIME, TIME_STEP, GLOB_DX, GLOB_DY, GLOB_DZ, LOAD_DIR, DOMAIN, VESSEL, HOLES, MPHAGE, NUCL

class Model(gm.Model):
    def __init__( self,  sim_dir='../sim/mphage_model', load_dir=LOAD_DIR, load_num="UT16-T-stack3-Sept10_iso_", load_datafile="particles-cropped.tif", d_co=DIF_COEF, vis=VISC, tot_time=TOT_TIME, dt=TIME_STEP, dx=GLOB_DX, dy=GLOB_DY, dz=GLOB_DZ, number_holes=5000, domain=DOMAIN, vessel=VESSEL, holes=HOLES, mphage=MPHAGE, nucl=NUCL, mphage_rate=0.2 ):

        gm.Model.__init__( self,  sim_dir='../sim/mphage_model', load_dir=LOAD_DIR, load_num="UT16-T-stack3-Sept10_iso_", load_datafile="particles-cropped.tif", d_co=DIF_COEF, vis=VISC, tot_time=TOT_TIME, dt=TIME_STEP, dx=GLOB_DX, dy=GLOB_DY, dz=GLOB_DZ, number_holes=0, domain=DOMAIN, vessel=VESSEL, holes=HOLES, mphage=MPHAGE, nucl=NUCL )

        self.mphage_rate = mphage_rate

    #--------------INITIALIZATION-------------
    #Same as Parent
    self.holes_loc = io.imread(self.holes).astype(float); self.holes_loc /= np.max(self.holes_loc)

    def initialize( self ):
        self.create_source_location()
        self.create_mphage_location()
        self.create_diffusion_location()
        return 0

    def create_mphage_location(self):
        self.mphage_loc = io.imread(self.mphage).astype(float); self.mphage_loc /= np.max(self.mphage_loc)
        self.mphage_flow_loc = np.zeros((self.mphage_loc.shape[0], self.mphage_loc.shape[1], self.mphage_loc.shape[2]))
        for i in range(1, self.mphage_flow_loc[0]-1):
            for j in range(1, self.mphage_flow_loc.shape[1]-1):
                for k in range(1, self.mphage_flow_loc.shape[2]-1):
                    if self.mphage_loc[i,j,k] == 1.0:
                        if self.mphage_loc[i-1,j,k] == 0.0:
                            self.mphage_flow_loc[i-1,j,k] = 1.0
                        if self.mphage_loc[i+1,j,k] == 0.0:
                            self.mphage_flow_loc[i+1,j,k] = 1.0
                        if self.mphage_loc[i,j-1,k] == 0.0:
                            self.mphage_flow_loc[i,j-1,k] = 1.0
                        if self.mphage_loc[i,j+1,k] == 0.0:
                            self.mphage_flow_loc[i,j+1,k] = 1.0
                        if self.mphage_loc[i,j,k-1] == 0.0:
                            self.mphage_flow_loc[i,j,k-1] = 1.0
                        if self.mphage_loc[i,j,k+1] == 0.0:
                            self.mphage_flow_loc[i,j,k+1] = 1.0
        return 0

    def create_diffusion_location(self):
        gm.Model.create_diffusion_location()
        self.diffusion_loc -= self.mphage_loc

    #--------------SIMULATION-------------
    #Same as Parent, except for update!

    def mphage_dynamics(self):

        return 0

    def update_simulation(self):
        return 0

    def simulation(self):
        self.diffusion_location()
        self.source_location()
        self.mphage_dynamics()
        return 0
