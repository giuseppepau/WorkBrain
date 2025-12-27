# --------------------------------------------------------------------------------------
# Simple intrinsic ignition tests for the group subjects (given by the DataLoader groups)
#
# By Gustavo Patow
#
# Pre-requisites:
#   Before executing this, be sure to have correctly configured the setup.py file...
#
# --------------------------------------------------------------------------------------
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

# import Utils.decorators as decorators
import src.neuronumba.observables.intrinsic_ignition as igniLib

import LibBrain.Plotting.p_values as p_values
import LibBrain.Utils.Stats.statannotations_permutation as perm_test

import LibBrain.Plotting.plot3DBrain_Utils as plot3D
import LibBrain.Plotting.project3DBrain as project3D

from setup import *
from igni_funcs import *


def computeIgnitions(ignition, fMRIs, group):
    results = {}
    for subject in fMRIs:
        print(f'Processing {group}: {subject}')
        filename = save_folder+f'/{ignition.modalityName[ignition.modality]}_{subject}.mat'
        fMRI = fMRIs[subject]['timeseries'].T  # We need (time, RoIs)
        results[subject] = compute_ignition(ignition, fMRI)  #, filename)
    return np.array([results[s]['mevokedinteg'] for s in results]).T, \
           np.array([results[s]['stdevokedinteg'] for s in results]).T


def run():
    plt.rcParams.update({'font.size': 15})
    # --------------------------------------------------
    # Setup observable!!!
    # --------------------------------------------------
    ignition = igniLib.Intrinsic_Ignition()
    ignition.modality = ignition.EventBasedIntrinsicIgnition  # EventBasedIntrinsicIgnition / PhaseBasedIntrinsicIgnition
    # --------------------------------------------------
    # Process fMRI for all subjects
    # --------------------------------------------------
    subj_or_nodes = 1  # 0 = subjects; 1 = nodes
    # --------------------------------------------------
    datasetLabels = DL.get_groupLabels()
    igniResults = {}
    metaResults = {}
    for cohort in datasetLabels:
        all_fMRI = DL.get_fullGroup_data(cohort)
        ignis, metas = computeIgnitions(ignition, all_fMRI, cohort)
        igniResults[cohort] = np.mean(ignis, axis=subj_or_nodes)
        metaResults[cohort] = np.mean(metas, axis=subj_or_nodes)

    labelText = 'Node' if subj_or_nodes == 1 else 'Subject'
    p_values.plotComparisonAcrossLabels2(igniResults, custom_test=perm_test.custom_permutation(),
                                         columnLables=datasetLabels, graphLabel=labelText+'-Ignition')
    p_values.plotComparisonAcrossLabels2(metaResults, custom_test=perm_test.custom_permutation(),
                                         columnLables=datasetLabels, graphLabel=labelText+'-Metastability')

    # --------------------------------------------------
    # Plot 3D average ignis and metas for each cohort
    # --------------------------------------------------
    do_plot3D = False
    if do_plot3D:
        plots_path = './_Results/Plots3D_IgniMeta/'
        if not os.path.isdir(plots_path):
            os.makedirs(plots_path)
        parcel = DL.get_parcellation()
        coords = parcel.get_CoGs()
        crtx = project3D.set_up_cortex(coords)
        plot3D.plot_multiview5ValuesForEachChort(igniResults, crtx,
                                                 title='', metaName=' Ignition',
                                                 cmap=cm.RdBu_r, display=False,
                                                 path=plots_path)
        plot3D.plot_multiview5ValuesForEachChort(metaResults, crtx,
                                                 title='', metaName=' Metastability',
                                                 cmap=cm.RdBu_r, display=False,
                                                 path=plots_path)

    # plot_TopViewValuesForAllCohorts(igniResults, testColors=cm.Blues)  # _r means reversed colormap
    # plot_TopViewValuesForAllCohorts(metaResults, testColors=cm.RdBu_r)

    print('done!')


# ================================================================================================================
if __name__ == '__main__':
    run()
# ================================================================================================================
# ================================================================================================================
# ================================================================================================================EOF
