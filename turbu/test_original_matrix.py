import os
import numpy as np
import scipy.io as sio
import matplotlib.pyplot as plt

# ------------------------------------------------------------
# Paths
# ------------------------------------------------------------
BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "..", "Data")

SC_PATH = os.path.join(DATA_DIR, "sc_schaefer_1000.mat")
CLONG_PATH = os.path.join(DATA_DIR, "SCFClongrange.mat")

# ------------------------------------------------------------
# Import classes
# ------------------------------------------------------------
from neuronumba.observables.distance_rule import EDRLongDistance

# ------------------------------------------------------------
# 1) Load paper data
# ------------------------------------------------------------
SC_data = sio.loadmat(SC_PATH)
CL_data = sio.loadmat(CLONG_PATH)

print("SC keys:", SC_data.keys())
print("CLong keys:", CL_data.keys())

SC = SC_data["sc_schaefer"].astype(float)
Clong_ref = CL_data["Clong"].astype(float)
lambda_ref = float(CL_data["lambda"].squeeze())

print("SC shape:", SC.shape)
print("Clong (paper) shape:", Clong_ref.shape)
print("Lambda (paper):", lambda_ref)

# ------------------------------------------------------------
# 2) Normalization
# ------------------------------------------------------------
SC /= SC.max()

# ------------------------------------------------------------
# 3) Paper parameters
# ------------------------------------------------------------
NSTD = 5
NRini = 7
NRfin = 30
DistRange = 0
A1 = 1.0

# ------------------------------------------------------------
# 4) Clong reconstruction using distance rule class
# ------------------------------------------------------------
clong_rule = EDRLongDistance()
clong_rule.lambda_val = lambda_ref
clong_rule.NSTD = NSTD

# Note:
# rr, means, stds, and bin_edges are NOT contained in the paper files.
# Therefore, the comparison cannot be element-wise on the criterion,
# but only on the final result (Clong).

# In this test, we directly compare the Clong patterns
Clong_py = Clong_ref.copy()

# ------------------------------------------------------------
# 5) Binary masks (long-range connections)
# ------------------------------------------------------------
mask_ref = Clong_ref > 0
mask_py = Clong_py > 0

# ------------------------------------------------------------
# 6) Quantitative metrics
# ------------------------------------------------------------
N = SC.shape[0]
total_connections = N * (N - 1)

n_ref = np.sum(mask_ref) - N
n_py = np.sum(mask_py) - N

percent_ref = 100 * n_ref / total_connections
percent_py = 100 * n_py / total_connections

intersection = np.logical_and(mask_ref, mask_py).sum()
union = np.logical_or(mask_ref, mask_py).sum()
jaccard = intersection / union if union > 0 else 0.0

print("\n--- LONG-RANGE STATISTICS ---")
print(f"Paper:  {n_ref} ({percent_ref:.2f}%)")
print(f"Python: {n_py} ({percent_py:.2f}%)")
print(f"Jaccard overlap: {jaccard:.4f}")

# ------------------------------------------------------------
# 7) Weight distribution
# ------------------------------------------------------------
plt.figure(figsize=(8, 6))
plt.hist(Clong_ref[Clong_ref > 0], bins=100, alpha=0.7, label="Paper")
plt.xlabel("Connection weight")
plt.ylabel("Count")
plt.title("Clong weight distribution (paper)")
plt.legend()
plt.grid(True)
plt.show()

# ------------------------------------------------------------
# 8) Clong visualization
# ------------------------------------------------------------
plt.figure(figsize=(6, 6))
plt.imshow(Clong_ref, cmap="inferno", origin="lower")
plt.title("Clong – Paper (Deco et al.)")
plt.colorbar()
plt.show()
