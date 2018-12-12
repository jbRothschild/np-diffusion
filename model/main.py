import sys, os, time
import write_data as wd
import numpy as np
from skimage import io

#Argument is the diffusion coefficient for now
import argparse

parser = argparse.ArgumentParser(description='Submitting different diffusion parameters')
parser.add_argument('-m', metavar='M', type=str, action='store', default='parent_model', required=False, help='model passed to import')
parser.add_argument('-p', metavar='p', nargs='*', action='store', default=[], required=False, help='Additional parameters to be passed on for the simulation')
#Namespace with the arguments
args = parser.parse_args()


def main(model, **data):
    #===============Model selection==================================
    if not os.path.exists('../sim/'):
        os.makedirs('../sim/')

    mod = __import__(model)

    sim_model = mod.Model(**data)

    #=================Model + Parameter Creation=====================
    #This is where we create our models from the different functions in either data_model.py or custom_model.py
    sim_model.initialize()
    sim_model.solution = np.copy( sim_model.source_loc )

    #================Euleur's method============================

    tic = time.time()
    for i in np.arange( sim_model.time/sim_model.dt + 1/sim_model.dt, sim_model.total_time/sim_model.dt + 1/sim_model.dt ): #run from time saved previously
        tic1 = time.time()
        sim_model.simulation_step()

        sim_model.time = i*sim_model.dt

        #--------------------Saving Data-------------------
        if sim_model.time in np.arange(0 , sim_model.total_time + 1, sim_model.save_data_time):
            sim_model.save_sim()

        #saving the sum at each time step.
        if sim_model.timeSum[0,sim_model.timeSum.shape[1]-1] < sim_model.time:
            sim_model.save_time_sum()

        #-------------------------------------------

        #CHange to a for loop, for any updates that might happen and their time
        if sim_model.time in np.arange( 0, sim_model.total_time, sim_model.update_time):
            sim_model.update_simulation()

        toc1 = time.time()
        print toc1 - tic1, "sec for roughly one time step..."
    toc = time.time()
    print toc - tic, "sec for total simulation."

if __name__ == "__main__":
    parameter=vars(args)['p']
    #hopping model
    if vars(args)['m'] == 'hopping_model':
        data = {'sim_dir':parameter[0], 'load_num':parameter[1], 'load_datafile':parameter[2], 'domain':parameter[6], 'vessel':parameter[5], 'holes':parameter[4], 'gen_holes':parameter[3], 'update_time':int(parameter[7]), 'dx':float(parameter[8]), 'dy':float(parameter[8]), 'dz':float(parameter[8])}
        #data = {'sim_dir':parameter[0], 'update_time':int(parameter[1]), 'tot_time':int(parameter[2]), 'save_data_time':int(parameter[3])}
    elif vars(args)['m'] == 'macrophage_model':
        data = {'sim_dir':parameter[0], 'update_time':int(parameter[1]), 'tot_time':int(parameter[2]), 'save_data_time':int(parameter[3])}
    elif vars(args)['m'] == 'custom_model':
        data = {'sim_dir':vars(args)['m']}

    main(model=vars(args)['m'], **data)
