import matplotlib as mpl
import matplotlib.pyplot as plt
import xarray as xr
from intake_esgf import ESGFCatalog
import numpy as np

# import cartopy.crs as ccrs

# How deep is the layer to integrate
D_MAX = 0.1

mpl.rc("font", **{"size": 18})
model = "CESM2"  # "CNRM-ESM2-1"  # "UKESM1-0-LL"  # "MPI-ESM1-2-LR" # "CESM2"
# "GFDL-ESM4" # "ACCESS-ESM1-5"  # "BCC-CSM2-MR"  # "CanESM5"  # "NorESM2-LM" # "MIROC6"
cat = ESGFCatalog().search(
    experiment_id="historical",
    variable_id=["mrsol", "mrsos"],
    frequency="mon",
    source_id=model,
)
cat.remove_ensembles()
ds = cat.to_dataset_dict(ignore_facets="table_id", add_measures=False)
# ds.load()

# for key, d in ds.items():
#     if "mrsos" not in d:
#         continue
#     if "depth" in ds[key]:
#         ds[key] = ds[key].drop_vars("depth")
#     if "depth_bnds" in d:
#         ds[key] = ds[key].drop_vars("depth_bnds")
# ds = [
#     d.sel(lat=60.0, lon=235.0, method="nearest").isel(time=1807) for _, d in ds.items()
# ]
# ds = xr.merge(ds)
# ds.load()
# depth = [d for d in ds.dims if "depth" in d][0]
# depth_bnds = ds[depth].attrs["bounds"]
# ndepth = int((ds[depth_bnds][:, 0] < D_MAX).sum().values)

# # # fractional sum of just the parts that overlap the top 10cm?
# bnd = ds[depth_bnds].dims[1]
# weights = ds[depth_bnds][:ndepth].clip(0, D_MAX).diff(dim=bnd) / ds[depth_bnds][
#     :ndepth
# ].diff(dim=bnd)
# method2 = float(ds["mrsol"][:ndepth].weighted(weights).sum())


# fig, ax = plt.subplots(figsize=(6, 10), tight_layout=True)
# for d in range(len(ds[depth])):
#     lbl = None if d else "mrsol"
#     ax.plot(
#         [ds["mrsol"][d]] * 2,
#         ds[depth_bnds][d],
#         "-",
#         color="tab:blue",
#         lw=2,
#         label=lbl,
#     )
# ax.grid()
# ax.set_ylim(0.23, -0.05)
# ax.set_xlim(0, 160)
# ax.set_xlabel("Soil Moisture [kg m-2]")
# ax.set_ylabel("Depth [m]")
# ax.plot(
#     [ds["mrsos"]] * 2,
#     [0, 0.1],
#     "-",
#     color="tab:orange",
#     lw=2,
#     label=f"mrsos ({ds['mrsos']:.2f})",
# )
# ax.plot(
#     [method2] * 2,
#     [0, D_MAX],
#     "--",
#     color="tab:red",
#     lw=2,
#     label=f"method2 ({method2:.2f})",
# )
# fig.legend()
# # fig.savefig(f"{model}.png")
# # plt.close()
# plt.show()


# 1. Calculate the long-term mean of the variable
long_term_mean_mrsos = (
    ds["mrsos"].sel(time=slice("2013-01-01", "2015-01-01")).mean(dim="time")
)
# long_term_mean_mrsol = ds["mrsol"].isel(depth=0).mean(dim="time")
long_term_mean_mrsol = (
    ds["mrsol"].sel(time=slice("2013-01-01", "2015-01-01")).mean(dim="time")
)

depth = [d for d in long_term_mean_mrsol.dims if "depth" in d][0]
depth_bnds = long_term_mean_mrsol[depth].attrs["bounds"]
ndepth = int((long_term_mean_mrsol[depth_bnds][:, 0] < D_MAX).sum().values)

# # fractional sum of just the parts that overlap the top 10cm?
bnd = long_term_mean_mrsol[depth_bnds].dims[1]
weights = long_term_mean_mrsol[depth_bnds][:ndepth].clip(0, D_MAX).diff(
    dim=bnd
) / long_term_mean_mrsol[depth_bnds][:ndepth].diff(dim=bnd)
method2 = long_term_mean_mrsol["mrsol"][:ndepth].weighted(weights).sum(dim=depth)


# Calculate the difference between the long-term means
difference = long_term_mean_mrsos["mrsos"] - method2

# Choose max colorbar value for plot
# vmax_plot = float(max(method2.max(), long_term_mean_mrsos["mrsos"].max()))
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
axs[1].set_title("Long-term Mean mrsol")
axs[1].set_xlabel("Longitude")
axs[1].set_ylabel("Latitude")

# Plot the difference in the third subplot
difference.plot(ax=axs[2], vmin=-5, vmax=5, cmap="RdBu", center=0)
axs[2].set_title("Difference (mrsos - mrsol)")
axs[2].set_xlabel("Longitude")
axs[2].set_ylabel("Latitude")

# Adjust layout
plt.tight_layout()
plt.show()


# for key, d in ds.items():
#     if "mrsos" not in d:
#         continue
#     if "depth" in ds[key]:
#         ds[key] = ds[key].drop_vars("depth")
#     if "depth_bnds" in d:
#         ds[key] = ds[key].drop_vars("depth_bnds")
# ds = [
#     d.sel(lat=60.0, lon=235.0, method="nearest").isel(time=1807) for _, d in ds.items()
# ]
# ds = xr.merge(ds)
# ds.load()
# depth = [d for d in ds.dims if "depth" in d][0]
# depth_bnds = ds[depth].attrs["bounds"]
# ndepth = int((ds[depth_bnds][:, 0] < D_MAX).sum().values)


# # fractional sum of just the parts that overlap the top 10cm?
# bnd = ds[depth_bnds].dims[1]
# weights = ds[depth_bnds][:ndepth].clip(0, D_MAX).diff(dim=bnd) / ds[depth_bnds][
#     :ndepth
# ].diff(dim=bnd)
# method2 = float(ds["mrsol"][:ndepth].weighted(weights).sum())


# ax.plot(
#     [method2] * 2,
#     [0, D_MAX],
#     "--",
#     color="tab:red",
#     lw=2,
#     label=f"method2 ({method2:.2f})",
# )
# fig.legend()
# fig.savefig(f"{model}.png")
# plt.close()
