import matplotlib as mpl
import numpy as np
import matplotlib.pyplot as plt
#mpl.use('TkAgg')
import xarray as xr
import time

fig, axes = plt.subplots(nrows=4,sharex=True)

#%% Bulk params
# Plotting
bb = 7
for ii in range(4):
    axes[ii].clear()

ds = xr.open_dataset('W{:d}s-a.nc'.format(bb))
ds['gam'] = ds.wh_4061/ds.water_depth
ds['lp'] = np.log10(ds.pspec)

ds.wh_4061.plot(ax=axes[0])
ds.wp_4060.plot(ax=axes[1])
ds.water_depth.plot(ax=axes[2])
ds.gam.plot(ax=axes[3])
plt.show()
plt.savefig('bulk_data_{:d}.png'.format(bb),dpi=150,format='png',)

#%% Mean depth
for bb in [1,2,3,4,5,7,8]:
    ds = xr.open_dataset('W{:d}s-a.nc'.format(bb))
    print(np.nanmean(ds.water_depth))



#%% Time series
fig, axes = plt.subplots(nrows=2,sharex=True)

#%%
bb = 1
ncfile = 'W{:d}b-cal.nc'.format(bb)
ds = xr.open_dataset(ncfile)

for ii in range(2):
    axes[ii].clear()

test = np.mean(ds.P_1ac,axis=1)
test.plot(ax=axes[0])
test = np.mean(ds.T_28,axis=1)
test.plot(ax=axes[1])
plt.savefig('time_series_{:d}.png'.format(bb),dpi=150,format='png',)


#%% Number of samples in each half hour

for bb in [1,2,3,4,5,7,8]:
    ncfile = 'W{:d}b-cal.nc'.format(bb)
    ds = xr.open_dataset(ncfile)
    print(ds.sample.shape)
# plt.clf()
# ds.lp.T.plot()
# plt.show()

