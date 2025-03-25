import uptide
import uptide.tidal_netcdf
import datetime
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
import params

# WHich constiuents do you want?
constituents = ['M2', 'S2', 'N2', 'K2', 'K1', 'O1', 'P1', 'Q1', 'M4', 'MS4', 'MN4' ]
tide = uptide.Tides(constituents)
# set your start date and time
tide.set_initial_time(params.start_datetime) #year, month, day, hour, min, sec

# point me at your TPXO files (grid and h_ data)
grid_file_name = "../../data/grid_tpxo9.nc"
data_file_name = "../../data/h_tpxo9.v1.nc"
tnci = uptide.tidal_netcdf.OTPSncTidalInterpolator(tide, grid_file_name, data_file_name)

#linear increase
tt = 86400 # 24 hours

#No need to edit below here

def set_tidal_field(elev, t, llvector):
    tnci.set_time(t)
    evector = elev.dat.data
    # create a linear ramping over the first hour
    for i,xy in enumerate(llvector):
        lon = xy[1]
        lat = xy[0]
        if xy[1] < 0:
            lon = xy[1] + 360.0

        multiplier = t / tt
        if t >= tt:
            multiplier = 1.0
        try:
            evector[i] = multiplier * tnci.get_val((lon, lat))
        except uptide.netcdf_reader.CoordinateError:
            evector[i] = 0.

    return evector

