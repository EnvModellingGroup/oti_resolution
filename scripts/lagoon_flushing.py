import xarray as xr
import numpy as np
import os
import geopandas as gpd
from datetime import timedelta
import re
import csv
import glob

outputdt = timedelta(seconds=240)
lagoon = gpd.read_file("/data/jh1889/oti_hires/data/release_poly.shp")
model_dir = "/data/jh1889/oti_hires/sims/coarse"
# fetch all the zarr outputs
#inputs = glob.glob(model_dir+"/*.zarr/")
inputs = [os.path.join(model_dir,"Trajectory_314880.zarr"),
          os.path.join(model_dir,"Trajectory_336480.zarr"),
          os.path.join(model_dir,"Trajectory_325680.zarr"),
          #os.path.join(model_dir,"Trajectory_358080.zarr"),
          #os.path.join(model_dir,"Trajectory_379680.zarr"),
          #os.path.join(model_dir,"Trajectory_401280.zarr"),
          ]

names = []
for i in inputs:
    names.append(re.findall(r'_(\d+)', i)[0])

# for each zarr
for name, file in zip(names, inputs):
    # load the zar
    ds = xr.open_zarr(file)
    print("Dealing with starttime: "+name)
    # each zarr will have a diferent time interval as we kicked them off at different times
    # timerange in nanoseconds
    timerange = np.arange(
        np.nanmin(ds["time"].values),
        np.nanmax(ds["time"].values) + np.timedelta64(outputdt),
        outputdt,
    )
    n_particles = [] # we'll use index to simply count from 0
    for time in timerange:
        print("\t Time: "+str(time))
        time_id = np.where(ds["time"] == time)
        particles = gpd.GeoDataFrame(geometry=gpd.points_from_xy(ds["lon"].values[time_id], ds["lat"].values[time_id]), crs="EPSG:32756")
        within_points = gpd.sjoin(particles, lagoon, predicate="within")
        n_particles.append(len(within_points))

    with open(os.path.join(model_dir, "particles_"+name+".csv"), "w") as f:
        csv_write = csv.writer(f)
        csv_write.writerow(["Time", "Particles"])
        index = 0
        for particle in n_particles:
            csv_write.writerow([index, particle])
            index = index + 1


