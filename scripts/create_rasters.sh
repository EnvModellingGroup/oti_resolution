#!/bin/bash
directory="../sims/modern/output/hdf5/"
ncore=1

resolution=50
projection=EPSG:32756
maskfile="../mesh/oti_smaller_extended_hires_mask.shp"
minmax="398050 412188 7396079 7405296"

function process_file {

    processing_file=${1}

    # loop over variables
    var=${varname[$i]}
    name=${names[$i]}
    file=${processing_file}
    # loop over variables with counter
    # create the raster ov the vtu
    mpiexec -n ${ncore} python h5_2_raster.py --resolution ${resolution} --velocity --min_max ${minmax} ${file} temp 
    #mask it
    gdalwarp -cutline ${maskfile} -s_srs ${projection} -crop_to_cutline -of GTIFF -r bilinear  -dstnodata -9999 -overwrite temp_u*.xyz "${file}_u.tif"
    gdalwarp -cutline ${maskfile} -s_srs ${projection} -crop_to_cutline -of GTIFF -r bilinear  -dstnodata -9999 -overwrite temp_v*.xyz "${file}_v.tif"
    rm temp*.xyz

}

FILES="${directory}/Velocity2d_00120.h5"
for f in $FILES
do
    process_file ${f}
done

