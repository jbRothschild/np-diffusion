import write_data as wd
import diffusion as dif

import sys, os
import numpy as np
from skimage import io

def main(sim_name, load):
    #===============Model selection==================================
    if load == True:
        import data_model as mod
    else:
        import custom_model as mod
    if not os.path.exists('../data/'):
        os.makedirs('../data/')
    #Set directory where the data will be saved. Also set the loading directory (../ChanLan/)
    data_dir = "../data/sim_" + sim_name #remote use
    load_dir = '../ChanLab/'
    #data_dir = $HOME #on Scinet
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    #=================Model + Parameter Creation=====================
    #This is where we create our models from the different functions in either data_model.py or custom_model.py
    if not os.path.exists(data_dir + count):
        #Creates models and parameters for models
        #Writes these to a file in the data folder. Be sure to add a comment on the model so we can understand what it is in the future.
        mod.model(load_dir, data_dir)
        vis, size, dx, dy, dz, time, dt, nu, comment = mod.params()
        wd.write_params_file(data_dir, dx, dy, dz, time, dt, vis, nu, comment)

    #===============Load======================================
    #We load up models
    diffusion_location = np.load(data_dir + "/diffusion_location.npy") #diffusion_
    source_location = np.load(data_dir + "/source_location.npy") #location of fixed concentration
    flow_location = np.load(data_dir + "/flow_location.npy") #can be more than 1 (number of directions flow is coming in from)

    #===============Initialization=============================
    if not os.path.exists(data_dir + count):
        np.save(data_dir + count, np.asarray(0))
        np.save(data_dir + "/diff_0sec.npy", source_location*bd.concentration_time(0))

    ijk = (np.linspace(1, diffusion_location.shape[0]-2, diffusion_location.shape[0]-2)).astype(int) #part of domain

    #Basically checks at what step we're at
    initial = np.load(data_dir + count)
    u = np.load(data_dir + "/diff_" + str(initial) + "sec.npy")

    #================Euleur's method============================
    for i in range(int(initial/dt)+1,time/dt+1): #run simulation from time
        print i
        un = u[:,:,:]

        dif.diffusion(u, un, ijk, diffusion_location, vis, dt, dx, dy, dz, load) #diffusion of particles within the diffusion_location
        dif.dirichlet_source_term(u, source_location, i, dt, load) #fixed source locations, dirichlet conditions
        dif.neumann_source_term(u, un, flow, i, dt, nu, dx, load) #locations where there are neumann boundary conditions

        if i in range(0,time,(time/4)):
            wd.save_run(i*dt, u, data_dir)

if __name__ == "__main__":
    main(sim_name='Syed', load=True)
