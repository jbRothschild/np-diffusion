import sys, os, time
import numpy as np
import skimage.io as io
import math
import write_data as wd

import parent_model as pm

np.random.seed(0)

from parameters import DIF_COEF, VISC, TOT_TIME, TIME_STEP, GLOB_DX, GLOB_DY, GLOB_DZ, LOAD_DIR, DOMAIN, VESSEL, HOLES, MPHAGE, NUCL, GEN_HOLES, SAVE_TIME

class Model(pm.Model):
    def __init__(self,  sim_dir='../sim/cylinder_model/', load_dir=None, load_num=None, load_datafile="particles-cropped.tif", d_co=DIF_COEF, vis=VISC, tot_time=TOT_TIME, dt=0.5, dx=0.5, dy=0.5, dz=0.5, number_holes=None, domain=None, vessel=None, holes=None, mphage=None, nucl=None, gen_holes=None, update_time=9999999, save_data_time=SAVE_TIME):
        # Initialize model accoding to the parent model

        super(Model, self).__init__(sim_dir=sim_dir, load_dir=load_dir, load_num=load_num, load_datafile=load_datafile, d_co=d_co, vis=vis, tot_time=tot_time, dt=dt, dx=dx, dy=dy, dz=dz, number_holes=number_holes, domain=domain, vessel=vessel, holes=holes, mphage=mphage, nucl=nucl, gen_holes=gen_holes, update_time=update_time, save_data_time=save_data_time)

        self.radius_vessel = 5.0; self.radius_hole=0.5
        return 0


    #--------------INITIALIZATION-------------
    # To set defaults of parent, simply remove the commented super functionality

    def concentration_time( self ):
        return super(Model, self).concentration_time()

    def create_source_location( self, minimum=0, maximum=None ):
        # super(Model, self).create_source_location( minimum, maximum )

        # holes
        self.source_loc = np.zeros((maximum,maximum,maximum))
        for i in np.arange(math.floor(maximum/2-self.hole_radius/self.dx), math.ceil(maximum/2+self.hole_radius/self.dx):
            for j in np.arange(math.floor(maximum/2-self.hole_radius/self.dx), math.ceil(maximum/2+self.hole_radius/self.dx):
                k=int(maximum/2)
                while ((maximum/2 - j)*self.dy)**2 + ((maximum/2 - k)*self.dz)**2 < 5.**2: k+=1
                self.source_loc[i,j,k] = 1.

        # uniform TODO

        return 0

    def create_flow_location( self, minimum=0, maximum=None ):
        # super(Model, self).create_flow_location( minimum, maximum )
        # For now ignore flow into the tumor by convection. Purely diffusion.
        # Might be some questions to ask regarding the IFP

    def create_mphage_location( self, minimum=0, maximum=None ):
        # super(Model, self).create_mphage_location( minimum, maximum )
        # Macrophages should be labeled and show be able to update, move around.
        # For now make them not move though, stationary

    def create_nucl_location( self, minimum=0, maximum=None ):
        # super(Model, self).create_nucl_location( minimum, maximum )

    def create_cell_location( self, minimum=0, maximum=None ):
        # idea behind cells is that they are obstacles in the way of
        # nanoparticle diffusion. Should be some uptake though

    def create_diffusion_location( self, minimum=0, maximum=None ):
        # super(Model, self).create_diffusion_location( minimum, maximum )
        self.diffusion_loc = np.zeros((maximum,maximum,maximum))
        self.diffusion_loc += 1.0
        for j in np.arange(0,maximum):
            for k in np.arange(0,maximum):
                if ((maximum/2 - j)*self.dy)**2 + ((maximum/2 - k)*self.dz)**2 < 5.**2
                    self.diffusion_loc[:,j,k] = 0.0
        self.diffusion_loc += self.source_loc
        self.ijk = ( np.linspace(1, self.diffusion_loc.shape[0]-2, self.diffusion_loc.shape[0]-2) ).astype(int)
        return 0


    def reduce_simulation( self, minimum, maximum ):
        # super(Model, self).reduce_simulation( minimum, maximum )
        return 0

    def initialize( self, minimum=0, maximum=150 ):
        self.create_source_location( minimum, maximum )
        self.create_diffusion_location( minimum, maximum )
        self.create_flow_location( minimum, maximum )
        return 0

    #--------------SIMULATION-------------
    #Same as Parent, except for update!

    def diffusion( self ):
        super(Model, self).diffusion()

    def neumann_condition( self ):
        super(Model, self).neumann_condition()

    def dirichlet_condition( self ):
        super(Model, self).dirichlet_condition()

    def update_simulation( self ):
        #UPDATING HAPPENS HERE, can have multiple update I guess
        total = np.sum(self.source_loc)
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

    def simulation_step(self):
        self.diffusion()
        self.dirichlet_condition()
        #self.neumann_condition()
        return 0

    #--------------SAVING-------------

    def save_sim( self ):
        super(Model, self).save_sim()
