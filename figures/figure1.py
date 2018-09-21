import numpy as np
import latex_plots as lp
import matplotlib.pyplot as plt

###########################################################################
########################### PLOTTING STARTS HERE
###########################################################################

import matplotlib as mpl
from matplotlib.colors import LogNorm
from matplotlib.ticker import LogLocator
from skimage import io

def tif2npy(sim, filename, time):
    nanoParticles = io.imread('../data/' + sim + filename)
    nanoP = nanoParticles.astype(float)/np.max(nanoParticles.astype(float))
    nanoP = np.asarray(nanoP)
    saveto = '../data/' + sim + '/diff_' + str(time) + 'sec'
    np.save(saveto, nanoP)

def main(sim, time = ''):
    if time == '':
        time = np.load('../data/' + sim + '/lastTime_seconds.npy')

    #colors_techniques = plt.cm.viridis(np.linspace(0.,1.,len(techniques))) #BuPu
    lines = [':', '-', ':', '-', ':', '-', '-']
    n = 10
    colors_gradient = plt.cm.inferno(np.linspace(0,1,n))

    fig, ax  = lp.newfig(0.6)
    nanoP = np.load('../data/' + sim +'/diff_' + str(time) + 'sec.npy')
    nanoP = nanoP/np.max(nanoP) #in case max in not concentration
    #findmin = nanoP
    #findmin[findmin == 0.0 ] = 100.0
    #mini = np.min(findmin)
    #nanoP = nanoP - np.full(np.shape(nanoP), mini)


    downsize = 1
    cax = ax.contourf(range(0,np.shape(nanoP)[0],1)[::downsize], range(0,np.shape(nanoP)[2],1)[::downsize], nanoP[np.int(np.shape(nanoP)[1]/2),::downsize,::downsize], levels=np.logspace(-3, 0, 100), locator=mpl.ticker.LogLocator(50), cmap=plt.cm.inferno)
    #cbar = fig.colorbar(cax, ticks=[10**0, 10**(-3), 10**(-6), 10**(-9)])
    cbar = fig.colorbar(cax, ticks=[10**0, 10**(-1), 10**(-2), minimum])

    #cbar.ax.set_ylabel(r'$Concentration$')
    for c in ax.collections:
        c.set_edgecolor("face")
    plt.title("Normalized concentration of np")
    ax.set_xlabel(r"$z$-direction ($\mu m$)")
    ax.set_ylabel(r"$y$-direction ($\mu m$)")
    ax.minorticks_off()
    filename = sim + "_" + str(time)
    lp.savefig(filename)
    plt.close(fig)



if __name__ == "__main__":
    #tif2npy('chanlab' ,'/UT16-T-stack3-Sept10_iso_particles-cropped.tif', '1800.0')
    #main('holes5k_08-31', time = 1800.0)
    main('holes', time = 1800.0)
