import sys, os, time
import numpy as np
import skimage.io as io

import parent_model as pm

from parameters import DIF_COEF, VISC, TOT_TIME, TIME_STEP, GLOB_DX, GLOB_DY, GLOB_DZ, LOAD_DIR, DOMAIN, VESSEL, HOLES, MPHAGE, NUCL

class Model(pm.Model):
    def __init__(self,  sim_dir='../sim/hopping_model/', load_dir=LOAD_DIR, load_num="UT16-T-stack3-Sept10_iso_", load_datafile="particles-cropped.tif", d_co=DIF_COEF, vis=VISC, tot_time=TOT_TIME, dt=TIME_STEP, dx=GLOB_DX, dy=GLOB_DY, dz=GLOB_DZ, number_holes=5000, domain=DOMAIN, vessel=VESSEL, holes=HOLES, mphage=MPHAGE, nucl=NUCL, hole_update_time=9999999):

        super(Model, self).__init__(sim_dir=sim_dir, load_dir=LOAD_DIR, load_num="UT16-T-stack3-Sept10_iso_", load_datafile="particles-cropped.tif", d_co=DIF_COEF, vis=VISC, tot_time=TOT_TIME, dt=TIME_STEP, dx=GLOB_DX, dy=GLOB_DY, dz=GLOB_DZ, number_holes=number_holes, domain=DOMAIN, vessel=VESSEL, holes=HOLES, mphage=MPHAGE, nucl=NUCL)
        self.holes_loc = io.imread(self.holes).astype(float); self.holes_loc /= np.max(self.holes_loc)
        self.update1_time = hole_update_time

    #--------------INITIALIZATION-------------
    #Same as Parent

    def concentration_time( self ):
        return super(Model, self).concentration_time()

    def create_source_location( self, minimum=0, maximum=-1 ):
        super(Model, self).create_source_location( minimum, maximum )

    def create_flow_location( self, minimum=0, maximum=-1 ):
        super(Model, self).create_flow_location( minimum, maximum )

    def create_mphage_location( self, minimum=0, maximum=-1 ):
        super(Model, self).create_mphage_location( minimum, maximum )

    def create_nucl_location( self, minimum=0, maximum=-1 ):
        super(Model, self).create_nucl_location( minimum, maximum )

    def create_diffusion_location( self, minimum=0, maximum=-1 ):
        super(Model, self).create_diffusion_location( minimum, maximum )

    def initialize( self, minimum=0, maximum=-1 ):
        self.create_source_location( minimum, maximum )
        self.create_diffusion_location( minimum, maximum )
        return 0

    #--------------SIMULATION-------------
    #Same as Parent, except for update!

    def diffusion( self ):
        super(Model, self).diffusion()

    def neumann_condition( self ):
        super(Model, self).neumann_condition()

    def dirichlet_condition( self ):
        super(Model, self).dirichlet_condition()

    def update1_simulation( self ):
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
    """"
    def reduce_simulation( self, minimum, maximum ):
        self.diffusion_loc = self.diffusion_loc[ minimum:maximum, minimum:maximum, minimum:maximum ]
        self.source_loc = self.source_loc[ minimum:maximum, minimum:maximum, minimum:maximum ]
        self.solution = np.zeros( np.asarray( self.diffusion_loc ).shape )
        self.ijk = ( np.linspace(1, self.diffusion_loc.shape[0]-2, self.diffusion_loc.shape[0] - 2 ) ).astype(int)

        return 0
    """
    def simulation_step(self):
        self.diffusion()
        self.dirichlet_condition()
        return 0
