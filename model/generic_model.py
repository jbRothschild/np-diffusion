import time

import sys, os
import numpy as np
from skimage import io

from parameters import DIF_COEF, TOT_TIME, TIME_STEP, GLOB_DX, GLOB_DY, GLOB_DZ, VISC

class Model:
    def __init__(self, d=DIF_COEF, vis=VISC, time=TOT_TIME, dt=TIME_STEP, dx=GLOB_DX, dy=GLOB_DY, dz=GLOB_DZ):
        self.diff = diff
        self.vis = vis
        self.time = TOT_TIME
        self.dt = TIME_STEP
        self.dx = GLOB_DX
        self.dy = GLOB_DY
        self.dz = GLOB_DZ

    def unpack(self):
        return self.d, self.time, self.dt, self.dx, self.dy, self.dz

    def source_location(self):

    def flow_location(self):

    def diffusion_location(self):

    def concentration_time(self):

    def diffusion(self):

    def neumann_condition(self):

    def dirichlet_condition(self):

    def update_simulation(self):

    def simulation(self):

class HoppingModel(Model):
    def __init__(self, d=DIF_COEF, vis=VISC, time=TOT_TIME, dt=TIME_STEP, dx=GLOB_DX, dy=GLOB_DY, dz=GLOB_DZ):
        Model.__init__(self, d=DIF_COEF, vis=VISC, time=TOT_TIME, dt=TIME_STEP, dx=GLOB_DX, dy=GLOB_DY, dz=GLOB_DZ)

DEFAULT_MODEL = Model()
