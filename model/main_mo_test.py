import write_data as wd
import diffusion as dif
import time

import sys, os
import numpy as np
from skimage import io

#Argument is the diffusion coefficient for now
import argparse

import datetime

runtime = datetime.datetime.now()
folder_suffix = runtime.strftime('%Y%m%d_%H%M%S')

parser = argparse.ArgumentParser(description='Submitting different diffusion parameters')
parser.add_argument('-m', metavar='M', type=str, action='store', default='macrophage_model_test', required=False, help='Additional parameters to be passed on for the simulation')
parser.add_argument('-p', metavar='p', type=float, action='store', default=[folder_suffix], required=False, help='Additional parameters to be passed on for the simulation')
#Namespace with the arguments
args = parser.parse_args()


def main(model, parameter):
    #===============Model selection==================================
    mod = __import__(model) #Make sure model is a python file that
    if not os.path.exists('../data/'):
        os.makedirs('../data/')

    #Set directory where the data will be saved. Also set the loading directory for certain diffusion geometries (../ChanLan/)
    data_dir = "../data/sim_" + str(model) + '_' + str(parameter)
    load_dir = '../ChanLab/'

    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    #=================Model + Parameter Creation=====================
    #This is where we create our models from the different functions in either data_model.py or custom_model.py
    count = '/lastTime_seconds.npy'
    vis, dx, dy, dz, total_time, dt, nu, save_time, model_var, update_time, model_var_comment, comment = mod.params(parameter)
    if not os.path.exists(data_dir + count):
        #Creates models and parameters for models
        #Writes these to a file in the data folder. Be sure to add a comment on the model so we can understand what it is in the future.
        mod.model(load_dir, data_dir, model_var, parameter)
    #---------------------------------------------------------------------
    wd.write_params_file(data_dir, dx, dy, dz, total_time, dt, vis, nu, comment, model_var, model_var_comment)

    #===============Load======================================
    #We load up the different domains defined in models
    diffusion_location = np.load(data_dir + "/diffusion_location.npy") #diffusion locations
    source_location = np.load(data_dir + "/source_location.npy") #location of fixed concentration
    num_holes = np.sum(source_location)
    flow_location = np.load(data_dir + "/flow_location.npy") #can be more than 1 (number of directions flow is coming in from)
    #flow_location_mo = np.load(data_dir + "/flow_location_mo.npy") #need a new flow location for macrophages.
    # if os.path.exists(data_dir + "/holes_location.npy"): #If there are other locations of possible holes, we need this array
    holes_location = np.load(data_dir + "/holes_location.npy")
    macro_location = np.load(data_dir + "/macro_location.npy")
    macro_source_location = np.load(data_dir + "/macro_source_location.npy")

    #===============Initialization=============================
    if not os.path.exists(data_dir + count): #Check if there is saved timepoint of simulation, if it isn't we set the time to 0
        np.save(data_dir + count, np.asarray(0))
        np.save(data_dir + "/diff_0sec.npy", source_location*mod.concentration_time(0)) #Save initial solution
        np.save(data_dir + "/time_sum.npy", np.array([[0.0],[0.0]])) #Save initial concentration and time (0,0)

    ijk = (np.linspace(1, diffusion_location.shape[0]-2, diffusion_location.shape[0]-2)).astype(int) #part of domain to sum over

    #Basically checks at what step we're at
    initial = np.load(data_dir + count)
    u = np.load(data_dir + "/diff_" + str(initial) + "sec.npy")
    timeSum = np.load(data_dir + "/time_sum.npy")

    #================Euleur's method============================
    
    tic = time.time()
    for i in np.arange(initial/dt+1,total_time/dt+1): #run sother = []imulation from time
        tic1 = time.time()
        un = u[:,:,:]

        dif.diffusion(u, un, ijk, diffusion_location, vis, dt, dx, dy, dz, mod) #diffusion of particles within the diffusion_location
        dif.dirichlet_source_term(u, source_location, i, dt, mod) #fixed source locations, dirichlet conditions
        dif.neumann_source_term(u, un, flow_location, i, dt, nu, dx, mod) #locations where there are neumann boundary conditions
        #dif.neumann_source_term_mo(u, un, flow_location_mo, i, dt, nu, dx, mod) # locations where there are macrophage neumann boundry conditions
    
        
        #Updating certain diffusion parameters
        if i*dt in np.arange(0,total_time+1,update_time):
            mod.update_diff(holes_location, source_location, data_dir) #function arguments will need to change, depending on the model

        #--------------------Saving Data-------------------
        if i*dt in np.arange(0,total_time+1,save_time):
            wd.save_run(i*dt, u, data_dir, count)
            wd.save_run_2D(i*dt, u[u.shape[0]/2,:,:], data_dir)

        #saving the sum at each time step.
        if timeSum[0,timeSum.shape[1]-1] < i*dt:
            timeSum = np.append(timeSum,[[i*dt],[np.sum(u)]], axis=1)
            np.save(data_dir + "/time_sum.npy", timeSum)
            print "         >> Sum this step", np.sum(u)
            #print "number of holes this step", np.sum(source_location)
        #-------------------------------------------

        toc1 = time.time()
        print toc1-tic1, "sec for roughly one time step..."

if __name__ == "__main__":
    main(model=vars(args)['m'], parameter=vars(args)['p'])
