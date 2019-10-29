import os
import network as nk
import numpy as np
import matplotlib.pyplot as plt

from collections import OrderedDict

from matplotlib.colors import LogNorm

from data import DOSE, FINAL_DOSE, SPECIES, NUM_KUP, NUM_REC_KUP, NP_SIZE

def plot_ben_data():
    fig = plt.figure()
    fig.set_size_inches(4.6, 3.2)

    for name in list(SPECIES.keys()):
        for dose in list(FINAL_DOSE.keys()):
            print(FINAL_DOSE[dose][24]['liver'])
            plt.errorbar(dose, np.mean(FINAL_DOSE[dose][24][SPECIES[name]]),
            yerr=np.std(FINAL_DOSE[dose][24][SPECIES[name]]),
            marker='o',
            mec='k',
            mew=1,
            color='k',
            ecolor=plt.cm.Set2(name),
            markerfacecolor=plt.cm.Set2(name),
            capsize=2,
            label=SPECIES[name]#,
            #linestyle='None'
            )
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = OrderedDict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys())

    plt.xscale('log')
    plt.xlabel(r'Dosage $\# Np$'); plt.ylabel(r'Uptake $\%$')
    plt.title(r'$\%$ uptake after 24 hours')
    figname = 'data24h'
    plt.savefig(DIR_OUTPUT + os.sep + figname + '.pdf'); plt.savefig(DIR_OUTPUT + os.sep + figname + '.eps')
    return 0

def plotting_solution(model, sim, dosage, data_dic=FINAL_DOSE):

    fig = plt.figure()
    fig.set_size_inches(4.6, 3.2)

    for i in np.arange(np.shape(model.sol.y)[0]):
        lw = 1 if i in list(SPECIES.keys()) else 1;
        ls = '-' if i in list(SPECIES.keys()) else '-';
        #total = float(NUM_REC_KUP) if i == 1 else dosage;
        total = dosage
        plt.plot(model.sol.t,100*model.sol.y[i]/total, color=plt.cm.Set2(i), linewidth=lw, linestyle=ls)

    for d in list(SPECIES.keys()):
        for time in list(DATA_DIC[dosage].keys()):
            plt.errorbar(time, np.mean(DATA_DIC[dosage][time][SPECIES[d]]),
            yerr=np.std(DATA_DIC[dosage][time][SPECIES[d]]),
            marker='o',
            mec='k',
            mew=1,
            color='k',
            ecolor=plt.cm.Set2(d),
            markerfacecolor=plt.cm.Set2(d),
            capsize=2#,
            #linestyle='None'
            )

    plt.legend(model.species)
    figname = "Network_dosage_" + sim + str( int( dosage/(10**14/(4*np.pi*50**2)) ) )
    plt.title("Dosage "+str(int( dosage/(10**14/(4*np.pi*50**2)) ) ) )
    plt.xlabel(r'time $h$'); plt.ylabel(r'\% Total (\%ID)')
    plt.savefig(DIR_OUTPUT + os.sep + figname + '.pdf'); plt.savefig(DIR_OUTPUT + os.sep + figname + '.eps')

    plt.close(fig)

    return 0

def plotting_solution2(model, sim, dosage, data_dic=FINAL_DOSE):
    fig, axarr = plt.subplots(nrows=1, ncols=2)
    fig.set_size_inches(7.2, 3.2)

    axarr[0].set_title(r'Nanoparticle location')
    axarr[0].set_xlabel(r'Time $h$')
    axarr[0].set_ylabel(r'\% Initial Dosage $\% ID$')
    axarr[0].plot(model.sol.t,100*model.sol.y[0]/dosage, color=plt.cm.Set2(0), linewidth=2, linestyle='-', label='Blood')
    axarr[0].plot(model.sol.t,100*model.sol.y[2]/dosage, color=plt.cm.Set2(1), linewidth=1, linestyle='--', label='bound')
    axarr[0].plot(model.sol.t,100*model.sol.y[3]/dosage, color=plt.cm.Set2(2), linewidth=1, linestyle='--', label='endosomes')
    axarr[0].plot(model.sol.t,100*model.sol.y[4]/dosage, color=plt.cm.Set2(3), linewidth=1, linestyle='--', label='internalized')
    axarr[0].plot(model.sol.t,100*(model.sol.y[2]+model.sol.y[3]+model.sol.y[4])/dosage, color=plt.cm.Set2(4), linewidth=2, linestyle='-', label='Liver')
    axarr[0].plot(model.sol.t,100*model.sol.y[5]/dosage, color=plt.cm.Set2(5), linewidth=2, linestyle='-', label='Tumor')
    axarr[0].legend()

    axarr[1].set_title(r'Receptor Dynamics')
    axarr[1].plot(model.sol.t,100*model.sol.y[1]/NUM_REC_KUP, color=plt.cm.Set2(6), linewidth=1, linestyle='-', label='unbound')
    axarr[1].plot(model.sol.t,100*model.sol.y[2]/NUM_REC_KUP, color=plt.cm.Set2(1), linewidth=1, linestyle='-', label='bound')
    axarr[1].plot(model.sol.t,100*model.sol.y[3]/NUM_REC_KUP, color=plt.cm.Set2(2), linewidth=1, linestyle='-', label='endosomes')
    axarr[1].set_xlabel(r'Time $h$')
    axarr[1].set_ylabel(r'\% Total Receptor')
    axarr[1].legend()

    for d in list(SPECIES.keys()):
        for time in list(DATA_DIC[dosage].keys()):
            axarr[0].errorbar(time, np.mean(DATA_DIC[dosage][time][SPECIES[d]]),
            yerr=np.std(DATA_DIC[dosage][time][SPECIES[d]]),
            marker='o',
            mec='k',
            mew=1,
            color='k',
            ecolor=plt.cm.Set2(d),
            markerfacecolor=plt.cm.Set2(d),
            capsize=2#,
            #linestyle='None'
            )

    figname = "Dosage_" + sim + str( int( dosage/(10**14/(4*np.pi*50**2)) ) )
    plt.savefig(DIR_OUTPUT + os.sep + figname + '.pdf'); plt.savefig(DIR_OUTPUT + os.sep + figname + '.eps')
    plt.close(fig)

    return 0



