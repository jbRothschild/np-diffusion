import numpy as np
import latex_plots as lp
import matplotlib.pyplot as plt

###########################################################################
########################### PLOTTING STARTS HERE
###########################################################################

#import matplotlib as mpl
from matplotlib.colors import LogNorm
from matplotlib.ticker import LogLocator
from skimage import io

def main():

    #colors_techniques = plt.cm.viridis(np.linspace(0.,1.,len(techniques))) #BuPu
    lines = [':', '--', '-']
    n = 10
    color_gradient = plt.cm.inferno(np.linspace(0,1,3))

    fig, ax  = lp.newfig(0.6)
    """
    simrun1 = np.load('../sim/CM/time_sum_158_1_10.npy')
    simrun2 = np.load('../sim/CM/time_sum_158_1_300.npy')
    simrun3 = np.load('../sim/CM/time_sum_158_1_2000.npy')
    simrun4 = np.load('../sim/CM/time_sum_158_2_10.npy')
    simrun5 = np.load('../sim/CM/time_sum_158_2_300.npy')
    simrun6 = np.load('../sim/CM/time_sum_158_2_2000.npy')
    simrun7 = np.load('../sim/CM/time_sum_158_3_10.npy')
    simrun8 = np.load('../sim/CM/time_sum_158_3_300.npy')
    simrun9 = np.load('../sim/CM/time_sum_158_3_2000.npy')


    plt.plot(simrun1[0],simrun1[1], color=color_gradient[0], linestyle = lines[0], label = '10 secs')
    plt.plot(simrun2[0],simrun2[1], color = color_gradient[1], linestyle = lines[0], label = '5 mins')
    plt.plot(simrun3[0],simrun3[1], color = color_gradient[2], linestyle = lines[0], label = '30 mins')
    plt.plot(simrun4[0],simrun4[1], color = color_gradient[0], linestyle = lines[1], label = '10 secs')
    plt.plot(simrun5[0],simrun5[1], color = color_gradient[1], linestyle = lines[1], label = '5 mins')
    plt.plot(simrun6[0],simrun6[1], color = color_gradient[2], linestyle = lines[1], label = '30 mins')
    plt.plot(simrun7[0],simrun7[1], color = color_gradient[0], linestyle = lines[2], label = '10 secs')
    plt.plot(simrun8[0],simrun8[1], color = color_gradient[1], linestyle = lines[2], label = '5 mins')
    plt.plot(simrun9[0],simrun9[1], color = color_gradient[2], linestyle = lines[2], label = '30 mins')
    """
    simrun1 = np.load('../sim/CM/time_sum_mphage60.npy')
    simrun2 = np.load('../sim/CM/time_sum_mphage300.npy')
    simrun3 = np.load('../sim/CM/time_sum_mphage1800.npy')

    plt.plot(simrun1[0],simrun1[1], color=color_gradient[0], linestyle = lines[0], label = '1 min')
    plt.plot(simrun2[0],simrun2[1], color=color_gradient[0], linestyle = lines[1], label = '5 min')
    plt.plot(simrun3[0],simrun3[1], color=color_gradient[0], linestyle = lines[2], label = '30 min')


    plt.legend()
    plt.title("Total gold nanoparticles")
    ax.set_xlabel(r"time (seconds)")
    ax.set_ylabel(r"total particles in tumor")
    ax.minorticks_off()
    filename = 'sum_mphage_hopping'
    lp.savefig(filename)
    plt.close(fig)

    #------------------------2A----------------------
    """
    fig, ax  = lp.newfig(0.6)

    holes50_1 = np.load('../data/time_sum/' + 'time_sum_hole5000_1s.npy')
    holes50_10 = np.load('../data/time_sum/' + 'time_sum_hole5000_10s.npy')
    holes50_60 = np.load('../data/time_sum/' + 'time_sum_hole5000_60s.npy')
    holes50_300 = np.load('../data/time_sum/' + 'time_sum_hole5000_300s.npy')

    plt.plot(holes50[0],holes50[1], color=colors_gradient[4], linestyle = lines[1])
    plt.plot(holes50_1[0],holes50_1[1], color=colors_gradient[5], linestyle = lines[0], label = '1s')
    plt.plot(holes50_10[0],holes50_10[1], color=colors_gradient[6], linestyle = lines[0], label = '10s')
    plt.plot(holes50_60[0],holes50_60[1], color=colors_gradient[7], linestyle = lines[0], label = '60s')
    plt.plot(holes50_300[0],holes50_300[1], color=colors_gradient[8], linestyle = lines[0], label = '300s')

    plt.legend()
    plt.title("Total gold nanoparticles")
    ax.set_xlim((0,500))
    ax.set_xlabel(r"time (seconds)")
    ax.set_ylabel(r"sum concentration")
    ax.minorticks_off()
    filename = 'fig2b'
    lp.savefig(filename)
    plt.close(fig)
    """

if __name__ == "__main__":
    main()
