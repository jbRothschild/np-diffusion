import sys
import numpy as np
import os
from skimage import io

cwd = os.getcwd() + "/Sim"

def dirichlet(size, hole_radius, vessel_radius):
    """
    Function that saves a 3D array of the Dirichlet boundary sources. Note that for now sources are all the same value

    Args:
        size(int): The size of the 3D array along one dimension
    Returns:
        bc_D(array[size,size,size]): Array of source terms in the model
    """
    bc_D = np.zeros((size,size,size))

    bc_D[0,:,:] = 0; bc_D[:,0,:] = 0; bc_D[:,:,0] = 0
    bc_D[-1,:,:] = 0; bc_D[:,-1,:] = 0; bc_D[:,:,-1] = 0

    #------HOLE at 150,160,150------
    bc_D[150,160,150] = 1.0
    #-------------------------------

    return bc_D

def neumann(size, hole_radius, vessel_radius):
    """
    Function  that saves a 3D array of the Neumann boundary locations

    Args:
        size(int): The size of the 3D array along one dimension
    Returns:
        uref(array[size,size,size]): Array of locations that have a Neumann boundary conditions
    """

    uref = np.zeros((size,size,size))

    radius = 10.
    for i in range(0,size):
        for j in range(0,size):
            for k in range(0,size):
                if ((j-int(size/2))**2 + (i-int(size/2))**2 <= vessel_radius**2):
                    uref[i,j,k] = 0.0
                else:
                    uref[i,j,k] = 1.0
    uref[150,160,150] = 1.0

    return uref

def tiff_load(filename):
    """
    Function that loads a TIFF 3D image and outputs its 3D array

    Args:
        filename(string): the name of the file to load
    Returns:
        The array
    """
    
    return io.imread(filename)

def concentration_time(time):
    """
    Function that calculates the change in concentration in the blood vessel as a function of time

    Args:
        time(int): time in seconds
    Returns:
        The concentration
    """
    #return 1.0
    return 0.7521*np.exp(-1.877*time) + 0.2479*np.exp(-0.1353*time)

def main(action='load', size=301, hole_radius=1, vessel_radius=10, cwd = cwd, fileN='none', fileD='none', file_domain='none'):
    #====================Grid constuction=====================
    if action == 'load':
        bc_D = tiff_load(fileD).astype(float)
        bc_N = 1 - tiff_load(fileN).astype(float) + bc_D
        uref_D = tiff_load(file_domain).astype(float)

    else:
        bc_N = neumann(size, hole_radius, vessel_radius)
        bc_D = dirichlet(size, hole_radius, vessel_radius)
        #Location of Internal and Boundary Dirichlets conditions
        uref_D = np.zeros((size,size,size)) + 1
        uref_D[0,:,:] = 0.0;  uref_D[:,0,:] = 0.0; uref_D[:,:,0] = 0.0
        uref_D[-1,:,:] = 0.0; uref_D[:,-1,:] = 0.0; uref_D[:,:,-1] = 0.0

    #Main Arrays
    np.save(cwd + "/Neumann", bc_N)
    np.save(cwd + "/Domain", uref_D-bc_D)
    np.save(cwd + "/Dirichlet", bc_D)


#main('load', size=301, hole_radius=1, vessel_radius=10, cwd=cwd, fileN=os.getcwd() + '/ChanLab/' + 'UT16-T-stack3-Sept10_iso_vesthresh-cropped.tif', fileD= os.getcwd() + '/ChanLab/' + 'UT16-T-stack3-Sept10_iso_gaps-cropped.tif', file_domain= os.getcwd() + '/ChanLab/' + 'UT16-T-stack3-Sept10_iso_tissueboundary-cropped.tif')
#main('create', size=301, hole_radius=1, vessel_radius=10, cwd=cwd)