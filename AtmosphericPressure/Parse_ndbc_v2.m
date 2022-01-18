clearvars
% Script reads in NDBC formatted wave/met buoy historical file, parses and
% plots conditions
%
% For data description: https://www.ndbc.noaa.gov/measdes.shtml
% To download and example: https://www.ndbc.noaa.gov/view_text_file.php?filename=46087h2005.txt.gz&dir=data/historical/stdmet/
%
% S. C. Crosby 2018


% 2018
fname = 'NDBC_frdw_2018.txt';
[ time1, slp1 ] = parseNDBC( fname );

% 2019
fname = 'NDBC_frdw_2019.txt';
[ time2, slp2 ] = parseNDBC( fname );

% 2020
fname = 'NDBC_frdw_2020_Jan.txt';
[ time3, slp3 ] = parseNDBC( fname );

% 2020
fname = 'NDBC_frdw_2020_Feb.txt';
[ time4, slp4 ] = parseNDBC( fname );

% 2020
fname = 'NDBC_frdw_2020_Mar.txt';
[ time5, slp5 ] = parseNDBC( fname );

% 2020
fname = 'NDBC_frdw_2020_Apr.txt';
[ time6, slp6 ] = parseNDBC( fname );

% Fake the rest
% time9 = (datenum(2020,2,1):datenum(2020,4,1))';
% slp9 = 1017*ones(size(time9));


% Concat
%slp = [slp1; slp2; slp3; slp4; slp5; slp6; slp7; slp8; slp9];
%time = [time1; time2; time3; time4; time5; time6; time7; time8; time9];
slp = [slp1; slp2; slp3; slp4; slp5; slp6];
time = [time1; time2; time3; time4; time5; time6];


% Clean
inds = slp < 100;
slp(inds) = NaN;
inds = slp > 2000;
slp(inds) = NaN;

% Interp
sum(isnan(slp))
[ slpI ] = interpShortNaN( time', slp', 24*7 );
sum(isnan(slpI))

% Unique
[~, I] = unique(time);
time = time(I);
slp = slp(I);

% Interp onto coarser series (hourly)
time_out = time(1):(1/24):time(end);
slp_out = interp1(time,slpI,time_out);

clf
hold on
plot(time, slp)
plot(time_out, slp_out)
datetick

disp(sum(isnan(slp_out)))


% Save file in csv format for python
fid = fopen('atmpressure.csv','w');
fprintf(fid,'time,pres\n');
for ii = 1:length(time_out)
    fprintf(fid,'%s,%6.2f\n',datestr(time_out(ii),'mm/dd/yyyy HH:SS'),slp_out(ii));
end
fclose(fid);
