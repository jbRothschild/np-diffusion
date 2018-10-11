import numpy as np
def write_params_file(data_dir, dx, dy, dz, time, dt, vis, nu, comment, model_var, model_var_comment):
    #A parameters file where we can check what parameters where being used
    file = open(data_dir + "/params.txt","w")
    file.write("Loaded boundary conditions\n")
    file.write("dx = "+ str(dx) +"; dy = "+ str(dy) +"; dz = "+ str(dz) +" #1 micrometer\n")
    file.write("time = "+ str(time)+"\n")
    file.write("dt = "+ str(dt) +" #Time steps of seconds\n")
    file.write("nu = "+ str(nu) +" #nu*dudx = du/dt\n")
    file.write("vis = "+ str(vis) +" #Diffusion coefficient\n")
    file.write(model_var_comment + " = " + str(model_var) + "\n\n")
    file.write("Comments: "+comment)
    file.close()

def save_run(t, u, data_dir, count):
    #save data of diffusion u at time t
    print t, " seconds run saved"
    np.save(data_dir + "/diff_"+str(t)+"sec", u)
    np.save(data_dir + "/" + count, np.asarray(t))

def save_run_2D(t, u, data_dir):
    #save data of diffusion 2D u at time t
    np.save(data_dir + "/diff_2D"+str(t)+"sec", u)

def partial_data(datafile, pd_filename, n):
    #save subsection of data (size n an integer around the center)
    data =  np.load(datafile)
    size = data.shape[0]
    np.save(pd_filename, data[size/2-n/2:size/2+n/2,size/2-n/2:size/2+n/2,size/2-n/2:size/2+n/2])
