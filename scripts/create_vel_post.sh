#!/bin/bash

# read the time file in
# Making a *BIG* assumption this matches only one file!
readarray -t time_list < *_times_thetis.txt

# pull directory as argument
directory=$1

for xyz in ${directory}/*_u_*.xyz;
do
    echo ${xyz}
    # swap out Nones to -9999
    sed -i 's/None/-9999/g' ${xyz}
    gdal_translate -a_nodata -9999 -of netCDF ${xyz} ${xyz}.nc > /dev/null
done

for xyz in ${directory}/*_v_*.xyz;
do
    echo ${xyz}
    sed -i 's/None/-9999/g' ${xyz}
    gdal_translate -a_nodata -9999 -of netCDF ${xyz} ${xyz}.nc > /dev/null
done


# we can now merge all the .nc files created with create_vel_par.sh
# we can * as we've made the number 0ddd so they should list in order
ncecat ${directory}/*_u_*.nc -O "${directory}/Velocity2d_U.nc"
ncecat ${directory}/*_v_*.nc -O "${directory}/Velocity2d_V.nc"

# then rename the record dimension as time
ncrename -d record,time ${directory}/Velocity2d_U.nc
ncrename -d record,time ${directory}/Velocity2d_V.nc


# adjust units of time to something sensible
printf -v joined '%s,' "${time_list[@]}"
string="time[time]={${joined%,}};time@long_name=\"Time\";time@units=\"seconds\""
ncap2 -s "${string}" ${directory}/Velocity2d_U.nc -O ${directory}/Velocity2d_U.nc
ncap2 -s "${string}" ${directory}/Velocity2d_V.nc -O ${directory}/Velocity2d_V.nc
# we then have to alter the time to be a float
ncap2 -s 'time=float(time)' --overwrite ${directory}/Velocity2d_U.nc ${directory}/Velocity2d_U.nc
ncap2 -s 'time=float(time)' --overwrite ${directory}/Velocity2d_V.nc ${directory}/Velocity2d_V.nc

# and finally set a sensible null value
fill_value=-999
