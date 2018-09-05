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

def main():

    #colors_techniques = plt.cm.viridis(np.linspace(0.,1.,len(techniques))) #BuPu
    lines = [':', '-', ':', '-', ':', '-', '-']
    n = 10
    colors_gradient = plt.cm.inferno(np.linspace(0,1,n))


    fig, ax  = lp.newfig(0.6)
    flow = np.load('../data/' + 'flow_08-31' + '/time_sum.npy')
    holes = np.load('../data/' + 'holes5k_08-31' + '/time_sum.npy')

    plt.plot(flow[0],flow[1], color=colors_gradient[0], linestyle = lines[0], label = 'flow')
    plt.plot(holes[0],holes[1], color=colors_gradient[1], linestyle = lines[1], label = 'holes')

    plt.legend()
    plt.title("Total gold nanoparticles")
    ax.set_xlabel(r"time (seconds)")
    ax.set_ylabel(r"sum concentration")
    ax.minorticks_off()
    filename = 'fig2'
    lp.savefig(filename)
    plt.close(fig)



if __name__ == "__main__":
    main()
