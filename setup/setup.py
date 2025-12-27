# --------------------------------------------------------------------------------------
# Setup file for processing AD, MCI and HC subjects
#
# By Gustavo Patow
#
# --------------------------------------------------------------------------------------
import os

dataset = 'ADNI_A' #/ ADNI_B_N238rev / ADNI_B_N238rev_alt

if dataset == 'ADNI_A':
    from LibBrain.DataLoaders import ADNI_A
    DL = ADNI_A.ADNI_A(use360=True,  cutTimeSeries=False, normalizeBurden=False)
    config = 0
elif 'ADNI_B' in dataset:
    from LibBrain.DataLoaders import ADNI_B_N238rev
    new_classification = ['HC(AB-)', 'HC(AB+)', 'MCI(AB+)', 'AD(AB+)']
    DL = ADNI_B_N238rev.ADNI_B_Alt(new_classification) #,
                                   # prefiltered_fMRI=False)
    config = 1

# ==========================================================================
# Important config options: filenames
# ==========================================================================
# ---------- Base analysis
if dataset == 'ADNI_A':
    save_folder = "./_Data_Produced/" + DL.name()
elif 'ADNI_B' in dataset:
    save_folder = "./_Data_Produced/" + dataset + "-" + str(config)
if not os.path.isdir(save_folder):  # just in case, create it!!!
    os.makedirs(save_folder)
# ---------- RSN analysis
RSN_save_folder = save_folder + f'/RSN'
if not os.path.isdir(RSN_save_folder):  # just in case, create it!!!
    os.makedirs(RSN_save_folder)

# ==========================================================================
# Configurations (ADNI_B_N238rev: 0.008 ~ 0.08)
# ADNI has a TR = 3 => Nyquist feq = 0.16
# ==========================================================================
if dataset == 'ADNI_A':
    configs = {0: (0.01, 0.09)}
elif 'ADNI_B' in dataset:
    configs = {            # all groups -> HC & AD -> RSN
        1: (0.01, 0.09),  #
        2: (0.008, 0.08),  # default: kk -> ! -> kk (kk@limbic, kk@cont)
        -3: (0.004, 0.007),  # Wrong!!!
        4: (0.04, 0.07),  # ! ->-> kk (ns@cont)
        5: (0.04, 0.08),  # kk -> ! -> kk (kk@cont)
        6: (0.03, 0.07),  # ! ->> kk (ns@cont)
        7: (0.02, 0.07),  # ! ->> kk (ns@limbic, kk@cont)
        8: (0.01, 0.08),  # kk -> ! -> kk (kk@limbic, kk@cont)
        9: (0.01, 0.07),  # kk -> ! -> kk (kk@limbic, kk@cont)
        10: (0.04, 0.075),  # ! ->> kk (kk@cont)
        11: (0.04, 0.079),  # kk -> ! -> kk (kk@cont)
        12: (0.04, 0.077),  # kk (11 > 12 > 10 > 4) -> ! -> kk (kk@cont)
        13: (0.04, 0.072),  # ! ->> kk (ns@cont)
    }


# import WholeBrain.Observables.BOLDFilters as BOLDFilters
# BOLDFilters.flp, BOLDFilters.fhi = configs[config]
# BOLDFilters.TR = 3.
# BOLDFilters.finalDetrend = True


# --------------------------------------------------
# Classify subject information into {HC, MCI, AD}
# --------------------------------------------------
# def getSubjects(cohort, classification):
#     return [s for s in classification if classification[s] == cohort]


# subjects = [os.path.basename(f.path) for f in os.scandir(base_folder+"/connectomes/") if f.is_dir()]
# classification = dataLoader.checkClassifications(subjects)
# classification = DL.get_classification()
# HCSubjects = [s for s in classification if classification[s] == 'HC']
# ADSubjects = [s for s in classification if classification[s] == 'AD']
# MCISubjects = [s for s in classification if classification[s] == 'MCI']
# print(f"We have {len(HCSubjects)} HC, {len(MCISubjects)} MCI and {len(ADSubjects)} AD \n")
# print("HCSubjects:", HCSubjects)
# print("ADSubjects", ADSubjects)
# print("MCISubjects", MCISubjects)

# --------------------------------------------------
# RSN part
# --------------------------------------------------
useLR = False
# If a mode detailed region is NOT needed, use an empty detailNetworks
detailNetworksEmpty = {}
# outParcellationRSNPath = '../../Data_Produced/Parcellations/Glasser360RSN.csv'

# If a more detailed region is needed, especify it here (see comment for collectNamesAndIDsRSN)
# In this case, we want a more detailed DMN
# detailNetworks = {'Default': ['PFC', 'Par', 'Temp', 'pCunPCC', 'PHC']}
# detailNetworksFullNames = ['Default_'+name for name in detailNetworks['Default']]  #['Default_PFC', 'Default_Par', 'Default_Temp', 'Default_pCunPCC', 'Default_PHC']
# # outParcellationRSNDetailPath = f'../../Data_Produced/Parcellations/Glasser360RSN_{"14" if useLR else "7"}_Detail-{"-".join(detailNetworks.keys())}_indices.csv'
# indicesFileParcellationRSNDetail = f'../../Data_Produced/Parcellations/Glasser360RSN_{"14" if useLR else "7"}_Detail-Default_indices.csv'  # For the detailed DMN


