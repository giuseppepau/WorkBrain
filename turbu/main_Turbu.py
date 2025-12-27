# =======================================================================
# Turbulence framework, main part. From:
# Gustavo Deco, Morten L. Kringelbach, Turbulent-like Dynamics in the Human Brain,
# Cell Reports, Volume 33, Issue 10, 2020, 108471, ISSN 2211-1247,
# https://doi.org/10.1016/j.celrep.2020.108471.
# (https://www.sciencedirect.com/science/article/pii/S2211124720314601)
#
# Part of the Thermodynamics of Mind framework:
# Kringelbach, M. L., Sanz Perl, Y., & Deco, G. (2024). The Thermodynamics of Mind.
# Trends in Cognitive Sciences (Vol. 28, Issue 6, pp. 568–581). Elsevier BV.
# https://doi.org/10.1016/j.tics.2024.03.009
#
# by Gustavo Patow, June 9, 2024
# =======================================================================
import os
import scipy.io as sio
import sys

# Aggiungi il percorso del tuo pacchetto LibBrain
sys.path.append("/home/alessandrofloris/Documenti/giuse/LibBrain/LibBrain")


from neuronumba.tools.filters import BandPassFilter
from neuronumba.observables.turbulence import Turbulence
# from neuronumba.observables import Information_transfer
from LibBrain.Plotting.p_values import printAveragesAndStd

import LibBrain.Utils.decorators as decorators
decorators.forceCompute = False  # Use this to force re-computations.

# ------------------------------ Data Loader
# --------- ADNI_A
import LibBrain.DataLoaders.ADNI_A as ADNI
DL = ADNI.ADNI_A(use360=True, cutTimeSeries=True)
# --------- ABNI_B
# import DataLoaders as ADNI_B
# DL = ADNI_B.ADNI_B()
# ------------------------------

coords = DL.get_parcellation().get_CoGs()

dataPath = './_Data_Produced/' + DL.name() + '/'


def print_avgs_and_std(dataset, obs, range):
    print("\nAverages and Std Dev (for checking only):")
    for pos, lambda_v in enumerate(range):
        results = {}
        for group in DL.get_groupLabels():
            results[group] = [dataset[s][obs][pos] for s in dataset if s in DL.get_groupSubjects(group)]
        print(f"Results for lambda = {lambda_v}:")
        printAveragesAndStd(results)


@decorators.loadOrCompute
def from_fMRI(Turbu, ts):
    return Turbu.from_fmri(ts)


@decorators.loadOrCompute
def from_fMRI_surrogate(Turbu, ts):
    return Turbu.from_surrogate(ts)


def computeTurbu_subj(subj, timeseries, range, DL):
    # ADNI_A
    bpf = BandPassFilter(k=2, flp=0.01, fhi=0.09, tr=DL.TR()*1000.)   # Define a band pass filter
    # ADNI_B
    # bpf = BandPassFilter(k=2, flp=0.008, fhi=0.08, tr=DL.TR()*1000.)   # Define a band pass filter

    fullDataPath = dataPath + f'subj_{subj}/'
    if not os.path.exists(fullDataPath):
        os.makedirs(fullDataPath)

    # =======================================================================
    # dictionaries for each subject
    # =======================================================================
    all_results = {}
    for lambda_v in range:
        print(f'Processing subj: {subj} @ lambda: {lambda_v}')

        # =======================================================================
        # Define the turbulence object
        # =======================================================================
        Turbu = Turbulence(cog_dist=coords, lambda_val=lambda_v, ignore_nans=True)
        # Turbu = Information_transfer(cog_dist=coords, lambda_val=lambda_v, ignore_nans=True)
        Turbu.configure()

        # VERY IMPORTANT: For performance reasons, the filter expects the signal to be in the
        # transposed form (n_time_samples, n_rois). We have to transpose it before passing it
        bold_filt = bpf.filter(timeseries.T)  # we keep it transposed...
        # ======================= main analysis
        # Compute the observable
        subjPath = fullDataPath + f'turbu_{subj}_{lambda_v}.mat'
        turbuRes = from_fMRI(Turbu, bold_filt, subjPath)
        # ======================= Surrogate analysis
        # Compute the surrogate
        # subjPath = fullDataPath + f'turbu_{subj}_surrogate.mat'
        # turbuRes |= from_fMRI_surrogate(Turbu, bold_filt, subjPath)
        # ======================= Done analysis
        # Organize results
        for res in turbuRes:
            if res not in all_results:
                all_results[res] = []
            all_results[res].append(turbuRes[res])  # append at the end of the list, for each lambda_v
        print(f"done {subj} !!")
    return all_results


def computeTurbu(range, DL):
    all_results = {}
    for subj in DL.get_classification():
        print(f'Computing Turbu, subj: {subj}')
        subjData = DL.get_subjectData(subj)
        timeseries = subjData[subj]['timeseries']
        all_results[subj] = computeTurbu_subj(subj, timeseries, range, DL)
        # =======================================================================
        # Save results
        # =======================================================================
        sio.savemat(dataPath + f'turbu_emp_{subj}.mat', all_results[subj])

    print_avgs_and_std(all_results, 'Rspatime', range)  # Change this!!!

# =======================================================================
# ==========================================================================
if __name__=="__main__":
    # decorators.forceCompute = True
    #lambdas = [0.01, 0.03, 0.06, 0.09, 0.12, 0.15, 0.18, 0.21, 0.24, 0.27]
    lambdas = [0.18]
    rev_lambdas = list(reversed(lambdas))  # To have the same order as in Matlab
    computeTurbu(rev_lambdas, DL)
    print("done")

# ================================================================================================================
# ================================================================================================================
# ================================================================================================================EOF