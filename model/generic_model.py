import sys, os, time
import numpy as np
from skimage import io

from parameters import DIF_COEF, VISC, TOT_TIME, TIME_STEP, GLOB_DX, GLOB_DY, GLOB_DZ, LOAD_DIR, DOMAIN, VESSEL, HOLES, MPHAGE, NUCL

class Model:
    def __init__(self,  sim_dir='../sim/generic_model', load_dir=LOAD_DIR, load_num="UT16-T-stack3-Sept10_iso_", load_datafile="particles-cropped.tif", diff=DIF_COEF, vis=VISC, tot_time=TOT_TIME, dt=TIME_STEP, dx=GLOB_DX, dy=GLOB_DY, dz=GLOB_DZ, number_holes=0):
        self.diff = diff; self.vis = vis #Diffusion coefficient and viscosity
        self.tot_time = TOT_TIME #total time for simulation
        self.dt = TIME_STEP; self.dx = GLOB_DX; self.dy = GLOB_DY; self.dz = GLOB_DZ #metric
        if not os.path.exists(sim_dir):
            os.makedirs(sim_dir)
        self.load_dir = load_dir+load_num; self.sim_dir = sim_dir
        self.conc_vessel = self.concentration_time(0.)
        self.datafile = self.load_dir + load_datafile
        self.domain = ; self.vessel = ; self.holes = ; self.mphage = ; self.nucl =
        self.number_holes = number_holes

        if os.path.exists(sim_dir+"timepoint.npy"): #If continuing simulation, reloads
            self.time = np.load(sim_dir+"timepoint.npy")
        else:
            self.time = 0.0

    def unpack(self):
        return self.d, self.vis, self.time, self.dt, self.dx, self.dy, self.dz

    def concentration_time(self, time_point):
        return 0.7521*np.exp(-1.877*self.time) + 0.2479*np.exp(-0.1353*self.time)

    #--------------INITIALIZATION-------------

    def initialize(self):
        self.create_flow_location(self)
        self.create_source_location(self)
        self.create_diffusion_location(self)
        self.create_mphage_location(self)
        self.create_nucl_location(self)
        return 0

    def create_source_location(self):
        #Creates source location
        if os.path.exists(self.sim_dir+"source_location.npy"): #If continuing simulation, reloads
            self.source_loc = np.load(self.sim_dir+"source_location.npy")
        else: #Creates new source, location
            holes_location = io.imread(self.holes).astype(float); holes_location /= np.max(self.holes_location)
            all_holes = np.sum( holes_location )
            self.source_loc = np.zeros( np.asarray(holes_location).shape )
            num_holes = self.number_holes
            #Select random locations
            for i in np.arange(0, holes_location.shape[0]):
                for j in np.arange(0, holes_location.shape[1]):
                    for k in np.arange(0, holes_location.shape[2]):
                        if (holes_location[i,j,k] > 0.0 and num_holes > 0):
                            prob = np.random.randint(0,all_holes)
                            all_holes -= 1.0
                            if prob < num_holes:
                                self.source_loc[i,j,k] += 1.0
                                num_holes -= 1
        del holes_location
        return 0

    def create_flow_location(self):
        #Location of where there is flow out of the vessel, an array with 1 just outside of teh vessel and 0 where elsewhere
        if os.path.exists(self.sim_dir+"flow_location.npy"): #If continuing simulation, reloads
            self.flow_loc = np.load(self.sim_dir+"flow_location.npy")
        else:
            vessel_location = io.imread(self.vessel).astype(float); vessel_location /= np.max(vessel_location)
            self.flow_loc = np.zeros((vessel_location.shape[0], vessel_location.shape[1], vessel_location.shape[2]))
        #Every locations near the vascularue gets +1#---------------------------------------------------------------------
        for i in range(1,vessel_location.shape[0]-1):
            for j in range(1,vessel_location.shape[1]-1):
                for k in range(1,vessel_location.shape[2]-1):
                    if vessel_location[i,j,k] == 1.0:
                        if vessel_location[i-1,j,k] == 0.0:
                            self.flow_loc[i-1,j,k] += 1.0
                        if vessel_location[i+1,j,k] == 0.0:
                            self.flow_loc[i+1,j,k] += 1.0
                        if vessel_location[i,j-1,k] == 0.0:
                            self.flow_loc[i,j-1,k] += 1.0macrophage
                        if vessel_location[i,j+1,k] == 0.0:
                            self.flow_loc[i,j+1,k] += 1.0macrophage
                        if vessel_location[i,j,k-1] == 0.0:
                            self.flow_loc[i,j,k-1] += 1.0
                        if vessel_location[i,j,k+1] == 0.0:
                            self.flow_loc[i,j,k+1] += 1.0
        del vessel_location
        return 0

    def diffusion_location(self):
        if os.path.exists(self.sim_dir+"flow_location.npy"): #If continuing simulation, reloads
            self.diffusion_loc = np.load(self.sim_dir+"flow_location.npy")
        else:
            tumor_location = io.imread(self.domain).astype(float)
            self.diffusion_loc = np.ones( np.asarray(tumor_location).shape ); diffusion_location /= np.max(diffusion_location)
            vessel_location = io.imread(self.vessel).astype(float); vessel_location /= np.max(vessel_location)
            holes_location = io.imread(self.holes).astype(float); holes_location /= np.max(holes_location)

            self.diffusion_loc +=  - vessel_location + holes_location
            del vessel_location, holes_location
            self.diffusion_loc[self.diffusion_loc > 1.0] = 1.0
        return 0

    def create_mphage_location(self):
        if os.path.exists(sim_dir+"marcophage_location.npy"): #If continuing simulation, reloads
            self.mphage_loc = np.load(sim_dir+"macrophage_location.npy")
        else:
            self.mphage_loc = 0.
        return 0

    def create_nucl_location(self):
        if os.path.exists(sim_dir+"nucleus_location.npy"): #If continuing simulation, reloads
            self.mphage_loc = np.load(sim_dir+"nucleus_location.npy")
        else:
            self.mphage_loc = 0.
        return 0

    #--------------SIMULATION-------------

    def diffusion(self):
        return 0

    def neumann_condition(self):
        self.solution += -self.solution*self.source_loc + self.concentration_time(self.time)*self.source_loc
        return 0

    def dirichlet_condition(self):
        self.solution += -self.solution*self.source_loc + self.concentration_time(self.time)*self.source_loc
        return 0

    def update_simulation(self):
        return 0

    def simulation_step(self):
        self.diffusion()
        self.neumann_condition()
        self.dirichlet_condition()
        return 0
