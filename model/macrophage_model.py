import sys, os, time
import numpy as np
import skimage.io as io

import hopping_model as hm

from parameters import DIF_COEF, VISC, TOT_TIME, TIME_STEP, GLOB_DX, GLOB_DY, GLOB_DZ, LOAD_DIR, DOMAIN, VESSEL, HOLES, MPHAGE, NUCL, GEN_HOLES, SAVE_TIME

class Model(hm.Model):
    def __init__( self,  sim_dir='../sim/mphage_model/', load_dir=LOAD_DIR, load_num="UT16-T-stack3-Sept10_iso_", load_datafile="particles-cropped.tif", d_co=DIF_COEF, vis=VISC, tot_time=TOT_TIME, dt=TIME_STEP, dx=GLOB_DX, dy=GLOB_DY, dz=GLOB_DZ, number_holes=5000, domain=DOMAIN, vessel=VESSEL, holes=HOLES, mphage=MPHAGE, nucl=NUCL, gen_holes=GEN_HOLES, mphage_rate=0.2, update_time=9999999, save_data_time=SAVE_TIME ):

        super(Model, self).__init__( sim_dir=sim_dir, load_dir=load_dir, load_num=load_num, load_datafile=load_datafile, d_co=d_co, vis=vis, tot_time=tot_time, dt=dt, dx=dx, dy=dy, dz=dz, number_holes=number_holes, domain=domain, vessel=vessel, holes=holes, mphage=mphage, nucl=nucl, gen_holes=gen_holes, update_time=update_time, save_data_time=save_data_time )

        self.mphage_rate = mphage_rate
        self.holes_loc = io.imread(self.holes).astype(float); self.holes_loc /= np.max(self.holes_loc)

    #--------------INITIALIZATION-------------
    #Same as Parent

    def concentration_time( self ):
        return super(Model, self).concentration_time()

    def create_source_location( self, minimum=0, maximum=None ):
        super(Model, self).create_source_location( minimum, maximum )

    def create_flow_location( self, minimum=0, maximum=None ):
        super(Model, self).create_flow_location( minimum, maximum )

    def create_mphage_location( self, minimum=0, maximum=None ):
        self.mphage_loc = io.imread(self.mphage).astype(float)[ minimum:maximum, minimum:maximum, minimum:maximum ]; self.mphage_loc /= np.max(self.mphage_loc)
        self.mphage_flow_loc = np.zeros((self.mphage_loc.shape[0], self.mphage_loc.shape[1], self.mphage_loc.shape[2]))
        for i in range( 1, self.mphage_flow_loc.shape[0] - 1 ):
            for j in range( 1, self.mphage_flow_loc.shape[1] - 1 ):
                for k in range( 1, self.mphage_flow_loc.shape[2] - 1 ):
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

    def create_nucl_location( self, minimum=0, maximum=None ):
        super(Model, self).create_nucl_location( minimum, maximum )

    def create_diffusion_location( self, minimum=0, maximum=None ):
        super(Model, self).create_diffusion_location( minimum, maximum )
        self.diffusion_loc -= self.mphage_loc #macrophage location not part of diffusion
        self.diffusion_loc[ self.diffusion_loc >= 1.0 ] = 1.0
        self.diffusion_loc[ self.diffusion_loc < 1.0 ] = 0.0
        self.particles_in_macrophage = self.mphage_loc + self.mphage_flow_loc #include the area around macrophage in mphage

    def reduce_simulation( self, minimum, maximum ):
        super(Model, self).reduce_simulation( minimum, maximum )
        self.mphage_flow_loc = self.mphage_flow_loc[ minimum:maximum, minimum:maximum, minimum:maximum ]
        self.mphage_loc = self.mphage_loc[ minimum:maximum, minimum:maximum, minimum:maximum ]
        self.particles_in_macrophage = self.particles_in_macrophage[ minimum:maximum, minimum:maximum, minimum:maximum ]
        return 0

    def initialize( self, minimum=0, maximum=None ):
        self.create_source_location( minimum, maximum )
        self.create_flow_location( minimum, maximum )
        self.create_mphage_location( minimum, maximum )
        self.create_diffusion_location( minimum, maximum )
        self.reduce_simulation( 205, 610-205 )
        return 0

    #--------------SIMULATION-------------
    #Same as Parent, except for update!

    def diffusion( self ):
        super(Model, self).diffusion()

    def neumann_condition( self ):
        super(Model, self).neumann_condition()

    def dirichlet_condition( self ):
        super(Model, self).dirichlet_condition()

    def mphage_dynamics(self):
        self.solution += - self.mphage_rate * self.solution * self.mphage_flow_loc * self.dt
        self.particles_in_macrophage += self.mphage_rate * self.solution * self.mphage_flow_loc * self.dt
        if self.time in range(0, self.total_time +1, self.save_data_time):
            np.save(self.sim_dir + "macrophage", self.particles_in_macrophage)
        return 0

    def update_simulation( self ):
        super(Model, self).update_simulation()
        return 0

    def simulation_step(self):
        super(Model, self).simulation_step()
        self.mphage_dynamics()
        return 0
