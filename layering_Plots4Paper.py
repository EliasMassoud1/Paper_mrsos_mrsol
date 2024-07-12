import matplotlib as mpl
import matplotlib.pyplot as plt
import xarray as xr
import intake_esgf
from intake_esgf import ESGFCatalog

# import numpy as np

intake_esgf.conf.set(additional_df_cols=[])


mpl.rc("font", **{"size": 18})

model = "NorESM2-LM"  # "CNRM-ESM2-1"  # "UKESM1-0-LL"  # "MPI-ESM1-2-LR" # "CESM2"
# "GFDL-ESM4" # "ACCESS-ESM1-5"  # "BCC-CSM2-MR"  # "CanESM5"  # "NorESM2-LM" # "MIROC6"
cat = ESGFCatalog().search(
    experiment_id="historical",
    variable_id=["mrsol", "mrsos"],
    frequency="mon",
    source_id=model,
)
cat.remove_ensembles()
# ds = cat.to_dataset_dict(ignore_facets="table_id", add_measures=False)
ds = cat.to_dataset_dict()
for key, d in ds.items():
    if "mrsos" not in d:
        continue
    if "depth" in ds[key]:
        ds[key] = ds[key].drop_vars("depth")
    if "depth_bnds" in d:
        ds[key] = ds[key].drop_vars("depth_bnds")
ds = [
    d.sel(lat=60.0, lon=235.0, method="nearest").isel(time=1807) for _, d in ds.items()
]
ds = xr.merge(ds)
ds.load()
depth = [d for d in ds.dims if "depth" in d][0]
depth_bnds = ds[depth].attrs["bounds"]
ndepth = int((ds[depth_bnds][:, 0] < 0.1).sum().values)

# fractional sum of just the parts that overlap the top 10cm?
bnd = ds[depth_bnds].dims[1]
weights = ds[depth_bnds][:ndepth].clip(0, 0.1).diff(dim=bnd) / ds[depth_bnds][
    :ndepth
].diff(dim=bnd)
method2 = float(ds["mrsol"][:ndepth].weighted(weights).sum())

# plot the soil moisture, layered and surface
fig, ax = plt.subplots(figsize=(6, 10), tight_layout=True)
for d in range(len(ds[depth])):
    lbl = None if d else "mrsol"
    ax.plot(
        [ds["mrsol"][d]] * 2,
        ds[depth_bnds][d],
        "-",
        color="tab:blue",
        lw=2,
        label=lbl,
    )
ax.plot(
    [ds["mrsos"]] * 2,
    [0, 0.1],
    "-",
    color="tab:orange",
    lw=2,
    label=f"mrsos ({ds['mrsos']:.2f})",
)
ax.grid()
ax.set_ylim(0.23, -0.05)
ax.set_xlim(0, 160)
ax.set_xlabel("Soil Moisture [kg m-2]")
ax.set_ylabel("Depth [m]")

ax.plot(
    [method2] * 2,
    [0, 0.1],
    "--",
    color="tab:red",
    lw=2,
    label=f"SM_integrated ({method2:.2f})",
)

fig.legend()
plt.show()


# # fractional sum of just the parts that overlap the top 10cm?
# bnd = ds[depth_bnds].dims[1]
# weights = ds[depth_bnds][:ndepth].clip(0, 0.1).diff(dim=bnd) / ds[depth_bnds][
#     :ndepth
# ].diff(dim=bnd)
# method2 = float(ds["mrsol"][:ndepth].weighted(weights).sum())

# # fractional sum of just the parts that overlap the top 10cm but ignoring the weird
# # negative depth?
# weights = ds[depth_bnds][:ndepth].clip(-0.05, 0.1).diff(dim=bnd) / ds[depth_bnds][
#     :ndepth
# ].diff(dim=bnd)
# method3 = float(ds["mrsol"][:ndepth].weighted(weights).sum())

# ax.plot(
#     [method1] * 2,
#     [0, 0.1],
#     "--",
#     color="tab:green",
#     lw=2,
#     label=f"method1 ({method1:.2f})",
# )
# ax.plot(
#     [method2] * 2,
#     [0, 0.1],
#     "--",
#     color="tab:red",
#     lw=2,
#     label=f"method2 ({method2:.2f})",
# )
# ax.plot(
#     [method3] * 2,
#     [0, 0.1],
#     "--",
#     color="tab:purple",
#     lw=2,
#     label=f"method3 ({method3:.2f})",
# )

# fig.legend()
# # fig.savefig(f"{model}.png")
# # plt.close()
# plt.show()
