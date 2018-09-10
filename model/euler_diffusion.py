import write_data as wd
import diffusion as dif
import time

import sys, os
import numpy as np
from skimage import io

#Argument is the diffusion coefficient for now
import argparse

parser = argparse.ArgumentParser(description='Submitting different diffusion parameters')
parser.add_argument('-D', metavar='D', type=float, action='store', default=5000, required=False, help='number of holes')
#Namespace with the arguments
args = parser.parse_args()





def main(sim_name, load, holes):
    #===============Model selection==================================
    if load == True:
        import move_holes as mod
    else:
        import custom_model as mod
    if not os.path.exists('../data/'):
        os.makedirs('../data/')
    #Set directory where the data will be saved. Also set the loading directory (../ChanLan/)
    data_dir = "../data/sim_" + sim_name + str(holes)#remote use
    load_dir = '../ChanLab/'
    count = '/lastTime_seconds.npy'
    #data_dir = $HOME #on Scinet
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    #=================Model + Parameter Creation=====================
    #This is where we create our models from the different functions in either data_model.py or custom_model.py
    if not os.path.exists(data_dir + count):
        #Creates models and parameters for models
        #Writes these to a file in the data folder. Be sure to add a comment on the model so we can understand what it is in the future.
        mod.model(load_dir, data_dir, 5000)
        #mod.model(load_dir, data_dir, holes)
    vis, size, dx, dy, dz, total_time, dt, nu, comment = mod.params(1.5)
    if not os.path.exists(data_dir + "/params.txt"):
        wd.write_params_file(data_dir, dx, dy, dz, total_time, dt, vis, nu, comment)

    #===============Load======================================
    #We load up models

    diffusion_location = np.load(data_dir + "/diffusion_location.npy") #diffusion_
    source_location = np.load(data_dir + "/source_location.npy") #location of fixed concentration
    num_holes = np.sum(source_location)
    flow_location = np.load(data_dir + "/flow_location.npy") #can be more than 1 (number of directions flow is coming in from)
    if os.path.exists(data_dir + "/holes_location.npy"):
        holes_location = np.load(data_dir + "/holes_location.npy")
        pos_holes = np.sum( holes_location )

    #===============Initialization=============================
    if not os.path.exists(data_dir + count):
        np.save(data_dir + count, np.asarray(0))
        np.save(data_dir + "/diff_0sec.npy", source_location*mod.concentration_time(0))
        np.save(data_dir + "/time_sum.npy", np.array([[0.0],[0.0]]))

    ijk = (np.linspace(1, diffusion_location.shape[0]-2, diffusion_location.shape[0]-2)).astype(int) #part of domain

    #Basically checks at what step we're at
    initial = np.load(data_dir + count)
    u = np.load(data_dir + "/diff_" + str(initial) + "sec.npy")
    timeSum = np.load(data_dir + "/time_sum.npy")

    #================Euleur's method============================
    tic = time.time()
    for i in np.arange(initial/dt+1,total_time/dt+1): #run simulation from time
        tic1 = time.time()
        un = u[:,:,:]

        dif.diffusion(u, un, ijk, diffusion_location, vis, dt, dx, dy, dz, mod) #diffusion of particles within the diffusion_location
        dif.dirichlet_source_term(u, source_location, i, dt, mod) #fixed source locations, dirichlet conditions
        dif.neumann_source_term(u, un, flow_location, i, dt, nu, dx, mod) #locations where there are neumann boundary conditions

        #Updating certain diffusion parameters
        mod.update_diff(holes_location, source_location, i*dt, total_time, holes, pos_holes, num_holes)

        #--------------------Saving Data-------------------
        """
        save_time_2D = 60. #number of seconds to elapse when saving 2D images
        if i*dt in np.arange(0,total_time+1,save_time_2D):
            wd.save_run_2D(i*dt, u[u.shape[0]/2,:,:], data_dir) #u.shape[0]/2 means it's in the middle
        """

        save_time = 300. #number of seconds to elapse when saving 3D images
        if i*dt in np.arange(0,total_time+1,save_time):
            wd.save_run(i*dt, u, data_dir, count)
            wd.save_run_2D(i*dt, u[u.shape[0]/2,:,:], data_dir)

        #saving
        if timeSum[0,timeSum.shape[1]-1] < i*dt:
            timeSum = np.append(timeSum,[[i*dt],[np.sum(u)]], axis=1)
            np.save(data_dir + "/time_sum.npy", timeSum)
        #-------------------------------------------


        toc1 = time.time()
        print toc1-tic1, "sec for roughly one time step..."

    toc = time.time()
    print toc-tic, "sec for Euler diffusion !"

if __name__ == "__main__":
    main(sim_name='move_holes_time', load=True, holes=vars(args)['D'])
