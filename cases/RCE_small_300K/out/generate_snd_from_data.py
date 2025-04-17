# The objective of this script is to use the stats.nc file from RCE_small to produce a spin-up sounding for larger sims.
import netCDF4 as nc
import numpy as np
import sys
import os
import glob

# z(m; z), p(mb; PRES), Tp(K; THETA), w(g/kg; QV), u(m/s; U), v(m/s; V), time (days; time)
def get_snd(h,p,Th,w,u,v):
    ################################
    data   = []
    header = f' z[m] p[mb] tp[K] q[g/kg] u[m/s] v[m/s] from {case}'
    day0    = 0.     # first day of sounding
    day1    = 1.     # second day of sounding
    nlev    = 72     # number of vertical levels
    ps      = 1015.  # mb=hPa 
    ################################
    data.append(header)
    ################################
    data.append(['%f,'%day0, '%f,'%nlev, '%f,'%ps])
    for c1,c2,c3,c4,c5,c6 in zip(h,p,Th,w,u,v):
        data.append([c1,c2,c3,c4,c5,c6])
    data.append(['%f,'%day1, '%f,'%nlev,'%f,'%ps])
    for c1,c2,c3,c4,c5,c6 in zip(h,p,Th,w,u,v):
        data.append([c1,c2,c3,c4,c5,c6])
    ################################
    # File path to save the text file
    fname = f"{cdir}/snd"
    # write data to a file
    with open(fname, 'w') as file:
        for i, row in enumerate(data):
            if i==0 or i == int(len(data)/2):
                # For the first two rows and the final row, write the row with single space
                file.write(' '.join(map(str, row)) + '\n')
            else:
                # For other rows, write the row with tab-separated values
                file.write('      '.join(map(str, row)) + '\n')
    ################################
    print('done.')

# Get the path to THIS file
cdir = os.path.dirname(os.path.abspath(__file__))

# Check if the correct number of arguments is provided
if len(sys.argv) != 2:
    print("Usage: python3 generate_snd_from_data.py <surface_temp>")
    sys.exit(1)

# Read the surface temperature from command line
Ts = float(sys.argv[1])

# Locate the directory where the data is stored
case = f'RCE_small_{Ts}K'
ddir = f'/u/home/f/fspauldi/SAM6.11.8/{case}/out'

# Find all .nc files containing "RCE_small" in the filename in RCE_small directory
nc_files = glob.glob(f"{ddir}/*RCE_small*.nc")
if len(nc_files) == 1:
    # Load the single matching .nc file
    fname = nc_files[0]
    print(f"Successfully found {case} .nc file: {nc_file}")
elif len(pickle_files) == 0:
    sys.exit("Error: No {case} .nc files found in the current directory.")
else:
    sys.exit(f"Error: Multiple {case} .nc files found: {nc_files}")

# Open the NetCDF file with dimensions (time,z)
dat = nc.Dataset(fname, 'r')
# Extract the 'time' variable
time = dat.variables['time'][:]
# Find indices where time is greater than 70 days
time_indices = np.where(time > 70)[0]
# Extract the variables for days > 70
PRES  = np.mean(dat.variables['PRES'][time_indices, :],axis=0)  # pressure (mb)
WV    = np.mean(dat.variables['QV'][time_indices, :],axis=0)    # water vapor mixing ratio (g/kg)
U     = np.mean(dat.variables['U'][time_indices, :],axis=0)     # u-velocity (m/s)
V     = np.mean(dat.variables['V'][time_indices, :],axis=0)     # v-velocity (m/s)
THETA = np.mean(dat.variables['THETA'][time_indices, :],axis=0) # potential temperature (K)
Z     = dat.variables['z'][:]                                   # height (m)
# Close the NetCDF file
dat.close()

#################################################
# Generate the sounding from data
get_snd(Z,PRES,THETA,WV,U,V)

