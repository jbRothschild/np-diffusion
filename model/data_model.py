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
    np.load(load_dir + filename)

    np.save(data_dir + "/source_location", source_location)

def create_flow_location(load_dir, data_dir, filename, other = None):
    np.load(load_dir + file)

    np.save(data_dir + "/flow_location", flow_location)

def create_diffusion_location(load_dir, data_dir, filename, other = None):
    np.load(load_dir + file)

    np.save(data_dir + "/diffusion_location", diffusion_location)

def model(load_dir, data_dir, load):
    SL = create_source_location(load_dir, data_dir, 'UT16-T-stack3-Sept10_iso_gaps-cropped.tif')
    FL = create_flow_location(load_dir, data_dir, 'UT16-T-stack3-Sept10_iso_vesthresh-cropped.tif')
    DL = create_diffusion_location(load_dir, data_dir, 'UT16-T-stack3-Sept10_iso_tissueboundary-cropped.tif', other = SL)
