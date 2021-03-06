import sys, os, time
import numpy as np
import skimage.io as io
import write_data as wd

import parent_model as pm

np.random.seed(0)

from parameters import DIF_COEF, VISC, TOT_TIME, TIME_STEP, GLOB_DX, GLOB_DY, GLOB_DZ, LOAD_DIR, DOMAIN, VESSEL, HOLES, MPHAGE, NUCL, GEN_HOLES, SAVE_TIME

class Model(pm.Model):
    def __init__(self,  sim_dir='../sim/custom_model/', load_dir=LOAD_DIR, load_num="UT16-T-stack3-Sept10_iso_", load_datafile="particles-cropped.tif", d_co=DIF_COEF, vis=VISC, tot_time=TOT_TIME, dt=TIME_STEP, dx=GLOB_DX, dy=GLOB_DY, dz=GLOB_DZ, number_holes=5000, domain=DOMAIN, vessel=VESSEL, holes=HOLES, mphage=MPHAGE, nucl=NUCL, gen_holes=GEN_HOLES, update_time=9999999, save_data_time=SAVE_TIME):

        super(Model, self).__init__(sim_dir=sim_dir, load_dir=load_dir, load_num=load_num, load_datafile=load_datafile, d_co=d_co, vis=vis, tot_time=tot_time, dt=dt, dx=dx, dy=dy, dz=dz, number_holes=number_holes, domain=domain, vessel=vessel, holes=holes, mphage=mphage, nucl=nucl, gen_holes=gen_holes, update_time=update_time, save_data_time=save_data_time)

        #self.holes_loc = io.imread(self.holes).astype(float); self.holes_loc /= np.max(self.holes_loc)


    #--------------INITIALIZATION-------------
    #Same as Parent

    def concentration_time( self ):
        return super(Model, self).concentration_time()

    def create_source_location( self, minimum=0, maximum=None ):
        self.source_loc = np.zeros((maximum,maximum,maximum))
        self.source_loc[int(maximum/2),int(maximum/2),int(maximum/2)] = 100.
        return 0

    def create_flow_location( self, minimum=0, maximum=None ):
        return 0

    def create_mphage_location( self, minimum=0, maximum=None ):
        return 0

    def create_nucl_location( self, minimum=0, maximum=None ):
        return 0

    def create_diffusion_location( self, minimum=0, maximum=None ):
        self.diffusion_loc = np.ones((maximum,maximum,maximum))
        self.ijk = ( np.linspace(1, self.diffusion_loc.shape[0]-2, self.diffusion_loc.shape[0]-2) ).astype(int)

    def reduce_simulation( self, minimum=0, maximum=None ):
        super(Model, self).reduce_simulation( minimum, maximum )
        return 0

    def initialize( self, minimum=0, maximum=200 ):
        self.create_source_location( minimum=minimum, maximum=maximum )
        self.create_diffusion_location( minimum=minimum, maximum=maximum )
        return 0

    #--------------SIMULATION-------------
    #Same as Parent, except for update!

    def diffusion( self ):
        super(Model, self).diffusion()

    def neumann_condition( self ):
        #super(Model, self).neumann_condition()
        return 0

    def dirichlet_condition( self ):
        #super(Model, self).dirichlet_condition()
        return 0

    def update_simulation( self ):
        return 0

    def simulation_step(self):
        self.diffusion()
        return 0

    #--------------SAVING-------------

    def save_sim( self ):
        super(Model, self).save_sim()
