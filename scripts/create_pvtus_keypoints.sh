#!/bin/bash

# run in a firedrake venv
# more cores == faster processing (to limit of your machine and mesh)
# wraps the h5_2_pvtu.py script to sort elevation and velocity VTUs 
# for paraview visualisation from thetis h5 files.

directory="../sims/modern/output/hdf5/"
ncore=2
file_numbers=("350" "433" "474" "1196" "1214" "1267")

function process_file {

    file=${1}
    output_file="${directory}/../${2}"
    # loop over variables with counter
    # create the raster ov the vtu
    python h5_2_pvtu.py ${file} ${output_file}

}

for f in ${file_numbers[@]}
do
    file="${directory}/Velocity2d_"$( printf "%05d" "$f" )".h5"
    echo ${file}
    process_file ${file} "Velocity2d"
done

for f in ${file_numbers[@]}
do
    file="${directory}/Elevation2d_"$( printf "%05d" "$f" )".h5"
    echo ${file}
    process_file ${file} "Elevation2d"
done


