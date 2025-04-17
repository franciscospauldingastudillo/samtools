import argparse
import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt
import sys
import glob
import os

# Define a dictionary mapping keys to potential NetCDF variable names with individual descriptions
VARIABLE_MAP = {
    "2Dthermo": {
        "variables": {
            "TABS": "Absolute temperature [K]",
            "RELH": "Relative humidity [%]",
            "RHO": "Air Density [kg/m^3]",
            "QV": "Water vapor [g/kg]",
            "p": "Pressure [mb]",
            "z": "Height [m]",
        }
    },
    "1Dthermo": {
        "variables": {
            "Ps": "Surface pressure [mb]",
            "SST": "Sea surface temperature [K]",
            "PREC": "Surface precipitation rate [mm/day]",
            "LHF": "Latent heat flux [W/m^2]",
            "SHF": "Sensible heat flux [W/m^2]",
            "CAPE": "Convective available potential energy [J/kg]"
        }
    },
    "cloud": {
        "variables": {
            "CLD": "Cloud fraction [dimensionless]"
        }
    },
    "rad": {
        "variables": {
            "RADQR": "Radiative heating rate [K/day]"
        }
    }
}

def find_variable(dataset, key):
    """Find the first matching variable from the dataset and return its name and description."""
    if key in VARIABLE_MAP:
        for var, desc in VARIABLE_MAP[key]["variables"].items():
            if var in dataset.variables:
                return var, desc
    return None, None

def find_nc_file(nc_pattern):
    """Find the first NetCDF file that matches the pattern."""
    matching_files = glob.glob(f"/data/fspauldinga/SAM6.11.8/{nc_pattern}/OUT_STAT/*{nc_pattern}_*.nc")
    if not matching_files:
        print(f"Error: No NetCDF file found matching pattern '{nc_pattern}'.")
        sys.exit(1)
    return matching_files[0]

def plot_variable(nc_pattern, var_name, var_desc, data, dataset):
    """Plot the given variable from the dataset."""
    time = dataset.variables["time"][:]
    z = dataset.variables["z"][:] if "z" in dataset.variables else None
    
    fig, ax = plt.subplots(figsize=(8, 6))
    
    if len(data.shape) == 1:  # 1D variable (time)
        if data.shape[0] == time.shape[0]:
            ax.plot(time, data, label=var_name)
            ax.set_xlabel("Time (days since start)")
        else:
            print(f"Skipping {var_name}: Dimension mismatch with time.")
            return
    elif len(data.shape) == 2 and z is not None:  # 2D variable (time, z)
        time_avg_period = 30  # Last 30 days
        if data.shape[0] == time.shape[0]:
            if len(time) > time_avg_period:
                data = np.mean(data[-time_avg_period:], axis=0)
            ax.plot(data, z, label=var_name)
            ax.set_xlabel(var_name)
            ax.set_ylabel("Height (z)")
        else:
            print(f"Skipping {var_name}: Time dimension mismatch.")
            return
    elif len(data.shape) == 3:  # Assume (time, lat, lon)
        data = np.mean(data, axis=0)  # Take time average
        im = ax.imshow(data, cmap='viridis', origin='lower')
        fig.colorbar(im, ax=ax, label=var_name)
    else:
        print(f"Skipping {var_name}: Unsupported variable shape {data.shape}.")
        return
    
    ax.set_title(f"{var_name} ({var_desc}) from {nc_pattern}")
    ax.legend()
    
    # Create directory if it does not exist
    output_dir = os.path.join(os.getcwd(), nc_pattern)
    os.makedirs(output_dir, exist_ok=True)
    
    plot_filename = os.path.join(output_dir, f"{var_name}.png")
    plt.savefig(plot_filename, dpi=300, bbox_inches='tight')
    print(f"Plot saved as {plot_filename}")
    plt.show()


def process_netcdf(nc_pattern, var_key=None):
    """Process and plot variables from the NetCDF file."""
    nc_file = find_nc_file(nc_pattern)
    dataset = nc.Dataset(nc_file, "r")
    
    if var_key:
        if var_key in VARIABLE_MAP:
            for var_name, var_desc in VARIABLE_MAP[var_key]["variables"].items():
                if var_name in dataset.variables:
                    data = dataset.variables[var_name][:]
                    plot_variable(nc_pattern, var_name, var_desc, data, dataset)
    else:
        # Iterate through all known variables in VARIABLE_MAP
        for category in VARIABLE_MAP.values():
            for var_name, var_desc in category["variables"].items():
                if var_name in dataset.variables:
                    data = dataset.variables[var_name][:]
                    plot_variable(nc_pattern, var_name, var_desc, data, dataset)
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plot NetCDF data.")
    parser.add_argument("nc_file", type=str, help="Pattern to search for NetCDF file.")
    parser.add_argument("variable_key", type=str, nargs='?', help="Variable key (e.g., 2Dthermo, 1Dthermo, 1Dcloud). If not provided, all known variables will be plotted.")
    
    args = parser.parse_args()
    process_netcdf(args.nc_file, args.variable_key)
