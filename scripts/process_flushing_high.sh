#!/bin/bash

DIR=$1
echo "Running in $DIR"
N=4

for start_time in `seq 314880 10800 487680`; do
    sem -j $N run_parcels.sh ${start_time}
done
echo "all done spring tide"

#for start_time in `seq 1076400 10800 1238400`; do
#    (
#        echo ${start_time}
#        if [ ! -d $DIR/Trajectory_${start_time}.zarr ]; then
#            echo "    Will run"
#            python ocean_parcels.py ${DIR} ${start_time} -v
#        fi
#
#    ) &
#
#    # allow to execute up to $N jobs in parallel
#    if [[ $(jobs -r -p | wc -l) -ge $N ]]; then
#        wait -n
#    fi
#
#done
echo "all done neap tide"

