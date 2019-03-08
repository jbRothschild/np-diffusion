import os
import network as nk
import numpy as np
import matplotlib.pyplot as plt

from matplotlib.colors import LogNorm

from data import DOSE, FINAL_DOSE, SPECIES

def plot_data(dose=1.0, data_species=[2,3]):
    for d in data_species:
        for time in list(FINAL_DOSE[dose].keys()):
            plt.errorbar(time, np.mean(FINAL_DOSE[dose][time][SPECIES[d]]),
            yerr=np.std(FINAL_DOSE[dose][time][SPECIES[d]]),
            marker='o',
            mec='k',
            mew=1,
            color='k',
            ecolor=plt.cm.Set2(d),
            markerfacecolor=plt.cm.Set2(d),
            capsize=2#,
            #linestyle='None'
            )

def odeSolve(dosage=1.0, important_species=[2,3], plotvsdata=False):

    tmodel = nk.Models(np.asarray([dosage,0.,0.,0.,0.]), nk.ben_net)
    tmodel.solve()

    fig = plt.figure()
    for i in np.arange(np.shape(tmodel.sol.y)[0]):
        lw = 2 if i in important_species else 1;
        ls = '-' if i in important_species else '--';
        plt.plot(tmodel.sol.t,100*tmodel.sol.y[i]/dosage, color=plt.cm.Set2(i), linewidth=lw, linestyle=ls)
    #plt.yscale('log')
    #plt.ylim([10**(-2),10**(2)])
    plt.legend(tmodel.species)
    if plotvsdata == True:
        plot_data(dosage, important_species)
    figname = "Network_dosage_"+str(dosage)
    plt.title("Dosage "+str(dosage))
    plt.xlabel(r'time $h$')
    plt.ylabel(r'\% Initial Dosage (\%ID)')
    plt.savefig(DIR_OUTPUT + os.sep + figname + '.pdf')
    plt.savefig(DIR_OUTPUT + os.sep + figname + '.eps')
    plt.close(fig)

if __name__ == '__main__':

    DIR_OUTPUT = "figures"
    if not os.path.exists(DIR_OUTPUT):
        os.makedirs(DIR_OUTPUT)

    plt.style.use('parameters.mplstyle')  # particularIMporting

    for dose in list(FINAL_DOSE.keys()):
        odeSolve(dosage=dose, important_species=list(SPECIES.keys()), plotvsdata=True)