def single_dosage(select_model, sim, dosage = 1.0, data_dic=FINAL_DOSE, multi = 1, showreceptor=False):
    # run the odeSolver
    select_model.solve()

    if not showreceptor:
        plotting_solution(select_model, sim, dosage, data_dic)
    else:
        plotting_solution2(select_model, sim, dosage, data_dic)

    return 0


def multi_dosage(select_model, sim, dosage=1.0, data_dic=FINAL_DOSE, multi=1., showreceptor=False):

    select_model.change_init_conc(np.asarray([select_model.init_conc[0], select_model.init_conc[1], 0., 0., 0., 0., 0.])/np.asarray([multi, 1., 1., 1., 1., 1., 1.]))
    
    select_model.args.append(np.asarray(select_model.time_eval))
    select_model.args.append(multi)
    #select_model.args = np.append(select_model.args, np.asarray(select_model.time_eval))
    select_model.solve()
    """
    sol = np.asarray(select_model.sol.y)
    print(np.shape(sol))
    sol[0,-1] += dosage/multi

    for multi in np.arange(1, multi):
        select_model.change_init_conc(np.asarray(sol[:,-1]))
        select_model.solve()
        print(np.shape(sol))
        sol = np.append(sol, np.asarray(select_model.sol.y), axis = 1)
        print("dimension " + str(np.shape(sol)))
    """
    if not showreceptor:
        plotting_solution(select_model, sim, dosage, data_dic)
    else:
        plotting_solution2(select_model, sim, dosage, data_dic)


    return 0

if __name__ == '__main__':

    DIR_OUTPUT = "figures"
    if not os.path.exists(DIR_OUTPUT):
        os.makedirs(DIR_OUTPUT)

    plt.style.use('parameters.mplstyle')  # particularIMporting

    DATA_DIC = FINAL_DOSE
    DATA_DIC = DOSE
    """
    # diffusion
    for dose in list(DATA_DIC.keys()):
        print("dose: " + str(dose))
        model = nk.Models(np.asarray([dose, float(NUM_REC_KUP), 0., 0., 0., 0., 0.]), float(NUM_KUP), float(NUM_REC_KUP), float(NP_SIZE), nk.ben_net_dif)

        single_dosage(model, 'bnd', dosage=dose, data_dic=DATA_DIC, showreceptor=True)

    # simple
    for dose in list(DATA_DIC.keys()):
        print("dose: " + str(dose))
        model = nk.Models(np.asarray([dose, 0., 0., 0.]), float(NUM_KUP), float(NUM_REC_KUP), float(NP_SIZE), nk.ben_net_simple)
        model.change_species((r'$N_p$', r'Liver', r'Tumor', r'Body'))

        single_dosage(model, 'bns', dosage=dose, data_dic=DATA_DIC, showreceptor=False)

    # no dynamics
    for dose in list(DATA_DIC.keys()):
        print("dose: " + str(dose))
        model = nk.Models(np.asarray([dose, float(NUM_REC_KUP), 0., 0., 0., 0., 0.]), float(NUM_KUP), float(NUM_REC_KUP), float(NP_SIZE), nk.ben_net)

        single_dosage(model, 'bn', dosage=dose, data_dic=DATA_DIC, showreceptor=True)
    """
    for dose in list(DATA_DIC.keys()):
        print("dose: " + str(dose))
        multi = 3.
        model = nk.Models(np.asarray([dose, float(NUM_REC_KUP), 0., 0., 0., 0., 0.]), float(NUM_KUP), float(NUM_REC_KUP), float(NP_SIZE), nk.ben_net_multi)

        multi_dosage(model, 'md_bnd', dosage=dose, data_dic=DATA_DIC, multi=multi, showreceptor=True)

    plot_ben_data()
