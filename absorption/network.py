import numpy as np
from scipy.integrate import solve_ivp

def ben_net(t,y):
    """
    Args :
        t : time points
        y[0] : Nanop ; y[1] : Kupffer surface ; y[2] : Inside Liver ; y[3] : Tumor ;
    """
    sol = np.zeros(y.shape)
    kt = 0.7; kk = 0.5; ki = 0.9; maxK = 325.; #verify units of everything

    sol[0] = - ( kk*maxK - kk*y[1] + kt ) * y[0]
    sol[1] = ( kk*maxK - kk*y[1] ) * y[0] - ki*y[1]
    sol[2] = ki*y[1]
    sol[3] = kt * y[0]


    return sol

class Models:

    def __init__(self, initial_concentration, ntwk):
        self.init_conc = initial_concentration
        self.init_time = 0.001
        self.final_time = 24.
        self.network = ntwk
        self.time_eval = list(np.arange(self.init_time, self.final_time, (self.final_time-self.init_time)/1000.))
        self.species = (r'$T_{pr}$', r'$C_{IL2}$', r'$T_{reg}$', r'$T_{ac}$', r'$ag$')

    def change_time(self, begin, end):
        self.init_time = begin
        self.final_time = end

    def change_init_conc(self, new_conc):
        self.init_conc = new_conc

    def change_time_eval(self, intervals):
        self.time_eval = list(np.arange(self.init_time, self.final_time, (self.final_time-self.init_time)/intervals))

    def solve(self):
        self.sol = solve_ivp(self.network, [self.init_time, self.final_time], self.init_conc, t_eval=self.time_eval)
