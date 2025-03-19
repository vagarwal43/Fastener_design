# FEniCS-GMSH Automation for Factor of Safety (FOS) Calculation

This project automates the process of calculating the **Factor of Safety (FOS)** for a 3D geometry defined in a STEP file. It uses **GMSH** for mesh generation and **FEniCS** for finite element analysis (FEA). The workflow is encapsulated in a single Python function, making it easy to use and integrate into larger workflows.

---

## Table of Contents
1. [Overview](#overview)
2. [Dependencies](#dependencies)
3. [Inputs](#inputs)
4. [Outputs](#outputs)


---

## Overview

The project consists of a single Python function, `calculate_fos`, which takes a STEP file and material properties as input and returns the Factor of Safety (FOS). The function performs the following steps:

1. **Mesh Generation**: Uses GMSH to generate a 3D mesh from the STEP file.
2. **Mesh Conversion**: Converts the GMSH mesh into XDMF format for use in FEniCS.
3. **Finite Element Analysis**: Solves the mechanical problem using FEniCS to compute stresses.
4. **FOS Calculation**: Computes the von Mises stress and calculates the Factor of Safety (FOS) based on the yield stress.

---

## Dependencies

The code relies on the following Python libraries:
- **FEniCS**: For finite element analysis.
- **GMSH**: For mesh generation.
- **meshio**: For converting GMSH mesh files to XDMF format.

Make sure you have the following installed:
- Python 3.x
- FEniCS (install via [FEniCS documentation](https://fenicsproject.org/download/))
- GMSH (install via [GMSH documentation](https://gmsh.info/doc/texinfo/gmsh.html))
- `meshio` (install via `pip install meshio`)

---

# Inputs

| Parameter | Type | Description |
| ------------- | ------------- | ------------- |
| step_file  | str |	Path to the STEP file containing the 3D geometry. |
| E | float |	Young's modulus of the material (in Pascals). |
| nu | float |	Poisson's ratio of the material. |
| yield_stress | float |	Yield stress of the material (in Pascals). |
| left_wall_tag | int |	Physical tag for the left wall boundary in the STEP file. |
| right_wall_tag | int |	Physical tag for the right wall boundary in the STEP file. |
| traction_force | tuple (float) |	Traction force vector applied to the right wall (in Pascals). |

---

# Outputs

The function returns a single output:
Factor of Safety (FOS): A float value representing the ratio of yield stress to the maximum von Mises stress.


