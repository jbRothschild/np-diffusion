import numpy as np
import skimage.io as io
import time
import write_data as wd

def params(other = []):
    #parameters for the diffusion

    #vis = 0.01 #DIffusion coefficient um^2/s
    vis = 1.5 #Diffusion coefficient in um^2/s
    count = '/lastTime_seconds.npy'
    dx = 2.; dy = 2.; dz = 2. #1 micrometer
    total_time = 24*3600.
    dt = 1.0 #dx*dx/(2.*vis) #Time steps of seconds dt < dx^2/2*D
    nu = 0.002 # nu = dudx

    save_time = 24*300. #how long we wait until we save
    update_time = 6*300 #how often updates happen
    model_var = [50000/(5*5*5)] #Model variant. In this model: [hole number]. ##Note these can change depending on what we're doing
    model_var_comment = '[number of holes]'
    #---------------------------------------------------------------------
    #IMPORTANT: ADD A COMMENT FOR EACH RUN
    comment = 'Diffusion with the proper diffusion coefficient, 50000 holes in total image which is 5*5*5 times larger than the image we're using'
    #---------------------------------------------------------------------
    wd.write_params_file(data_dir, dx, dy, dz, total_time, dt, vis, nu, comment, model_var, model_var_comment)

    return vis, dx, dy, dz, total_time, dt, nu, save_time, model_var, update_time

def create_source_location(load_dir, data_dir, filename, other = None):
    #File which loads the file with dirichlet conditions
    holes_location = io.imread(load_dir + filename).astype(float)
    holes_location /= np.max(holes_location)
    source_location = np.zeros( np.asarray(holes_location).shape )

    total = np.sum(holes_location)
    for i in np.arange(0, holes_location.shape[0]):
        for j in np.arange(0, holes_location.shape[1]):
            for k in np.arange(0, holes_location.shape[2]):
                if (holes_location[i,j,k] > 0.0 and other > 0):
                    prob = np.random.randint(0,total)
                    total -= 1.0
                    if prob < other:
                        source_location[i,j,k] = 1.0
                        other -= 1

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
        Nonesim_name='hopping_model',
    """
    tic1 = time.time()
    vessel_location = io.imread(load_dir + filename).astype(float)sim_name='hopping_model',
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
    tumor_location = io.imread(load_dir + filename).astype(float)
    diffusion_location = np.ones( np.asarray(tumor_location).shape )
    diffusion_location /= np.max(diffusion_location)
    vessel_location = io.imread(load_dir + other[0]).astype(float)
    vessel_location /= np.max(vessel_location)
    source_location = np.load(data_dir + other[1]).astype(float)
    source_location /= np.max(source_location)

    np.save(data_dir + "/diffusion_location", diffusion_location - vessel_location + source_location)
    #np.save(data_dir + "/diffusion_location", diffusion_location[150:-150,150:-150,150:-150]-vessel_location[150:-150,150:-150,150:-150] + source_location[150:-150,150:-150,150:-150])#got to take out vasculature but add source if there are any.

def model(load_dir, data_dir, parameter):
    """
    Function that creates the different arrays that set the geometry of our diffusion landscape.

    Args:
        load_dir(string): directory with all the data files
        data_dir(string): directory where all the manipulated arrays are stored after creation
    Returns:
        None
    """
    tic = time.time()
    SL = create_source_location(load_dir, data_dir, 'UT16-T-stack3-Sept10_iso_50000gaps.tif', other=parameter)
    FL = create_flow_location(load_dir, data_dir, 'UT16-T-stack3-Sept10_iso_vesthresh-cropped.tif', other=parameter)
    DL = create_diffusion_location(load_dir, data_dir, 'UT16-T-stack3-Sept10_iso_tissueboundary-cropped.tif', other = ['UT16-T-stack3-Sept10_iso_vesthresh-cropped.tif','/source_location.npy'])
    toc = time.time()
    print toc-tic, "sec elapsed creating model..."

def concentration_time(time_point):
    """
    Function that calculates the change in concentration in the blood vessel as #---------------------------------------------------------------------#---------------------------------------------------------------------a function of time (according to Syed et co. observations)

    Args:
        time(float): time in hours
    Returns:SL = create_source_location(load_dir, data_dir, 'UT16-T-stack3-Sept10_iso_50000gaps.tif')
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

def update_diff(holes_location, source_location, data_dir, parameter = []):

    total = np.sum(source_location)
    other = np.sum(holes_location)
    source_location *= 0.0

    for i in np.arange(0, holes_location.shape[0]):
        for j in np.arange(0, holes_location.shape[1]):
            for k in np.arange(0, holes_location.shape[2]):
                if (holes_location[i,j,k] > 0.0 and total > 0):
                    prob = np.random.randint(0,other)
                    other -= 1.0
                    if prob < total:
                        source_location[i,j,k] += 1.0
                        total -= 1
    print "New hole count:", np.sum(source_location)

    np.save(data_dir + "/source_location", source_location)
    return 0
