import numpy as np
from scipy.integrate import solve_ivp

def dif_coef(np_size):
    kb = 1.4*10**(-23) # J/K = kg.m^2 / s^2.K
    T = 310 # K
    nu = 2.78*10**(-3) # Pa.s = kg / m.s^2
    D =  ( kb*T ) / ( 6*np.pi*nu*np_size*10**(-9) ) # m^2 / s
    return D*10**18 # converting m^2 to nm^2

def ben_net(t, y, *args):
    """
    Args :
        t : time points
        y[0] : Nanop ; y[1] : Kupffer surface ; y[2] : Inside Liver ; y[3] : Tumor ;
    """
    sol = np.zeros(y.shape)
    dosage = args[0][0]
    numKpf = args[1]; numRec= args[2] #number of kupffer cells total & number of receptors total
    npRadius = args[3]; kpfRadius = 7500; recRadius = 5.  # nm
    volBlood = 1.46*10**(18) + 0 # nm**3 + is for injection]

    Jon = ( ( 4*np.pi*dif_coef(npRadius)*kpfRadius*recRadius ) / ( volBlood*( recRadius*y[1]/numKpf + np.pi*kpfRadius ) ) ) * y[0] * y[1]
    k = 1; koff = k*0.000000001; kin = k*0.99; kren = k*0.99; kCancer = k*0.05; kBody = k*0.2;#verify units of everything
    Jin = kin*y[2]; Jren = kren*y[3]

    sol[0] = - Jon - ( kCancer + kBody )*y[0] + koff*y[2] # concentration in blood
    sol[1] = - Jon + koff*y[2] + Jren # number of receptors
    sol[2] =  - koff*y[2] - Jin + Jon # bound
    sol[3] = Jin - Jren # internalized and bound
    sol[4] = Jren # internalized proper
    sol[5] = kCancer*y[0] # in tumor
    sol[6] = kBody*y[0] # in rest of body
    #print(dosage/numRec)
    print(t,Jon/y[0],y[1]/numKpf)

    return sol

class Models:

    def __init__(self, initial_concentration, num_kup, num_rec, np_size, ntwk):
        self.init_conc = initial_concentration
        self.init_time = 0.001; self.final_time = 24.
        self.network = ntwk
        self.kupffer = num_kup; self.receptor = num_rec; self.np_size = np_size
        self.time_eval = list(np.arange(self.init_time, self.final_time, (self.final_time-self.init_time)/1000.))
        self.species = (r'$N_p$', r'$R$', r'$C_R$', r'$C_{RI}$', r'$C_I$', r'Tumor', r'Body')
        self.args = [ self.init_conc, self.kupffer, self.receptor, self.np_size ]

    def change_time(self, begin, end):
        self.init_time = begin
        self.final_time = end

    def change_init_conc(self, new_conc):
        self.init_conc = new_conc

    def change_time_eval(self, intervals):
        self.time_eval = list(np.arange(self.init_time, self.final_time, (self.final_time-self.init_time)/intervals))

    def solve(self):
        self.sol = solve_ivp(lambda t, y: self.network(t, y, *self.args), [self.init_time, self.final_time], self.init_conc, t_eval=self.time_eval)
