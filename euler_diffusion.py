import sys
import numpy as np
import os
import euler_boundary as bd
from skimage import io
#import plot_diffusion as pd

def main(sim, load, D):
    cwd = os.getcwd() + "/Sim_" + sim + str(D) #remote use
    load_dir = os.getcwd() + '/ChanLab/'
    #cwd = $HOME #on Scinet
    if not os.path.exists(cwd):
        os.makedirs(cwd)
        
    #parameters
    count = '/lastTime_seconds.npy'
    size = 301
    dx = 1; dy = 1; dz = 1 #1 micrometer
    time = 3600*4
    dt = 30 #Time steps of 30 seconds
    vis = D #Diffusion coefficient
    v_radius = int(10./dx) #vessel radius in units of dx
    h_radius = int(1./dx) #hole radius in units of dx
    
    file = open(cwd + "/params.txt","w")
    if load != True:
        file.write("Created from model in euler_boudary\n")
        file.write("size =" + str(size)+"\n")
        file.write("v_radius = "+ str(v_radius) +" #vessel radius in units of dx\n")
        file.write("h_radius = "+ str(h_radius) +" #hole radius in units of dx\n")
    else:
        file.write("Loaded boundary conditions\n")
    file.write("dx = "+ str(dx) +"; dy = "+ str(dy) +"; dz = "+ str(dz) +" #1 micrometer\n")
    file.write("time = "+ str(time)+"\n")
    file.write("dt = "+ str(dt) +" #Time steps of 30 seconds\n")
    file.write("vis = "+ str(vis) +" #Diffusion coefficient\n")
    file.close() 
    
    
    #boundaries
    if not os.path.exists(cwd + count):
        #If we're using tiff images
        if load == True:
            bd.main('load', size=size, hole_radius=h_radius, vessel_radius=v_radius, cwd=cwd, fileN=load_dir + 'UT16-T-stack3-Sept10_iso_vesthresh-cropped.tif', fileD= load_dir + 'UT16-T-stack3-Sept10_iso_gaps-cropped.tif', file_domain= load_dir + 'UT16-T-stack3-Sept10_iso_tissueboundary-cropped.tif')
            #If we're using boundaries from euler_boundary
        else:
            bd.main('create', size=size, hole_radius=h_radius, vessel_radius=v_radius, cwd=cwd)

    neumann = np.load(cwd + "/Neumann.npy") #Neumann
    domain = np.load(cwd + "/Domain.npy") #domain
    dirichlet = np.load(cwd + "/Dirichlet.npy") #location of fixed concentration
    
    u = np.zeros((domain.shape[0], domain.shape[1], domain.shape[2])) #solution
    un = np.zeros((domain.shape[0], domain.shape[1], domain.shape[2])) #temp location for solution
    ijk = (np.linspace(1, domain.shape[0]-2, domain.shape[0]-2)).astype(int) #part of domain
    """
    neum_i = np.load(cwd + "/neum_i.npy"); neum_ip = np.load(cwd + "/neum_ip.npy"); neum_im = np.load(cwd + "/neum_im.npy")
    nuem_j = np.load(cwd + "/neum_j.npy"); neum_jp = np.load(cwd + "/neum_jp.npy"); neum_jm = np.load(cwd + "/neum_jm.npy")
    neum_k = np.load(cwd + "/neum_k.npy"); neum_kp = np.load(cwd + "/neum_kp.npy"); neum_km = np.load(cwd + "/neum_km.npy")
    """
    
    if not os.path.exists(cwd + count): #saves initial and creates lastTime_seconds.npy to run simulations. Basically checks at what step we're at
        np.save(cwd + count, np.asarray(0))
        np.save(cwd + "/diff_0min.npy", dirichlet*bd.concentration_time(0))
        
    initial = np.load(cwd + count)
    u = np.load(cwd + "/diff_" + str(initial/60) + "min" +".npy")

    #================Euleur's method============================

    for i in range(int(initial/dt)+1,time/dt+1): #run simulation from time
        un = u
        print i
        u[:,:,:] = un[:,:,:]
        
        u[ijk,:,:] += neumann[ijk,:,:]*( vis*dt*neumann[ijk+1,:,:]*( un[ijk+1,:,:]-un[ijk,:,:] ) + vis*dt*neumann[ijk-1,:,:]*( un[ijk-1,:,:]-un[ijk,:,:] ))/(dx**2)
        
        u[:,ijk,:] += neumann[:,ijk,:]*( vis*dt*neumann[:,ijk+1,:]*( un[:,ijk+1,:]-un[:,ijk,:] ) + vis*dt*neumann[:,ijk-1,:]*( un[:,ijk-1,:]-un[:,ijk,:] ))/(dy**2)
               
        u[:,:,ijk] += neumann[:,:,ijk]*( vis*dt*neumann[:,:,ijk+1]*( un[:,:,ijk+1]-un[:,:,ijk] ) + vis*dt*neumann[:,:,ijk-1]*( un[:,:,ijk-1]-un[:,:,ijk] ))/(dz**2)

        u = u*domain + bd.concentration_time(i*dt/3600)*dirichlet
        
        if i in range(0,time,20):
            np.save(cwd + "/diff_"+str(i*dt/60)+"min", u)
            np.save(cwd + "/" + count, np.asarray(i*dt))
            print np.load(cwd + count)
            #io.imsave(cwd + "/diff_"+str(i*dt/60)+"min.tif", u)
            
        print np.sum(u)
        
if __name__ == "__main__":
    main(sim='Syed', load=True, D=0.01)
