import uptide
import uptide.tidal_netcdf
import datetime

# WHich constiuents do you want?
constituents = ['M2', 'S2', 'N2', 'K2', 'K1', 'O1', 'P1', 'Q1' ]
tide = uptide.Tides(constituents)
# set your start date and time
tide.set_initial_time(datetime.datetime(2005,11,11,0,0,0)) #year, month, day, hour, min, sec

# point me at your FES file
grid_file_name = "../grid_tpxo9.nc"
tnci = uptide.tidal_netcdf.AMCGTidalInterpolator(tide,  grid_file_name)
#tnci.set_mask_from_fill_value('m2amp', 1.844674e+19)

# no need to edit beflow here

def set_tidal_field(elev, t, llvector):
    tnci.set_time(t)
    evector = elev.dat.data
    for i,xy in enumerate(llvector):
        lon = xy[1]
        lat = xy[0]
        try:
            evector[i] = tnci.get_val((lat, lon)) / 100.
        except uptide.netcdf_reader.CoordinateError:
            evector[i] = 0.

