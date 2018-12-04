import sys, os, time
import numpy as np
from skimage import io

import matplotlib.pyplot as plt

from parameters import DIF_COEF, VISC, TOT_TIME, TIME_STEP, GLOB_DX, GLOB_DY, GLOB_DZ, LOAD_DIR, DOMAIN, VESSEL, HOLES, MPHAGE, NUCL

class Model(object):
    def __init__( self,  sim_dir='../sim/parent_model/', load_dir=LOAD_DIR, load_num="UT16-T-stack3-Sept10_iso_", load_datafile="particles-cropped.tif", d_co=DIF_COEF, vis=VISC, tot_time=TOT_TIME, dt=TIME_STEP, dx=GLOB_DX, dy=GLOB_DY, dz=GLOB_DZ, number_holes=5000, domain=DOMAIN, vessel=VESSEL, holes=HOLES, mphage=MPHAGE, nucl=NUCL , *args):
        self.d_co = d_co; self.vis = vis #Diffusion coefficient and viscosity
        self.total_time = tot_time #total time for simulation
        self.dt = dt; self.dx = dx; self.dy = dy; self.dz = dz #metric
        if not os.path.exists(sim_dir):
            os.makedirs(sim_dir)
        self.load_dir = load_dir+load_num; self.sim_dir = sim_dir
        self.datafile = self.load_dir + load_datafile
        self.domain = self.load_dir + DOMAIN; self.vessel = self.load_dir + vessel; self.holes = self.load_dir + holes; self.mphage = self.load_dir + mphage; self.nucl = self.load_dir + nucl
        self.number_holes = number_holes

        if os.path.exists( self.sim_dir + "timepoint.npy" ): #If continuing simulation, reloads
            self.time = np.load( self.sim_dir + "timepoint.npy" )
        else:
            self.time = 0.0
            np.save(self.sim_dir + "timepoint.npy", np.asarray(self.time))

        if os.path.exists( self.sim_dir + "time_sum.npy" ): #If continuing simulation, reloads
            self.timeSum = np.load( self.sim_dir + "time_sum.npy" )
        else:
            self.timeSum = np.array( [[0],[0.0]] )
            np.save( self.sim_dir + "time_sum.npy", self.timeSum )

    def unpack( self ):
        return self.d, self.d_co, self.time, self.dt, self.dx, self.dy, self.dz

    def concentration_time( self ):
        return 0.7521 * np.exp( -1.877*self.time/3600. ) + 0.2479 * np.exp( -0.1353*self.time/3600. )
        #return 0.5407 * np.exp( -0.3465*self.time ) + 0.4593 * np.exp( -5.122*self.time ) (in hours or minutes or sec????)

    #--------------INITIALIZATION-------------

    def create_source_location( self, minimum=0, maximum=-1 ):
        #Creates source location
        if os.path.exists( self.sim_dir + "source_location.npy" ): #If continuing simulation, reloads
            self.source_loc = np.load( self.sim_dir+"source_location.npy" )
        else: #Creates new source, location
            self.holes_loc = io.imread( self.holes ).astype(float)[ minimum:maximum, minimum:maximum, minimum:maximum ]; self.holes_loc /= np.max( self.holes_loc )
            all_holes = np.sum( self.holes_loc )
            self.source_loc = np.zeros( np.asarray( self.holes_loc ).shape )
            num_holes = self.number_holes
            #Select random locations
            for i in np.arange( 0, self.holes_loc.shape[0] ):
                for j in np.arange( 0, self.holes_loc.shape[1] ):
                    for k in np.arange( 0, self.holes_loc.shape[2] ):
                        if ( self.holes_loc[i,j,k] > 0.0 and num_holes > 0 ):
                            prob = np.random.randint( 0, all_holes )
                            all_holes -= 1.0
                            if prob < num_holes:
                                self.source_loc[i,j,k] += 1.0
                                num_holes -= 1
        return 0

    def create_flow_location( self, minimum=0, maximum=-1 ):
        #Location of where there is flow out of the vessel, an array with 1 just outside of teh vessel and 0 where elsewhere
        if os.path.exists( self.sim_dir + "flow_location.npy" ): #If continuing simulation, reloads
            self.flow_loc = np.load( self.sim_dir + "flow_location.npy" )
        else:
            vessel_location = io.imread( self.vessel ).astype(float)[ minimum:maximum, minimum:maximum, minimum:maximum ]; vessel_location /= np.max( vessel_location )
            self.flow_loc = np.zeros( ( vessel_location.shape[0], vessel_location.shape[1], vessel_location.shape[2] ) )
        #Every locations near the vascularue gets +1#---------------------------------------------------------------------
        for i in range( 1, vessel_location.shape[0] - 1 ) :
            for j in range( 1, vessel_location.shape[1] - 1 ) :
                for k in range( 1, vessel_location.shape[2] - 1 ):
                    if vessel_location[i, j, k] == 1.0:
                        if vessel_location[i-1, j, k] == 0.0:
                            self.flow_loc[i-1, j, k] += 1.0
                        if vessel_location[i+1, j, k] == 0.0:
                            self.flow_loc[i+1, j, k] += 1.0
                        if vessel_location[i, j-1, k] == 0.0:
                            self.flow_loc[i, j-1, k] += 1.0
                        if vessel_location[i, j+1, k] == 0.0:
                            self.flow_loc[i, j+1, k] += 1.0
                        if vessel_location[i, j, k-1] == 0.0:
                            self.flow_loc[i, j, k-1] += 1.0
                        if vessel_location[i, j, k+1] == 0.0:
                            self.flow_loc[i, j, k+1] += 1.0
        del vessel_location
        return 0

    def create_diffusion_location( self, minimum=0, maximum=-1 ):
        if os.path.exists( self.sim_dir + "diffusion_location.npy" ): #If continuing simulation, reloads
            self.diffusion_loc = np.load( self.sim_dir+"flow_location.npy" )
        else:
            tumor_location = io.imread( self.domain ).astype(float)[ minimum:maximum, minimum:maximum, minimum:maximum ]
            self.diffusion_loc = np.ones( np.asarray( tumor_location ).shape ); self.diffusion_loc /= np.max( self.diffusion_loc)
            vessel_location = io.imread( self.vessel ).astype(float)[ minimum:maximum, minimum:maximum, minimum:maximum ]; vessel_location /= np.max( vessel_location )
            holes_location = io.imread( self.holes ).astype(float)[ minimum:maximum, minimum:maximum, minimum:maximum ]; holes_location /= np.max( holes_location )

            self.diffusion_loc += - vessel_location + holes_location
            self.diffusion_loc[ self.diffusion_loc >= 1.0 ] = 1.0
            self.diffusion_loc[ self.diffusion_loc < 1.0 ] = 0.0
            del vessel_location, holes_location

        self.ijk = ( np.linspace(1, self.diffusion_loc.shape[0]-2, self.diffusion_loc.shape[0]-2) ).astype(int)

        return 0

    def create_mphage_location( self, minimum=0, maximum=-1 ):
        if os.path.exists( self.sim_dir + "marcophage_location.npy" ): #If continuing simulation, reloads
            self.mphage_loc = np.load( self.sim_dir + "macrophage_location.npy" )
        else:
            self.mphage_loc = 0.
        return 0

    def create_nucl_location( self, minimum=0, maximum=-1 ):
        if os.path.exists( self.sim_dir + "nucleus_location.npy" ): #If continuing simulation, reloads
            self.mphage_loc = np.load( self.sim_dir + "nucleus_location.npy" )
        else:
            self.mphage_loc = 0.
        return 0

    def initialize( self, minimum=0, maximum=-1 ):
        self.create_flow_location( minimum, maximum )
        self.create_source_location( minimum, maximum )
        self.create_mphage_location( minimum, maximum )
        self.create_nucl_location( minimum, maximum )
        self.create_diffusion_location( minimum, maximum )
        self.solution = np.zeros( np.asarray( self.diffusion_loc ).shape )
        return 0

    #--------------SIMULATION-------------
    #Explain each one

    def diffusion(self):
        un = np.copy( self.solution[:,:,:] )
        #un = self.solution

        self.solution[self.ijk,:,:] += self.diffusion_loc[self.ijk,:,:]*( self.d_co*self.dt*self.diffusion_loc[self.ijk+1,:,:]*( un[self.ijk+1,:,:]-un[self.ijk,:,:] ) )/(self.dx**2)

        self.solution[self.ijk,:,:] += self.diffusion_loc[self.ijk,:,:]*( self.d_co*self.dt*self.diffusion_loc[self.ijk-1,:,:]*( un[self.ijk-1,:,:]-un[self.ijk,:,:] ) )/(self.dx**2)

        self.solution[:,self.ijk,:] += self.diffusion_loc[:,self.ijk,:]*( self.d_co*self.dt*self.diffusion_loc[:,self.ijk+1,:]*( un[:,self.ijk+1,:]-un[:,self.ijk,:] ) )/(self.dy**2)

        self.solution[:,self.ijk,:] += self.diffusion_loc[:,self.ijk,:]*( self.d_co*self.dt*self.diffusion_loc[:,self.ijk-1,:]*( un[:,self.ijk-1,:]-un[:,self.ijk,:] ) )/(self.dy**2)

        self.solution[:,:,self.ijk] += self.diffusion_loc[:,:,self.ijk]*( self.d_co*self.dt*self.diffusion_loc[:,:,self.ijk+1]*( un[:,:,self.ijk+1]-un[:,:,self.ijk] ) )/(self.dz**2)

        self.solution[:,:,self.ijk] += self.diffusion_loc[:,:,self.ijk]*( self.d_co*self.dt*self.diffusion_loc[:,:,self.ijk-1]*( un[:,:,self.ijk-1]-un[:,:,self.ijk] ) )/(self.dz**2)

        #Periodic Boundary Conditions
        self.solution[0,:,:] += self.diffusion_loc[0,:,:]*( self.d_co*self.dt*self.diffusion_loc[1,:,:]*( un[1,:,:]-un[0,:,:] ) + self.d_co*self.dt*self.diffusion_loc[-1,::-1,::-1]*( un[-1,::-1,::-1]-un[0,:,:] ))/(self.dx**2)

        self.solution[:,0,:] += self.diffusion_loc[:,0,:]*( self.d_co*self.dt*self.diffusion_loc[:,1,:]*( un[:,1,:]-un[:,0,:] ) + self.d_co*self.dt*self.diffusion_loc[::-1,-1,::-1]*( un[::-1,-1,::-1]-un[:,0,:] ))/(self.dy**2)

        self.solution[:,:,0] += self.diffusion_loc[:,:,0]*( self.d_co*self.dt*self.diffusion_loc[:,:,1]*( un[:,:,1]-un[:,:,0] ) + self.d_co*self.dt*self.diffusion_loc[::-1,::-1,-1]*( un[::-1,::-1,-1]-un[:,:,0] ))/(self.dz**2)

        self.solution[-1,:,:] += self.diffusion_loc[-1,:,:]*( self.d_co*self.dt*self.diffusion_loc[-2,:,:]*( un[-2,:,:]-un[-1,:,:] ) + self.d_co*self.dt*self.diffusion_loc[0,::-1,::-1]*( un[0,::-1,::-1]-un[-1,:,:] ))/(self.dx**2)

        self.solution[:,-1,:] += self.diffusion_loc[:,-1,:]*( self.d_co*self.dt*self.diffusion_loc[:,-2,:]*( un[:,-2,:]-un[:,-1,:] ) + self.d_co*self.dt*self.diffusion_loc[::-1,0,::-1]*( un[::-1,0,::-1]-un[:,-1,:] ))/(self.dy**2)

        self.solution[:,:,-1] += self.diffusion_loc[:,:,-1]*( self.d_co*self.dt*self.diffusion_loc[:,:,-2]*( un[:,:,-2]-un[:,:,-1] ) + self.d_co*self.dt*self.diffusion_loc[::-1,::-1,0]*( un[::-1,::-1,0]-un[:,:,-1] ))/(self.dz**2)

        del un
        return 0

    def neumann_condition( self ):
        self.solution += self.concentration_time() * self.flow_loc
        return 0

    def dirichlet_condition( self ):
        self.solution += - self.solution * self.source_loc + self.concentration_time() * self.source_loc

        return 0

    #--------------SIMULATION-------------

    def simulation_step( self ):
        self.diffusion()
        self.dirichlet_condition()
        #self.neumann_condition()
        #self.
        return 0

    def update_simulation( self ):
        return 0

    #--------------SAVING-------------

    def save_sim( self ):

        return 0
