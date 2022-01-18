import numpy as np
import pandas as pd
import scipy.signal
import xarray as xr
import datetime

# CF Checker, https://compliance.ioos.us/index.html
# sea_surface_wave_significant_height - https://cfconventions.org/Data/cf-standard-names/77/build/cf-standard-name-table.html
# wh_4061 - https://pubs.usgs.gov/of/2005/1211/images/pdf/report.pdf

# .to_xarray to go from pd to xrray()
# Babak is 3-month out of data

# Parameters
data_fol = '../spotter02_recover202108'
spec_files = ['Szz.csv', 'Sxx.csv', 'Syy.csv', 'a1.csv', 'b1.csv', 'a2.csv', 'b2.csv']
bulk_file = 'bulkparameters.csv'
LF_limit = 0.1 # Low frequency limit [Hz]
HF_limit = 1 # High frequency limit [Hz]
k_min = 0.7 # Valid range for check ratio
k_max = 2.0
k_per_error = 0.25 # Portion of frequencies with out of range check ratio permitted

# read spectra parameters, e.g E(f)
# Outputs time, frequency, and spectra as datetime and numpy arrays
def read_spec(fname, LF_limit, HF_limit):
    df = pd.read_csv(fname, header=0, na_values=[' nan ','nan ',' nan'], dtype=np.float64)
    df.columns = df.columns.str.replace(' ', '')
    df = df.rename(columns={'#year':'year'})
    time = pd.to_datetime(dict(year=df.year, month=df.month, day=df.day, hour=df.hour, minute=df['min'], second=df.sec))
    frequency = df.keys()[8:].astype(float)
    spec = df.iloc[:,8:].to_numpy()
    i_fr = (frequency >= LF_limit) & (frequency <= HF_limit)
    spec = spec[:, i_fr]
    frequency = frequency[i_fr]
    return (time, frequency, spec)

# Read bulk wave parameters, outputs pandas dataframe with datetime index
def read_bulk(fname):
    df = pd.read_csv(fname, header=0, na_values=[' nan ','nan ',' nan'], dtype=np.float64)
    df.columns = df.columns.str.replace(' ', '')
    df = df.rename(columns={'#year': 'year'})
    time = pd.to_datetime(dict(year=df.year, month=df.month, day=df.day, hour=df.hour, minute=df['min'], second=df.sec))
    df.index = time
    df = df.iloc[:,7:]
    return df

# Read in bulk
fname = data_fol + '/' + bulk_file
bulk = read_bulk(fname)

# Read in spectra
time, frequency, szz = read_spec(data_fol + '/' + spec_files[0], LF_limit, HF_limit)
_, _, sxx = read_spec(data_fol + '/' + spec_files[1], LF_limit, HF_limit)
_, _, syy = read_spec(data_fol + '/' + spec_files[2], LF_limit, HF_limit)
_, _, a1 = read_spec(data_fol + '/' + spec_files[3], LF_limit, HF_limit)
_, _, b1 = read_spec(data_fol + '/' + spec_files[4], LF_limit, HF_limit)
_, _, a1 = read_spec(data_fol + '/' + spec_files[5], LF_limit, HF_limit)
_, _, b2 = read_spec(data_fol + '/' + spec_files[6], LF_limit, HF_limit)

# Calculate Check Ratio
K = np.sqrt((sxx + syy)/szz)

# How many frequency bins
Nf = len(frequency)

# Find out of range K (Normal range for check ratio  0.7 to 2.0)
# Note that from CDIP Processing: If more than one-quarter of the bands have check factors values of two or more, a warning is issued and logged.
K_out_of_range = (K < k_min) | (K > k_max)
K_count = np.sum(K_out_of_range, axis=1)
K_bad = K_count > (Nf * k_per_error)

print('Check ratio error for {:d} of {:d} time steps found'.format(np.sum(K_bad), len(K_count)))

# To do: compute wave bulk parameters from restricted spectra. ugh



