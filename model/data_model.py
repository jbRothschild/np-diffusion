import numpy as np
import skimage.io as io

def params():
    #parameters for the diffusion

    vis = 0.01 #DIffusion coefficient um^2/s
    count = '/lastTime_seconds.npy'
    size = 301
    dx = 2; dy = 2; dz = 2 #1 micrometer
    time = 3600*4
    dt = 60 #Time steps of 30 seconds dt < dx^2/2D
    nu = 0.002 # nu = dudx

    #IMPORTANT: ADD A COMMENT FOR EACH RUN
    comment = 'First try'

    return vis, size, dx, dy, dz, time, dt, nu, comment

def create_source_location(load_dir, data_dir, filename, other = None):
    #File which loads the file with dirichlet conditions
    source_location = io.imread(load_dir + filename).astype(float)

    np.save(data_dir + "/source_location", source_location[:300,:300,:300])

def create_flow_location(load_dir, data_dir, filename, other = None):
    """
    Function that creates the location of flow. +1 for each place which is beside a vessel. can have -1 for certain otehr things I guess!

    Args:
        load_dir(string): directory with all the data files
        data_dir(string): directory where all the manipulated arrays are stored after creation
        filename(string): name of file which has vasculature.
        other(): Nothing for now.
    Returns:
        None
    """
    vessel_location = io.imread(load_dir + filename).astype(float)
    flow_location = np.zeros((vessel_location.shape[0], vessel_location.shape[1], vessel_location.shape[2]))
    for i in range(1,vessel_location.shape[0]-1):
        for j in range(1,vessel_location.shape[1]-1):
            for k in range(1,vessel_location.shape[2]-1):
                if vessel_location[i,j,k] == 1.0:
                    if vessel_location[i-1,j,k] == 0.0:
                        flow_location[i-1,j,k] += 1.0

                    if vessel_location[i+1,j,k] == 0.0:
                        flow_location[i+1,j,k] += 1.0

                    if vessel_location[i,j-1,k] == 0.0:
                        flow_location[i,j-1,k] += 1.0

                    if vessel_location[i,j+1,k] == 0.0:
                        flow_location[i,j+1,k] += 1.0

                    if vessel_location[i,j,k-1] == 0.0:
                        flow_location[i,j,k-1] += 1.0

                    if vessel_location[i,j,k+1] == 0.0:
                        flow_location[i,j,k+1] += 1.0
    np.save(data_dir + "/flow_location", flow_location[:300,:300,:300])

def create_diffusion_location(load_dir, data_dir, filename, other = None):
    """
    Function that creates the location of diffusion. For now that's anything that's not

    Args:
        load_dir(string): directory with all the data files
        data_dir(string): directory where all the manipulated arrays are stored after creation
        filename(string): name of file which has the tumor domain.
        other(): Nothing for now.
    Returns:
        None
    """
    diffusion_location = io.imread(load_dir + filename).astype(float)
    vessel_location = io.imread(load_dir + other).astype(float)
    np.save(data_dir + "/diffusion_location", diffusion_location[:300,:300,:300]-vessel_location[:300,:300,:300]) #got to take out vasculature but add source if there are any.

def model(load_dir, data_dir):
    """
    Function that creates the different arrays that set the geometry of our diffusion landscape.

    Args:
        load_dir(string): directory with all the data files
        data_dir(string): directory where all the manipulated arrays are stored after creation
    Returns:
        None
    """
    SL = create_source_location(load_dir, data_dir, 'UT16-T-stack3-Sept10_iso_gaps-cropped.tif')
    FL = create_flow_location(load_dir, data_dir, 'UT16-T-stack3-Sept10_iso_vesthresh-cropped.tif')
    DL = create_diffusion_location(load_dir, data_dir, 'UT16-T-stack3-Sept10_iso_tissueboundary-cropped.tif', other = 'UT16-T-stack3-Sept10_iso_vesthresh-cropped.tif')

def concentration_time(time):
    """
    Function that calculates the change in concentration in the blood vessel as a function of time (according to Syed et co. observations)

    Args:
        time(float): time in hours
    Returns:
        The concentration
    """
    #return 1.0
    return 0.7521*np.exp(-1.877*time) + 0.2479*np.exp(-0.1353*time)

def neumann_flow(un, flow_location, i, dt, nu):
    #contribution due to neumann flow_location.
    return flow_location*nu

def set_dirichlet(source, source_location, i, dt):
    #contribution due to dirichlet source terms
    return concentration_time(i*dt/3600.)*source*source_location
