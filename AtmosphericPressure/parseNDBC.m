function [ time, slp ] = parseNDBC( filename )
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here

% Format example: 2005 01 01 00 30 111  8.8 10.7 99.00 99.00 99.00 999 1000.2   7.2   9.2   3.8 99.0 99.00
% Formatter
fmt = '%d %d %d %d %d %f %f %f %f %f %f %f %f %f %f %f %f %f';
%buoy_fmt = '%d %d %d %d %d %f  %f %f %f %f %f %f %f   %f   %f   %f %f %f';

% Read in file  -------------------------------------
fid = fopen(filename);
data = textscan(fid,fmt,'headerlines',2);
fclose(fid);

% Parse
yr = double(data{1});
mo = double(data{2});
da = double(data{3});
hr = double(data{4});
mn = double(data{5});
windDir = data{6};
windSpeed = data{7};
windGust = data{8};
waveHeight = data{9};
wavePeakPeriod = data{10};
waveAvgPeriod = data{11};
waveDir = data{12};
atmPres = data{13};
atmTemp = data{14};
waterTemp = data{15};
dewPoint = data{16};

% Create matlab time variable
time = datenum(yr,mo,da,hr,mn,0);
slp = atmPres;
end

