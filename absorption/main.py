import network as nk
import numpy as np
import matplotlib.pyplot as plt

from matplotlib.colors import LogNorm

def main():
    for dosage in [100.,200.,300.,4000., 16000.]:
        tmodel = nk.Models(np.asarray([0.,0.,0.,0.,dosage]), nk.ben_net)
        tmodel.solve()

        fig = plt.figure()
        for i in np.arange(np.shape(tmodel.sol.y)[0]):
            plt.plot(tmodel.sol.t,tmodel.sol.y[i], color=plt.cm.Set2(i))
        #plt.yscale('log')
        #plt.ylim([10**(-5),10**5])
        plt.legend(tmodel.species)
        savename = "Network_dosage_"+str(dosage)+".png"
        plt.savefig(savename)
        plt.close(fig)

    n = 10.
    SOL = []
    for i in np.arange(0., 200., n):
        tmodel.change_init_conc(np.asarray([0.,0.,0.,0.,i]))
        tmodel.solve()
        SOL.append(tmodel.sol.y[0])
        print(np.size(tmodel.sol.t))
        print(tmodel.sol.t[np.argmax(tmodel.sol.y[0])])

    SOL_array = (np.asarray(SOL))
    SOL_array[SOL_array <= 0] = 10**(-7)
    maximum = int(np.log10(SOL_array).max())+1
    minimum = 0

    fig  = plt.figure()
    ax = fig.add_subplot(111)

    cax = ax.contourf(tmodel.sol.t, np.arange(0., 200., n), SOL_array, cmap=plt.cm.inferno, norm=LogNorm() , levels=np.logspace(minimum, maximum, 100))
    cbar = fig.colorbar(cax, ticks=[10**minimum, 10**int((maximum-minimum)/3), 10**int((maximum-minimum)*2/3), 10**maximum])
    for c in ax.collections:
        c.set_edgecolor("face")
    cbar.ax.set_ylabel(r'$Concentration\ of\ T_{cell}$')
    ax.set_title(r"")
    ax.set_xlabel(r"$Time$")
    ax.set_ylabel(r"$ initial\ antigen\ concentration$")
    #ax.set_yscale("log")
    ax.minorticks_off()
    plt.savefig("T_cell_by_initial_ag.png")
    plt.close(fig)


if __name__ == "__main__":
    main()
