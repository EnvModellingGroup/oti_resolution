import datetime
from utm import *
import pytz

# path relative to the root dir of this template. Leave as mesh/blah.msh in most cases
mesh_file = 'mesh/oti_only.msh'
forcing_boundary = 666
utm_zone = 56
utm_band="K"
cent_lat = -23.496
cent_lon = 152.077
spin_up = 172800 # 2 days
end_time = 2764800 # 32 days
output_dir = "output"
output_time = 900
constituents = ['M2', 'S2', 'N2', 'K2', 'K1', 'O1', 'P1', 'Q1', 'M4']
# year, month, day, hour, min, sec
#start_datetime = datetime.datetime(2022,11,22,0,0,0) 
start_datetime = datetime.datetime(2005,11,11,0,0,0)
time_diff = pytz.timezone('Australia/Brisbane')
