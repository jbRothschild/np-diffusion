import numpy as np
import skimage.io as io
import time

def params(v):
    #parameters for the diffusion

    #vis = 0.01 #DIffusion coefficient um^2/s
    vis = v #Diffusion coefficient in um^2/s
    count = '/lastTime_seconds.npy'
    size = 610
    dx = 2.; dy = 2.; dz = 2. #1 micrometer
    total_time = 3600.
    dt = 1.0 #dx*dx/(2.*vis) #Time steps of seconds dt < dx^2/2*D
    nu = 0.002 # nu = dudx

    #IMPORTANT: ADD A COMMENT FOR EACH RUN
    comment = 'Diffusion with the proper diffusion coefficient, 5000 holes.'

    return vis, size, dx, dy, dz, total_time, dt, nu, comment

def create_source_location(load_dir, data_dir, filename, other = None):
    #File which loads the file with dirichlet conditions
    source_location = io.imread(load_dir + filename).astype(float)
    source_location /= np.max(source_location)

    np.save(data_dir + "/source_location", source_location)
    #np.save(data_dir + "/source_location", source_location[150:-150,150:-150,150:-150])

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
    tic1 = time.time()
    vessel_location = io.imread(load_dir + filename).astype(float)
    vessel_location /= np.max(vessel_location)
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
    np.save(data_dir + "/flow_location", flow_location)
    #np.save(data_dir + "/flow_location", flow_location[150:-150,150:-150,150:-150])
    toc1 = time.time()
    print toc1-tic1, "sec elapsed creating flow..."

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
    diffusion_location /= np.max(diffusion_location)
    vessel_location = io.imread(load_dir + other[0]).astype(float)
    vessel_location /= np.max(vessel_location)
    source_location = io.imread(load_dir + other[1]).astype(float)
    source_location /= np.max(source_location)

    np.save(data_dir + "/diffusion_location", diffusion_location - vessel_location + source_location)
    #np.save(data_dir + "/diffusion_location", diffusion_location[150:-150,150:-150,150:-150]-vessel_location[150:-150,150:-150,150:-150] + source_location[150:-150,150:-150,150:-150])#got to take out vasculature but add source if there are any.

def model(load_dir, data_dir):
    """
    Function that creates the different arrays that set the geometry of our diffusion landscape.

    Args:
        load_dir(string): directory with all the data files
        data_dir(string): directory where all the manipulated arrays are stored after creation
    Returns:
        None
    """
    tic = time.time()
    SL = create_source_location(load_dir, data_dir, 'UT16-T-stack3-Sept10_iso_5000gaps.tif')
    FL = create_flow_location(load_dir, data_dir, 'UT16-T-stack3-Sept10_iso_vesthresh-cropped.tif')
    DL = create_diffusion_location(load_dir, data_dir, 'UT16-T-stack3-Sept10_iso_tissueboundary-cropped.tif', other = ['UT16-T-stack3-Sept10_iso_vesthresh-cropped.tif','UT16-T-stack3-Sept10_iso_5000gaps.tif'])
    toc = time.time()
    print toc-tic, "sec elapsed creating model..."

def concentration_time(time_point):
    """
    Function that calculates the change in concentration in the blood vessel as a function of time (according to Syed et co. observations)

    Args:
        time(float): time in hours
    Returns:
        The concentration
    """
    #return 1.0 #if we make concetration in blood vessel fixed
    return 0.7521*np.exp(-1.877*time_point) + 0.2479*np.exp(-0.1353*time_point)

def neumann_flow(un, flow_location, i, dt, nu, dx):
    #contribution due to neumann flow_location.
    #return concentration_time(i*dt/3600.)*flow_location*nu*2*dx
    return 0 #set when flow location is 0

def set_dirichlet(source_location, i, dt):
    #contribution due to dirichlet source terms
    return concentration_time(i*dt/3600.)*source_location
    #return 0 #set when there are no source locations
