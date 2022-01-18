# This is a sample Python script.
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# Outliers are in cdf, do some QC
# CF compliance will pass with singleton dimensions and without.
# Maintain compliance?

# Make the atm cdf file from a csv file of date and pressure
def makeatmcdf(atmcsv, cdfraw, atmcdf, offset):

    def read_met_data(filename):
        a = pd.read_csv(filename, header=0, parse_dates=[0],
                        infer_datetime_format=True, index_col=0)
        return xr.Dataset(a)

    gndcrmet = read_met_data(atmcsv)  # This creates an xarray Dataset
    gndcrmet = gndcrmet['pres'].to_dataset()  # Let's keep only the BP variable
    gndcrmet['pres'] = gndcrmet['pres'] / 100  # convert our atmos data (in millibars) to decibars

    # Load the raw Aquadopp data
    RAW = xr.open_dataset(cdfraw, autoclose=True)

    met = gndcrmet['pres']  # make a new met variable
    met = met.rename('atmpres')  # rename it to the standard atmpres variable name
    met = met.reindex(time=RAW['time'], copy=True, method='nearest')  # reindex the met data onto the Aquadopp time base
    met.attrs.update(offset=offset)  # -10.15) # set the atmospheric offset as an attribute
    met.to_netcdf(atmcdf)  # save to disk

#if __name__ == '__main__':

import yaml
import xarray as xr
import pandas as pd
import stglib
for bb in [8]:#[1,2,3,4,5,7]:  # range(5):#range(1):
    gatts = 'W{:d}_global_attributes'.format(bb)
    config = 'W{:d}_rbrwave'.format(bb)
    atmcdf = '../AtmosphericPressure/W{:d}_atmpres.cdf'.format(bb)
    atmcsv = '../AtmosphericPressure/atmpressure.csv'
    cdfraw = 'W{:d}-raw.cdf'.format(bb)
    ncname = 'W{:d}b-cal.nc'.format(bb)
    offset = 0;

    # ------ Step 1 read the metadata files and combine
    metadata = stglib.read_globalatts(gatts)
    with open(config) as f:
        config = yaml.safe_load(f)
    for k in config:
        metadata[k] = config[k]

    # ------ Step 2 make the atm cdf file from metadata
    stglib.rsk.rsk2cdf.rsk_to_cdf(metadata)

    # ------ Step 3 make the atmospheric pressure file
    makeatmcdf(atmcsv, cdfraw, atmcdf, offset)

    # ------ Step 4 make nc file of continuous data
    ds = stglib.rsk.cdf2nc.cdf_to_nc(cdfraw, atmcdf)

    # ------- Step 5 calculate the wave data
    ds = stglib.rsk.nc2waves.nc_to_waves(ncname)









