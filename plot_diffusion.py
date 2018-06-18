import numpy as np
import matplotlib as mpl
mpl.use('pgf')

def figsize(scale):
    fig_width_pt = 469.755                          # Get this from LaTeX using \the\textwidth
    inches_per_pt = 1.0/72.27                       # Convert pt to inch
    golden_mean = (np.sqrt(5.0)-1.0)/2.0            # Aesthetic ratio (you could change this)
    fig_width = fig_width_pt*inches_per_pt*scale    # width in inches
    fig_height = fig_width*golden_mean              # height in inches
    fig_size = [fig_width,fig_height]
    return fig_size

pgf_with_latex = {                      # setup matplotlib to use latex for output
    "pgf.texsystem": "lualatex",        # change this if using xetex or lautex
    "text.usetex": True,                # use LaTeX to write all text
    "font.family": "serif",
    "font.serif": [],                   # blank entries should cause plots to inherit fonts from the document
    "font.sans-serif": [],
    "font.monospace": [],
    "axes.labelsize": 10,               # LaTeX default is 10pt font.
    "font.size": 10,
    "legend.fontsize": 8,               # Make the legend/label fonts a little smaller
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "figure.figsize": figsize(0.9),     # default fig size of 0.9 textwidth
    "pgf.preamble": [
        r"\usepackage[utf8x]{inputenc}",    # use utf8 fonts becasue your computer can handle it :)
        r"\usepackage[T1]{fontenc}",        # plots will be generated using this preamble
        ]
    }
mpl.rcParams.update(pgf_with_latex)

import matplotlib.pyplot as plt

# I make my own newfig and savefig functions
def newfig(width):
    plt.clf()
    fig = plt.figure(figsize=figsize(width))
    ax = fig.add_subplot(111)
    return fig, ax

def savefig(filename):
    plt.savefig('{}.pgf'.format(filename), bbox_inches='tight',dpi=2400) #resolution
    plt.savefig('{}.pdf'.format(filename), bbox_inches='tight',dpi=2400) #specify resolution


###########################################################################
########################### PLOTTING STARTS HERE
###########################################################################
import sys
import os

import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from matplotlib.ticker import LogLocator
import numpy as np

def main(sim, time = ''):
    simulation = '1'
    sys.path.insert(0, '/home/jrothschild/Research')
    cwd = sim
    if time == '':
        np.load(cwd + '/lastTime_seconds.npy')

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
    ax.set_ylabel(r"$y-direction$")
    #ax.set_yscale("log")
    ax.minorticks_off()
    savefig(cwd + "/Vessel")
    plt.close(fig)
    """
    #=======================FIGURE NP==========================
    #time = 240


    fig, ax  = newfig(0.6)
    nanoP = np.load(cwd + '/diff_' + str(time) + 'min.npy')

    nanoP[nanoP < 10**(-9)] = 10**(-9)
    cax = ax.contourf(range(0,np.shape(nanoP)[0],1), range(0,np.shape(nanoP)[2],1), nanoP[np.int(np.shape(nanoP)[1]/2),:,:], levels=np.logspace(-9, 0, 100), locator=mpl.ticker.LogLocator(50), cmap=plt.cm.inferno,)
    cbar = fig.colorbar(cax, ticks=[10**0, 10**(-3), 10**(-6), 10**(-9)])
    #cbar.ax.set_ylabel(r'$Concentration$')
    for c in ax.collections:
        c.set_edgecolor("face")
    if sim == os.getcwd() + "/SimD0.01":
        plt.plot([0, 148], [160, 160], 'r', lw=1)
        plt.plot([152, 300], [160, 160], 'r', lw=1)
        plt.plot([0, 300], [140, 140], 'r', lw=1)
    """
    else:
        Vessel = np.load(cwd + '/Neumann.npy')
        x,y = np.argwhere(Vessel[np.int(np.shape(Vessel)[1]/2),:,:] == 1).T
        plt.scatter(x,y,c='r',marker='.')
    """
    plt.title("Normalized concentration of NP")
    ax.set_xlabel(r"$z$-direction ($\mu m$)")
    ax.set_ylabel(r"$y$-direction ($\mu m$)")
    ax.minorticks_off()
    savefig(cwd + "/nanoP_" + str(time))
    plt.close(fig)


if __name__ == "__main__":
    #main(os.getcwd() + "/SimD0.01", time = 240)
    #main(os.getcwd() + "/SimFull", time = 240)
    main(os.getcwd() + "/ChanLab", time = 240)
