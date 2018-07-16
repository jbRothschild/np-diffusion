import numpy as np

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
    source_location = np.load(load_dir + filename)

    np.save(data_dir + "/source_location", source_location)

def create_flow_location(load_dir, data_dir, filename, other = None):
    flow_location = np.load(load_dir + file)
    for
    np.save(data_dir + "/flow_location", flow_location)

def create_diffusion_location(load_dir, data_dir, filename, other = None):
    diffusion_location = np.load(load_dir + file)
    
    np.save(data_dir + "/diffusion_location", diffusion_location)

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
    DL = create_diffusion_location(load_dir, data_dir, 'UT16-T-stack3-Sept10_iso_tissueboundary-cropped.tif', other = SL)

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
