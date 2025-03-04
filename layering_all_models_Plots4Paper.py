import matplotlib as mpl
import matplotlib.pyplot as plt
import xarray as xr
import intake_esgf
from intake_esgf import ESGFCatalog

# Configure ESGF
intake_esgf.conf.set(additional_df_cols=[])

mpl.rc("font", **{"size": 16})

# List of models sorted alphabetically
models = sorted(
    [
        "ACCESS-ESM1-5",
        "BCC-CSM2-MR",
        "CanESM5",
        "CESM2",
        "CNRM-ESM2-1",
        "MIROC6",
        "MPI-ESM1-2-LR",
        "NorESM2-LM",
        "UKESM1-0-LL",
    ]
)

# Create a figure with a 3x3 grid of subplots
fig, axs = plt.subplots(3, 3, figsize=(15, 15), tight_layout=True)
axs = axs.flatten()  # Flatten for easier indexing

# Iterate over models and subplots
for i, model in enumerate(models):
    ax = axs[i]

    try:
        # Search for data
        cat = ESGFCatalog().search(
            experiment_id="historical",
            variable_id=["mrsol", "mrsos"],
            frequency="mon",
            source_id=model,
        )
        cat.remove_ensembles()
        ds = cat.to_dataset_dict()

        # Filter and process data
        for key, d in ds.items():
            if "mrsos" not in d:
                continue
            if "depth" in ds[key]:
                ds[key] = ds[key].drop_vars("depth")
            if "depth_bnds" in d:
                ds[key] = ds[key].drop_vars("depth_bnds")
        ds = [
            d.sel(lat=60.0, lon=235.0, method="nearest").isel(time=1807)
            for _, d in ds.items()
        ]
        ds = xr.merge(ds)
        ds.load()
        depth = [d for d in ds.dims if "depth" in d][0]
        depth_bnds = ds[depth].attrs["bounds"]
        ndepth = int((ds[depth_bnds][:, 0] < 0.1).sum().values)

        # Compute weighted soil moisture for the top 10cm
        bnd = ds[depth_bnds].dims[1]
        weights = ds[depth_bnds][:ndepth].clip(0, 0.1).diff(dim=bnd) / ds[depth_bnds][
            :ndepth
        ].diff(dim=bnd)
        method2 = float(ds["mrsol"][:ndepth].weighted(weights).sum())

        # Plot soil moisture
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
        ax.plot(
            [method2] * 2,
            [0, 0.1],
            "--",
            color="tab:red",
            lw=2,
            label=f"SM_integrated ({method2:.2f})",
        )

        # Set axis labels and title
        ax.set_ylim(0.23, -0.05)
        ax.set_xlim(0, 160)
        ax.set_xlabel("Soil Moisture [kg m-2]")
        ax.set_ylabel("Depth [m]")
        ax.set_title(model)

        # Add legend for each subplot
        ax.legend(loc="upper right", fontsize=12)

    except Exception as e:
        ax.text(0.5, 0.5, f"Error: {str(e)}", ha="center", va="center", fontsize=12)
        ax.set_title(model)
        ax.axis("off")

# Remove unused subplots
for j in range(len(models), len(axs)):
    fig.delaxes(axs[j])


# Save the figure
fig.savefig("layering_all_models.png", dpi=300)

# Display the plot
plt.show()
