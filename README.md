# samtools

This repository provides tools, examples, and setup scripts to facilitate the use of the System for Atmospheric Modeling (SAM).

## Repository Structure

- `cases/`  
  Example experimental setups (e.g., RCE_small_300K), including grid and sounding generators, including mean soundings from existing .nc files. 

- `job-scripts/`  
  HPC job submission scripts (e.g., for `qsub`) on Hoffman2.

- `scripts/`  
  Utilities for post-processing SAM output (binary to NetCDF converters, plotting scripts).

- `setup/`  
  Bash scripts to set up a working environment to compile and run SAM.

## Installation 

To install and use the SAM tools:

1. Clone the repository:

    ```bash
    git clone git@github.com:franciscospauldingastudillo/samtools.git
    ```

    or (if you prefer HTTPS):

    ```bash
    git clone https://github.com/franciscospauldingastudillo/samtools.git
    ```

## Quick Start

1. **Set up the SAM linux environment:**

    ```bash
    cd setup
    ./dependencies
    ```

2. **Submit a sample run:**

    ```bash
    cd job-scripts
    qsub ./qsub-RCE_small 300 0
    ```

3. **Post-process and plot results:**

    ```bash
    cd scripts
    python stat_plotter.py RCE_small_300K
    ```

## Requirements

- Python 3.x
- numpy
- matplotlib
- netCDF4

