# --------------------------------------------------------------------------------------
# Iintrinsic ignition functions, for convenience in a sepparate file
#
# By Gustavo Patow
#
# --------------------------------------------------------------------------------------
from neuronumba.tools.filters import BandPassFilter

from setup import *


def filer_fMRI(fMRI):  # fMRI in (time, RoIs) format
    # ========================================================================
    # We create the bandpass filter we will use for the signals
    bpf = BandPassFilter(
        k=2,
        flp=configs[config][0],
        fhi=configs[config][1],
        tr=DL.TR() * 1000.,
        apply_detrend=True,
        apply_demean=True,
        remove_artifacts=True
    )
    return bpf.filter(fMRI)


def compute_ignition(ignition, fMRI):  # fMRI in (time, RoIs) format
    filt_fMRI = filer_fMRI(fMRI)
    igni = ignition.from_fmri(filt_fMRI)
    return igni
