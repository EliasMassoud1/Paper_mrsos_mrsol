# Discrepancies in the Representation of Surface and Layered Soil Moisture in Earth System Models

This repository contains the code associated with the scientific article titled **"Discrepancies in the Representation of Surface and Layered Soil Moisture in Earth System Models"**, which was submitted to *Geophysical Research Letters (GRL)*. The work explores how soil moisture (SM) is represented in different Earth System Models (ESMs) and highlights discrepancies between surface soil moisture (mrsos) and vertically integrated soil moisture (mrsol).

## Table of Contents

- [Project Description](#project-description)
- [Key Findings](#key-findings)
- [How to Use](#how-to-use)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Project Description

Soil moisture (SM) is a critical variable in Earth System Models (ESMs) and is essential for understanding various environmental processes. However, different models represent soil moisture in different ways, leading to discrepancies that can complicate comparisons of model outputs. In particular, the surface soil moisture (mrsos) is often defined consistently across models (top 10 cm), but the representation of layered soil moisture (mrsol) varies based on model-specific definitions of the soil profile.

This study compares the vertically integrated layered soil moisture (mrsol) to surface soil moisture (mrsos) across several models from the 6th Coupled Model Intercomparison Project (CMIP6). Our findings show that while some models' mrsol integrates to match mrsos globally, others exhibit discrepancies, either regionally or throughout the entire globe. These discrepancies arise from issues such as variable mapping inconsistencies, interpolation errors, and model-specific problems like frozen soil handling or incorrect depth definitions.

This repository includes the scripts that facilitate model comparison and visualization of the discrepancies between mrsol and mrsos across different CMIP6 models.

## Key Findings

- **Soil moisture is represented differently**: Different Earth System Models (ESMs) represent soil moisture in different ways, especially the representation of surface soil moisture (mrsos) and vertically integrated soil moisture (mrsol).
- **Surface vs. Layered Moisture Discrepancies**: For some models, the vertically integrated layered soil moisture (mrsol) matches the surface soil moisture (mrsos) globally. For other models, this match occurs only in certain grid cells, and in a few models, it never matches.
- **Challenges in Model Comparisons**: The discrepancies observed between mrsol and mrsos complicate model-based comparisons and highlight the need for standardizing soil moisture definitions across models and improving derived variable accuracy.
- **Implications for Research**: These discrepancies must be carefully considered in any research using model-generated soil moisture data to avoid misleading conclusions.

## License

This project is licensed under a [Creative Commons Attribution 4.0 International License (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).

## Acknowledgments

This research was partially supported by the RUBISCO Science Focus Area (RUBISCO SFA KP1703), which is sponsored by the Regional and Global Model Analysis (RGMA) activity of the Earth and Environmental Systems Modeling (EESM) Program in the Earth and Environmental Systems Sciences Division (EESSD) of the Office of Biological and Environmental Research (BER) in the U.S. Department of Energy Office of Science. This paper has been authored by UT-Battelle, LLC, under contract DE-AC05-00OR22725 with the U.S. Department of Energy (DOE). The U.S. government retains and the publisher, by accepting the article for publication, acknowledges that the U.S. government retains a nonexclusive, paid-up, irrevocable, worldwide license to publish or reproduce the published form of this paper, or allow others to do so, for U.S. government purposes. DOE will provide public access to these results of federally sponsored research in accordance with the DOE Public Access Plan. 
