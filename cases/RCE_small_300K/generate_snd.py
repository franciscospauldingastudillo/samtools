import sys
import numpy as np
def make_snd(Ts):
    ################################
    # create a file to initialize the atmosphere (surf->toa)
    data   = []
    header = ' z[m] p[mb] tp[K] q[g/kg] u[m/s] v[m/s]'
    day0    = 0.     # first day of sounding
    day1    = 1.
    nlev    = 72.    # number of vertical levels
    ps      = 1015.  # mb=hPa
    ################################
    # thermodynamic constants
    g     = 9.81  # m/s2
    Rd    = 287.  # J/kg/K
    cp    = 1004. # J/kg/K
    ################################
    # define the vertical levels
    h = ([37, 112, 194, 288, 395, 520, 667, 843, 1062, 1331,
    1664, 2055, 2505, 3000, 3500, 4000, 4500, 5000, 5500, 6000,
    6500, 7000, 7500, 8000, 8500, 9000, 9500, 10000, 10500, 11000,
    11500, 12000, 12500, 13000, 13500, 14000, 14500, 15000, 15500, 16000,
    16500, 17000, 17500, 18000, 18500, 19000, 19500, 20000, 20500, 21000,
    21500, 22000, 22500, 23000, 23500, 24000, 24500, 25000, 25500, 26000,
    26500, 27000, 27500, 28000, 28500, 29000, 29500, 30000, 30500, 31000,
    31500, 32000])
    h = np.round(np.array(h),decimals=0)
    ################################
    # analytical specific humidity (Wing et al. 2018)
    q0 = 0.018   # kg/kg (surface specific humidity)
    zq1= 4000.   # m
    zq2= 7500.   # m
    qt = 1.0e-14 # kg/kg (stratospheric specific humidity)   
    zt = 15000.  # m (fiducial tropopause height)
    q  = q0*np.exp(-h/zq1)*np.exp(-(h/zq2)**2)
    q  = np.where(h>zt,qt,q)
    # analytical mixing ratio (g/kg; SAM requirement)
    w  = np.divide(q,1-q)
    w  = 1e3*w # kg/kg->g/kg
    ################################
    # analytic virtual temperature (Wing et al. 2018)
    T0    = Ts # T(surface)
    Tv0   = T0*(1+0.608*q0) # Tv(surface)
    Gamma = 0.0067 # K/m (virtual tempearture lapse rate)
    Tvt   = Tv0-Gamma*zt # (stratospheric virtual temperature)
    Tv    = Tv0-Gamma*h
    Tv    = np.where(Tv<Tvt,Tvt,Tv)
    ################################
    # analytic temperature
    T     = np.divide(Tv,1+0.608*q)
    ################################
    # analytic pressure (Wing et al. 2018)
    p0    = ps
    pt    = p0*(Tvt/Tv0)**(g/(Rd*Gamma))
    p     = p0*((Tv0-Gamma*h)/Tv0)**(g/(Rd*Gamma))
    p     = np.where(h>zt,pt*np.exp(-(g*(h-zt))/(Rd*Tvt)),p)
    ################################
    # analytic potential temperature
    Th = T*(ps/p)**(Rd/cp)
    ################################
    # horizontal velocities (no wind)
    u    = np.zeros([len(h)])
    v    = np.zeros([len(h)])
    ################################
    # clean-up the values
    h = np.round(h,decimals=4)
    p = np.round(p,decimals=4)
    T = np.round(T,decimals=4)
    Th= np.round(Th,decimals=4)
    w = np.round(w,decimals=4)
    u = np.round(u,decimals=4)
    v = np.round(v,decimals=4)
    ################################
    data.append(header)
    ################################
    print(type(day0))
    print(type(nlev))
    print(type(ps))
    data.append(['%f,'%day0, '%f,'%nlev, '%f,'%ps])
    for c1,c2,c3,c4,c5,c6 in zip(h,p,Th,w,u,v):
        data.append([c1,c2,c3,c4,c5,c6])
    data.append(['%f,'%day1, '%f,'%nlev,'%f,'%ps])
    for c1,c2,c3,c4,c5,c6 in zip(h,p,Th,w,u,v):
        data.append([c1,c2,c3,c4,c5,c6])
    ################################
    # File path to save the text file
    fname = "./snd"
    # write data to a file
    with open(fname, 'w') as file:
        for i, row in enumerate(data):
            if i==0 or i == int(len(data)/2):
                # For the first two rows and the final row, write the row with single space
                file.write(' '.join(map(str, row)) + '\n')
            else:
                # For other rows, write the row with tab-separated values
                file.write('      '.join(map(str, row)) + '\n')
    #fig,ax = plt.subplots()
    #ax.plot(Th,h)

# generate the sounding
Ts = float(sys.argv[1])
make_snd(Ts)
print('done.\n')

