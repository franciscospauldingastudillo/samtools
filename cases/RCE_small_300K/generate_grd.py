import numpy as np

h = ([37, 112, 194, 288, 395, 520, 667, 843, 1062, 1331,
    1664, 2055, 2505, 3000, 3500, 4000, 4500, 5000, 5500, 6000,
    6500, 7000, 7500, 8000, 8500, 9000, 9500, 10000, 10500, 11000,
    11500, 12000, 12500, 13000, 13500, 14000, 14500, 15000, 15500, 16000,
    16500, 17000, 17500, 18000, 18500, 19000, 19500, 20000, 20500, 21000,
    21500, 22000, 22500, 23000, 23500, 24000, 24500, 25000, 25500, 26000,
    26500, 27000, 27500, 28000, 28500, 29000, 29500, 30000, 30500, 31000,
    31500, 32000])
h = np.round(np.array(h),decimals=0)

# grd format (height, index, dz)
c1 = h
c2 = np.arange(1,len(h)+1)
c3 = h[1:]-h[0:-1]
c3 = np.append(c3,c3[-1])

# initialize an empty list to store data
data = []

# loop through each value of x, y, and z
for x,y,z in zip(c1,c2,c3):
    data.append([x,y,z])

# file path to save the text file
fname = './grd'

# writing data to the file
with open(fname,'w') as file:
    for row in data:
        file.write(' '.join(map(str,row))+'\n')

print('done.\n')

