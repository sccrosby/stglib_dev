from __future__ import division, print_function
import xarray as xr
import pandas as pd

filename = 'atmpressure.csv'
cdfRawFile = '../StglibProcessing/B1-raw.cdf'
cdfRawFile = '../StglibProcessing/B2-raw.cdf'
cdfRawFile = '../StglibProcessing/B3-raw.cdf'
cdfRawFile = '../StglibProcessing/S1-raw.cdf'
cdfRawFile = '../StglibProcessing/S2-raw.cdf'


def read_met_data(filename):
    a = pd.read_csv(filename, header=0, parse_dates=[0],
                    infer_datetime_format=True, index_col=0)

    return xr.Dataset(a)

gndcrmet = read_met_data(filename) # This creates an xarray Dataset
gndcrmet = gndcrmet['pres'].to_dataset() # Let's keep only the BP variable
gndcrmet['pres'] = gndcrmet['pres']/100 # convert our atmos data (in millibars) to decibars
#gndcrmet.to_netcdf(ncfile1) # This saves to a .nc file. Not required here as we will just be reading it back again

# Load the raw Aquadopp data
RAW = xr.open_dataset(cdfRawFile, autoclose=True)

# Load the met data
# gndcrmet = xr.open_dataset(ncfile1, autoclose=True)

met = gndcrmet['pres'] # make a new met variable
met = met.rename('atmpres') # rename it to the standard atmpres variable name
met = met.reindex(time=RAW['time'], copy=True, method='nearest') # reindex the met data onto the Aquadopp time base
met.attrs.update(offset=-0.01) #-10.15) # set the atmospheric offset as an attribute
#met.attrs.update(offset=-10.15) # set the atmospheric offset as an attribute
met.to_netcdf('atmpres.cdf') # save to disk



#def load_clean(filename):
#    ds = xr.open_dataset(filename, decode_times=False, autoclose=True)
#    ds['time'] = ds['time_cf']
#    ds = ds.drop('time2')
#    
#    return xr.decode_cf(ds)
#
#VEL = load_clean('../StglibProcessing/051161s-a.nc')
#
##%%
#
#plt.figure(figsize=(10,8))
#RAW['P_1'].plot()
#VEL['P_1ac'].plot()
#plt.show()