import matplotlib as mpl
import matplotlib.pyplot as plt
import xarray as xr
from intake_esgf import ESGFCatalog
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# Set projection
projection = ccrs.Robinson()
mpl.rc("font", **{"size": 24})  # Increase font size for better readability

# Define models to plot
models = ["ACCESS-ESM1-5", "BCC-CSM2-MR", "CESM2"]

# Set layer depth
D_MAX = 0.1

# Create figure with tighter spacing
fig, axs = plt.subplots(
    3,
    3,
    figsize=(18, 16),  # Reduce height to minimize excess spacing
    subplot_kw={"projection": projection},
    constrained_layout=True,  # Automatically optimize layout
)

# Reduce spacing between rows and columns
plt.subplots_adjust(hspace=0.1, wspace=0.1)

for i, model in enumerate(models):
    # Load dataset
    cat = ESGFCatalog().search(
        experiment_id="historical",
        variable_id=["mrsol", "mrsos"],
        frequency="mon",
        source_id=model,
    )
    cat.remove_ensembles()
    ds = cat.to_dataset_dict(ignore_facets="table_id", add_measures=False)

    # Compute long-term means
    long_term_mean_mrsos = (
        ds["mrsos"].sel(time=slice("2013-01-01", "2015-01-01")).mean(dim="time")
    )
    long_term_mean_mrsol = (
        ds["mrsol"].sel(time=slice("2013-01-01", "2015-01-01")).mean(dim="time")
    )

    # Determine depth bounds
    depth = [d for d in long_term_mean_mrsol.dims if "depth" in d][0]
    depth_bnds = long_term_mean_mrsol[depth].attrs["bounds"]
    ndepth = int((long_term_mean_mrsol[depth_bnds][:, 0] < D_MAX).sum().values)

    # Weighted sum of the top 10cm
    bnd = long_term_mean_mrsol[depth_bnds].dims[1]
    weights = long_term_mean_mrsol[depth_bnds][:ndepth].clip(0, D_MAX).diff(
        dim=bnd
    ) / long_term_mean_mrsol[depth_bnds][:ndepth].diff(dim=bnd)
    method2 = long_term_mean_mrsol["mrsol"][:ndepth].weighted(weights).sum(dim=depth)

    # Compute difference
    difference = long_term_mean_mrsos["mrsos"] - method2

    # Define color limits
    vmax_plot = 50

    # Mask zeros
    masked_mrsos = long_term_mean_mrsos["mrsos"].where(
        long_term_mean_mrsos["mrsos"] != 0
    )
    masked_mrsol = method2.where(method2 != 0)
    masked_difference = difference.where(difference != 0)

    # Plot mrsos
    mrsos_plot = masked_mrsos.plot(
        ax=axs[i, 0],
        vmax=vmax_plot,
        transform=ccrs.PlateCarree(),
        add_colorbar=False,  # Remove subplot colorbars
        add_labels=False,  # Prevent "depth = 0.05 [m]" title
    )
    axs[i, 0].coastlines(linewidth=0.6)
    axs[i, 0].add_feature(cfeature.BORDERS, linewidth=0.3)
    axs[i, 0].set_global()

    # Plot mrsol
    masked_mrsol.plot(
        ax=axs[i, 1],
        vmax=vmax_plot,
        transform=ccrs.PlateCarree(),
        add_colorbar=False,  # Remove subplot colorbars
        add_labels=False,  # Prevent "depth = 0.05 [m]" title
    )
    axs[i, 1].coastlines(linewidth=0.6)
    axs[i, 1].add_feature(cfeature.BORDERS, linewidth=0.3)
    axs[i, 1].set_global()

    # Plot difference
    masked_difference.plot(
        ax=axs[i, 2],
        vmin=-5,
        vmax=5,
        cmap="RdBu",
        center=0,
        transform=ccrs.PlateCarree(),
        add_colorbar=False,  # Remove subplot colorbars
        add_labels=False,  # Prevent "depth = 0.05 [m]" title
    )
    axs[i, 2].coastlines(linewidth=0.6)
    axs[i, 2].add_feature(cfeature.BORDERS, linewidth=0.3)
    axs[i, 2].set_global()

    # Add model name and panel-specific titles
    axs[i, 0].text(
        0.5,
        1.1,
        f"mrsos - {model}",
        transform=axs[i, 0].transAxes,
        ha="center",
        va="bottom",
        fontsize=24,
        fontweight="bold",
    )
    axs[i, 1].text(
        0.5,
        1.1,
        f"mrsol - {model}",
        transform=axs[i, 1].transAxes,
        ha="center",
        va="bottom",
        fontsize=24,
        fontweight="bold",
    )
    axs[i, 2].text(
        0.5,
        1.1,
        f"Difference - {model}",
        transform=axs[i, 2].transAxes,
        ha="center",
        va="bottom",
        fontsize=24,
        fontweight="bold",
    )

# Show plot
plt.show()
fig.savefig("global_All_Bias.png", dpi=300)
