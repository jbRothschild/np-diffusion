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
    holes3 = np.load('../data/time_sum/' + 'time_sum_hole300.npy')
    holes30 = np.load('../data/time_sum/' + 'time_sum_hole3000.npy')
    holes300 = np.load('../data/time_sum/' + 'time_sum_hole30000.npy')
    holes10 = np.load('../data/time_sum/' + 'time_sum_hole1000.npy')
    holes100 = np.load('../data/time_sum/' + 'time_sum_hole10000.npy')
    holes5 = np.load('../data/time_sum/' + 'time_sum_hole500.npy')
    holes50 = np.load('../data/time_sum/' + 'time_sum_hole5000.npy')
    holes500 = np.load('../data/time_sum/' + 'time_sum_hole50000.npy')

    plt.plot(holes3[0],holes3[1], color=colors_gradient[0], linestyle = lines[1], label = '300 holes')
    plt.plot(holes5[0],holes5[1], color=colors_gradient[1], linestyle = lines[1], label = '500 holes')
    plt.plot(holes10[0],holes10[1], color=colors_gradient[2], linestyle = lines[1], label = '1000 holes')
    plt.plot(holes30[0],holes30[1], color=colors_gradient[3], linestyle = lines[1], label = '3000 holes')
    plt.plot(holes50[0],holes50[1], color=colors_gradient[4], linestyle = lines[1], label = '5000 holes')
    plt.plot(holes100[0],holes100[1], color=colors_gradient[5], linestyle = lines[1], label = '10000 holes')
    plt.plot(holes300[0],holes300[1], color=colors_gradient[6], linestyle = lines[1], label = '30000 holes')
    plt.plot(holes500[0],holes500[1], color=colors_gradient[7], linestyle = lines[1], label = '50000 holes')

    plt.legend()
    plt.title("Total gold nanoparticles")
    ax.set_xlabel(r"time (seconds)")
    ax.set_ylabel(r"sum concentration")
    ax.minorticks_off()
    filename = 'fig2a'
    lp.savefig(filename)
    plt.close(fig)

    #------------------------2A----------------------

    fig, ax  = lp.newfig(0.6)

    holes50_1 = np.load('../data/time_sum/' + 'time_sum_hole5000_1s.npy')
    holes50_10 = np.load('../data/time_sum/' + 'time_sum_hole5000_10s.npy')
    holes50_60 = np.load('../data/time_sum/' + 'time_sum_hole5000_60s.npy')
    holes50_300 = np.load('../data/time_sum/' + 'time_sum_hole5000_300s.npy')

    #plt.plot(holes50[0],holes50[1], color=colors_gradient[4], linestyle = lines[1])
    #plt.plot(holes50_1[0],holes50_1[1], color=colors_gradient[5], linestyle = lines[0], label = '1s')
    plt.plot(holes50_10[0],holes50_10[1], color=colors_gradient[6], linestyle = lines[0], label = '10s')
    #plt.plot(holes50_60[0],holes50_60[1], color=colors_gradient[7], linestyle = lines[0], label = '60s')
    #plt.plot(holes50_300[0],holes50_300[1], color=colors_gradient[8], linestyle = lines[0], label = '300s')

    plt.legend()
    plt.title("Total gold nanoparticles")
    ax.set_xlabel(r"time (seconds)")
    ax.set_ylabel(r"sum concentration")
    ax.minorticks_off()
    filename = 'fig2b'
    lp.savefig(filename)
    plt.close(fig)

if __name__ == "__main__":
    main()
