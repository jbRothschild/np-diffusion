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

def main(sim, time = ''):
    if time == '':
        time = np.load('../data/' + sim + '/lastTime_seconds.npy')

    #colors_techniques = plt.cm.viridis(np.linspace(0.,1.,len(techniques))) #BuPu
    lines = [':', '-', ':', '-', ':', '-', '-']
    n = 10
    colors_gradient = plt.cm.inferno(np.linspace(0,1,n))
    """
    #=======================FIGURE Hole==========================
    fig, ax  = newfig(0.6)
    Hole = np.load(cwd + '/Dirichlet.npy')

    cax = ax.contourf(range(0,np.shape(Hole)[0],1), range(0,np.shape(Hole)[2],1), Hole[np.int(np.shape(Hole)[1]/2),:,:], cmap=plt.cm.inferno)
    cbar = fig.colorbar(cax)
    cbar.ax.set_ylabel(r'$Concentration$')
    ax.set_xlabel(r"$x-direction$")
    ax.set_ylabel(r"$y-direction$")
    #ax.set_yscale("log")
    ax.minorticks_off()
    #plt.savefig('Hole.pgf', bbox_inches='tight')
    #plt.savefig('Hole.pdf', bbox_inches='tight')
    savefig(cwd + "/Hole")
    plt.close(fig)

    #=======================FIGURE VESSEL==========================
    fig, ax  = newfig(0.6)
    Vessel = np.load(cwd + '/Neumann.npy')

    cax = ax.contourf(range(0,np.shape(Vessel)[0],1), range(0,np.shape(Vessel)[2],1), Vessel[np.int(np.shape(Vessel)[1]/2),:,:], cmap=plt.cm.inferno)
    cbar = fig.colorbar(cax)
    cbar.ax.set_ylabel(r'$Concentration$')
    ax.set_xlabel(r"$x-direction$")
    """
    """
    else:
        Vessel = np.load(cwd + '/Diff_Coeff.npy')
        x,y = np.argwhere(Vessel[np.int(np.shape(Vessel)[1]/2),:,:] == 1).T
        plt.scatter(x,y,c='r',marker='.')
    """
    """
    ax.set_ylabel(r"$y-direction$")
    #ax.set_yscale("log")
    ax.minorticks_off()
    savefig(cwd + "/Vessel")
    plt.close(fig)
    """
    #=======================FIGURE NP==========================
    #time = 240


    fig, ax  = lp.newfig(0.6)
    nanoP = np.load('../data/' + sim +'/diff_' + str(time) + 'sec.npy')
    #Only for ChanLab data
    #nanoParticles = io.imread(cwd + '/UT16-T-stack3-Sept10_iso_particles-cropped.tif')
    #nanoP = nanoParticles.astype(float)/np.max(nanoParticles.astype(float))

    nanoP[nanoP < 10**(-3)] = 10**(-3)
    cax = ax.contourf(range(0,np.shape(nanoP)[0],1), range(0,np.shape(nanoP)[2],1), nanoP[np.int(np.shape(nanoP)[1]/2),:,:], levels=np.logspace(-3, 0, 100), locator=mpl.ticker.LogLocator(50), cmap=plt.cm.inferno)
    #cbar = fig.colorbar(cax, ticks=[10**0, 10**(-3), 10**(-6), 10**(-9)])
    cbar = fig.colorbar(cax, ticks=[10**0, 10**(-1), 10**(-2), 10**(-3)])

    #cbar.ax.set_ylabel(r'$Concentration$')
    for c in ax.collections:
        c.set_edgecolor("face")
    plt.title("Normalized concentration of np")
    ax.set_xlabel(r"$z$-direction ($\mu m$)")
    ax.set_ylabel(r"$y$-direction ($\mu m$)")
    ax.minorticks_off()
    filename = "nanoP_log_" +str(time)
    lp.savefig(filename)
    plt.close(fig)


if __name__ == "__main__":
    #main(os.getcwd() + "/SimD0.01", time = 240)01
    main("sim_flow", time = '')
    #main(os.getcwd() + "/SimFullT", time = 240)
    #main(os.getcwd() + "/ChanLab", time = 240)
