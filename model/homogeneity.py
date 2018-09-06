import numpy as np
import skimage.morphology as morph
import sys, os

def skeleton_dist(data, vessel, domain):
    dist = []
    return dist


def rev_diffusion_dist(data, vessel, domain = []):
    """
    Function that does a naive reverse diffusion, moving 1/6 of the concentration at each point into the locations adjacent. Sticks to the vessel walls

    Input
        data(array,3d): diffusion data_array
        vessel(array,3d): vasculature data with 1.0 wherever there's a vessel, an be skeletonized data too!
    Output
        dist?
    """
    #Pseudo reverse diffusion
    data_temp = data
    for t in np.arange(0,20):
        for i in np.arange(1,data.shape[0]):
            for j in np.arange(1,data.shape[1]):
                for k in np.arange(1,data.shape[2]):
                    if vessel[i,j,k] == 0:
                        temp = data[i,j,k]/6
                        data_temp[i+1,j,k] = temp
                        data_temp[i-1,j,k] = temp
                        data_temp[i,j+1,k] = temp
                        data_temp[i,j-1,k] = temp
                        data_temp[i,j,k+1] = temp
                        data_temp[i,j,k-1] = temp
        data = data_temp

    #Find distribution of particles on vessel surface
    dist = []
    for i in np.arange(0,data.shape[0]+1):
        for j in np.arange(0,data.shape[1]+1):
            for k in np.arange(0,data.shape[2]+1):
                if vessel[i,j,k] > 0 and data[i,j,k] > 0.0:
                    dist.append(data[i,j,k])
    return dist

def heterogen_score(dist):
    variance = np.var(dist)
    mean = np.mean(dist)
    return variance/mean**2

def main(sim_name, domainfile, sourcefile, datafile, method, use_skel):
    domain = np.load(sim_name + domainfile).astype(int)
    source = np.load(sim_name + sourcefile).astype(int)
    vessel = 1 - domain - source #since what we're reading is the diffusion domain file

    if not os.path.exists(sim_name + '/skeleton_vessel.npy'):
        skel = morph.skeletonize_3d(vessel)
        np.save(sim + '/skeleton_vessel.npy', skel)
    if use_skel == True:
        vessel = np.load(sim_name + '/skeleton_vessel.npy')

    H_score = []

    for i in np.arange(0,data.shape):
        data = np.load(sim_name + datafile[i])
        distribution = method(data, vessel, domain-source)
        H_scores.append(heterogen_score(distribution))

    print H_scores

    return 0

if __name__ == "__main__":
    main(sim_name = '../data/try', domainfile = 'diffusion_try.npy', sourcefile = 'source_try.npy', datafile = '/data_try.npy', method = rev_diffusion_dist, use_skel=False)
    #main(sim_name = '../data/holesUT16', domainfile = '/diffusion_location.npy', sourcefile = '/source_location.npy', datafile = ['diff_holes00300.npy','diff_holes00500.npy','diff_holes01000.npy','diff_holes03000.npy','diff_holes05000.npy','diff_holes10000.npy','diff_holes30000.npy','diff_holes50000.npy',], method = rev_diffusion_dist, use_skel=False)
