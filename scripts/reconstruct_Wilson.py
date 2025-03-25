import uptide
import datetime
from helper_functions import *
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates

start_datetime = datetime.datetime(1983,8,20,0,0,0)
tide = uptide.Tides(['M2', 'S2', 'K1', 'O1', 'Q1', 'P1', 'N2', 'K2'])  # select which constituents to use
tide.set_initial_time(start_datetime)  # set t=0 at 1 Jan 2001, UTC 12:00
tide_gauge_data = read_tide_gauge_data("../data/tide_gauge_2.csv")
oti = tide_gauge_data['ONE TREE I.']
amp = [
       oti['M2 amp'],
       oti['S2 amp'],
       oti['K1 amp'],
       oti['O1 amp'],
       oti['Q1 amp'],
       oti['P1 amp'],
       oti['N2 amp'],
       oti['K2 amp'],
       ]
pha = [
       oti['M2 phase'],
       oti['S2 phase'],
       oti['K1 phase'],
       oti['O1 phase'],
       oti['Q1 phase'],
       oti['P1 phase'],
       oti['N2 phase'],
       oti['K2 phase'],
       ]




t = np.arange(0, 10*24*3600.0, 100)
# create to datetime
datetimes = start_datetime + t* datetime.timedelta(seconds=1)
eta = tide.from_amplitude_phase(amp, pha, t)
fig, ax = plt.subplots()
ax.plot(datetimes, eta)
myFmt = DateFormatter("%H", usetex=True)
ax.xaxis.set_major_formatter(myFmt)
ax.xaxis.set_major_locator(mdates.HourLocator(interval=3))
ax.set_xlim([start_datetime, start_datetime+datetime.timedelta(days=10)])
## Rotate date labels automatically
fig.autofmt_xdate()
sec = ax.secondary_xaxis(location=-0.075)
sec.xaxis.set_major_locator(mdates.DayLocator(interval=1))
sec.xaxis.set_major_formatter(mdates.DateFormatter('%d'))
sec.tick_params('x', length=0)
sec.spines['bottom'].set_linewidth(0)
# label the xaxis, but note for this to look good, it needs to be on the
# secondary xaxis.
sec.set_xlabel('Dates (August 1983)')

plt.show()
# near the NEAP tide
