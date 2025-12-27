import sys
import os
import numpy as np
import matplotlib.pyplot as plt

# Fix the path to locate LibBrain
libbrain_src = "/home/alessandrofloris/Documenti/giuse/LibBrain/src"
sys.path.insert(0, libbrain_src)
sys.path.insert(0, os.path.join(libbrain_src, "LibBrain"))

# ------------------------------------------------------------------
# DistanceRule and Clong
from neuronumba.observables.distance_rule import EDR_distance_rule, EDRLongDistance

# DataLoader
import LibBrain.DataLoaders.ADNI_A as ADNI

# ------------------------------------------------------------------
# 1) Load the DataLoader
# ------------------------------------------------------------------
DL = ADNI.ADNI_A(cutTimeSeries=True)
coords = DL.get_parcellation().get_CoGs()
print("CoG shape:", coords.shape)

# ------------------------------------------------------------------
# 2) Use the real SC matrix from the first HC subject
# ------------------------------------------------------------------
subject = DL.get_groupSubjects('HC')[0]
subjectData = DL.get_subjectData(subject)[subject]
SC_matrix = subjectData['SC'].astype(float)
print("SC matrix shape:", SC_matrix.shape)

# ------------------------------------------------------------------
# Normalize SC between 0 and 1
# ------------------------------------------------------------------
SC_max = SC_matrix.max()
if SC_max > 0:
    SC_matrix /= SC_max

# ------------------------------------------------------------------
# 3) Create the DistanceRule and compute rr and c_exp
# ------------------------------------------------------------------
lambda_val = 0.18
distance_rule = EDR_distance_rule()
distance_rule.lambda_val = lambda_val
rr, c_exp = distance_rule.compute(coords)
print("rr shape:", rr.shape)
print("c_exp shape:", c_exp.shape)

# ------------------------------------------------------------------
# 4) Histogram parameters
# ------------------------------------------------------------------
NR = 144  # number of distance bins
means, stds, bin_edges, maxs = distance_rule.compute_hist(c_exp, rr, NR)
centers = (bin_edges[:-1] + bin_edges[1:]) / 2

# ------------------------------------------------------------------
# 5) Exponential fit to estimate lambda
# ------------------------------------------------------------------
lambda_fit = distance_rule.fit_exponential(centers, means)
print("\nEstimated lambda:", lambda_fit)

# ------------------------------------------------------------------
# 6) Histogram plot
# ------------------------------------------------------------------
plt.figure(figsize=(8, 6))
plt.errorbar(centers, means, yerr=stds, fmt='o', markersize=4, capsize=3, label='Histogram')
plt.plot(centers, means[0] * np.exp(-lambda_fit * centers), 'r-', label=f'Exp fit: λ={lambda_fit:.3f}')
plt.plot(centers, maxs, 'green')
plt.xlabel("Distance")
plt.ylabel("Mean SC (± std)")
plt.title("Histogram: SC decay with distance")
plt.legend()
plt.grid(True)
plt.show()

# ------------------------------------------------------------------
# 7) Compute Clong
# ------------------------------------------------------------------
clong_rule = EDRLongDistance()
clong_rule.NSTD = 5  # Number of standard deviations
clong_rule.lambda_val = lambda_fit

# Mandatory parameters
NRini = 7      # first significant bin
NRfin = 30    # last significant bin
DistRange = 0  # minimum distance
A1 = 1

Clong = clong_rule.compute_Clong(
    rr, SC_matrix, means, stds, bin_edges,
    NRini, NRfin, DistRange=DistRange, A1=A1
)

# Now compute EDR on Clong
EDR_Clong = clong_rule.compute(rr, Clong)

print("Clong shape:", Clong.shape)
print("EDR+Clong shape:", EDR_Clong.shape)

# ------------------------------------------------------------------
# 7b) Matrix statistics (for debugging)
# ------------------------------------------------------------------
for name, mat in zip(['c_exp', 'Clong', 'EDR+Clong'], [c_exp, Clong, EDR_Clong]):
    print(f"{name}: min={mat.min():.6f}, max={mat.max():.6f}, mean={mat.mean():.6f}, std={mat.std():.6f}")

# ------------------------------------------------------------------
# 7c) Check selected bins values and long-range connections
# ------------------------------------------------------------------
print("\nMeans and stds of selected bins (NRini → NRfin):")
N = Clong.shape[0]
long_range_mask = np.zeros_like(Clong, dtype=bool)  # binary matrix of long-range connections

for i in range(NRini - 1, NRfin):
    mv = means[i]
    st = stds[i]
    threshold = mv + clong_rule.NSTD * st
    in_bin = (np.digitize(rr, bin_edges) - 1 == i)
    in_bin_upper = (SC_matrix > threshold)
    mask = in_bin & in_bin_upper & (rr > DistRange)
    long_range_mask |= mask
    n_conn_bin = np.sum(mask) - np.trace(mask)  # exclude diagonal
    print(
        f"Bin {i+1}: mean={mv:.6f}, std={st:.6f}, "
        f"threshold={threshold:.6f}, connections={n_conn_bin}"
    )

# ------------------------------------------------------------------
# 9) Percentage of long-range connections
# ------------------------------------------------------------------
total_connections = N * (N - 1)
long_range_connections = np.sum(long_range_mask) - N  # exclude diagonal
percent_long_range = 100 * long_range_connections / total_connections

print(f"\nTotal long-range connections: {long_range_connections}/{total_connections}")
print(f"Percentage of long-range connections: {percent_long_range:.2f}%")

# ------------------------------------------------------------------
# 8) Matrix visualization
# ------------------------------------------------------------------
vmin = min(c_exp.min(), Clong.min(), EDR_Clong.min())
vmax = max(c_exp.max(), Clong.max(), EDR_Clong.max())

fig, axes = plt.subplots(1, 3, figsize=(18, 6))
fig.patch.set_facecolor('black')
matrices = [c_exp, Clong, EDR_Clong]
titles = ['EDR', 'Clong', 'EDR+Clong']

for ax, mat, title in zip(axes, matrices, titles):
    im = ax.imshow(mat, cmap='inferno', origin='lower', vmin=vmin, vmax=vmax)
    ax.set_title(title, color='white')
    ax.set_facecolor('black')
    ax.tick_params(colors='white')
    plt.colorbar(im, ax=ax, orientation='vertical')

plt.tight_layout()
plt.show()
