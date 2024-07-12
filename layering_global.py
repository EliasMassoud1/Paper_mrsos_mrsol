import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
from intake_esgf import ESGFCatalog

# How deep is the layer to integrate
D_MAX = 0.1

mpl.rc("font", **{"size": 18})
model = "CanESM5"  # "CNRM-ESM2-1"  # "UKESM1-0-LL"  # "MPI-ESM1-2-LR" # "CESM2"
# "GFDL-ESM4" # "ACCESS-ESM1-5"  # "BCC-CSM2-MR"  # "CanESM5"  # "NorESM2-LM" # "MIROC6"
cat = ESGFCatalog().search(
    experiment_id="historical",
    variable_id=["mrsol", "mrsos"],
    frequency="mon",
    source_id=model,
)
cat.remove_ensembles()
ds = cat.to_dataset_dict(ignore_facets="table_id", add_measures=True)

# Calculate the long-term mean of the variable
long_term_mean_mrsos = (
    ds["mrsos"].sel(time=slice("2013-01-01", "2015-01-01")).mean(dim="time")
)
long_term_mean_mrsol = (
    ds["mrsol"].sel(time=slice("2013-01-01", "2015-01-01")).mean(dim="time")
)

depth = [d for d in long_term_mean_mrsol.dims if "depth" in d][0]
depth_bnds = long_term_mean_mrsol[depth].attrs["bounds"]
ndepth = int((long_term_mean_mrsol[depth_bnds][:, 0] < D_MAX).sum().values)

# Fractional sum of just the parts that overlap the top 10cm
bnd = long_term_mean_mrsol[depth_bnds].dims[1]
weights = long_term_mean_mrsol[depth_bnds][:ndepth].clip(0, D_MAX).diff(
    dim=bnd
) / long_term_mean_mrsol[depth_bnds][:ndepth].diff(dim=bnd)
method2 = (
    long_term_mean_mrsol["mrsol"][:ndepth]
    .weighted(weights.fillna(0))
    .sum(dim=depth, keep_attrs=True)
)

# Mask out the non-land portions using the land fraction
long_term_mean_mrsos = xr.where(
    ds["mrsol"]["sftlf"] > 1e-8, long_term_mean_mrsos, np.nan, keep_attrs=True
)
method2 = xr.where(ds["mrsol"]["sftlf"] > 1e-8, method2, np.nan, keep_attrs=True)
method2.name = "mrsos"

# Calculate the difference between the long-term means
difference = long_term_mean_mrsos["mrsos"] - method2

# Choose max colorbar value for plot
vmax_plot = float(50)

# Create a figure with three subplots
fig, axs = plt.subplots(1, 3, figsize=(18, 6))

# Plot mrsos in the first subplot
long_term_mean_mrsos["mrsos"].plot(
    ax=axs[0], vmax=vmax_plot
)  # Selecting the DataArray before plotting
axs[0].set_title("Long-term Mean mrsos")
axs[0].set_xlabel("Longitude")
axs[0].set_ylabel("Latitude")

# Plot mrsol in the second subplot
method2.plot(ax=axs[1], vmax=vmax_plot)  # Selecting the DataArray before plotting
axs[1].set_title("Long-term Mean Top 10 cm mrsol")
axs[1].set_xlabel("Longitude")
axs[1].set_ylabel("Latitude")

# Plot the difference in the third subplot
difference.plot(ax=axs[2], cmap="RdBu", center=0, vmin=-5, vmax=5)
axs[2].set_title("Difference (mrsos - mrsol)")
axs[2].set_xlabel("Longitude")
axs[2].set_ylabel("Latitude")

# Adjust layout
plt.tight_layout()
plt.show()
