import numpy as np
from scipy.integrate import solve_ivp

def dif_coef(np_size):
    kb = 1.4*10**(-23)
    T = 310
    nu = 3.2*10**(-3)
    return ( kb*T ) / ( 6*np.pi*nu*np_size*10**(-9) ) * 10**(13) # converting um^2 to nm^2

def ben_net(t, y, *args):
    """
    Args :
        t : time points
        y[0] : Nanop ; y[1] : Kupffer surface ; y[2] : Inside Liver ; y[3] : Tumor ;
    """
    sol = np.zeros(y.shape)
    dosage = args[0]
    numKpf = args[1] #number of kupffer cells total
    numRec= args[2] #number of receptors total
    npRadius = args[3] # nm
    kpfRadius = 10000  # nm
    volBlood = 1.46*10**(18) # nm**3
    recRadius = 500. # nm radius

    Jon = ( 4*np.pi*dif_coef(npRadius)*kpfRadius*recRadius ) / ( volBlood*( recRadius*y[1]/numRec + np.pi*kpfRadius ) ) * y[0] * y[1]
    k = 1
    #Jon = k*0.5*y[0]*y[1]
    koff = k*0.01; kin = k*0.20; kren = k*0.15; kCancer = k*0.005; kBody = k*0.03;#verify units of everything
    Jin = kin*y[2]
    Jren = kren*y[3]

    sol[0] = - Jon - ( kCancer + kBody )*y[0] + koff*y[2]
    sol[1] = - Jon + koff*y[2] + Jren
    sol[2] =  - koff*y[2] - Jin + Jon
    sol[3] = Jin - Jren
    sol[4] = Jren
    sol[5] = kCancer*y[0]
    sol[6] = kBody*y[0]

    print(dif_coef(npRadius)*kpfRadius*recRadius )

    return sol

def previous_ben_net(t, y, *args):
    """
    Args :
        t : time points
        y[0] : Nanop ; y[1] : Kupffer surface ; y[2] : Inside Liver ; y[3] : Tumor ;
    """
    sol = np.zeros(y.shape)
    dosage = args[0]
    numKpf = args[1] #number of kupffer cells total
    numRec= args[2] #number of receptors total
    npRadius = args[3] # nm
    kpfRadius = 10000  # nm
    volBlood = 1.46*10**(18) # nm**3
    recRadius = 5. # nm radius

    Jon = ( 4*np.pi*dif_coef(npRadius)*kpfRadius*recRadius ) / ( recRadius*y[1]/numRec + np.pi*kpfRadius ) * y[0] * y[1]
    k = 10*(-20)
    #Jon = k*y[0]*y[1]
    koff = k; kin = k; kren = k; kCancer = k; kBody =k;#verify units of everything
    Jin = kin*y[2]
    Jren = kren*y[3]

    sol[0] = - Jon - ( kCancer + kBody )*y[0] + koff*y[2]
    sol[1] = -Jon + koff*y[2] + Jren
    sol[2] =  - koff*y[2] - Jin + Jon
    sol[3] = Jin - Jren
    sol[4] = Jren
    sol[5] = kCancer*y[0]
    sol[6] = kBody*y[0]
    print(Jon)

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
