#!/usr/bin/env python
from helper_functions import *
import numpy as np
import matplotlib.pyplot as plt
import datetime
import csv
import pandas as pd
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, "sims")))
import params
import argparse
import pytz


def main():

    parser = argparse.ArgumentParser(
         prog="plot gauge anim",
         description="""Plot the tidal elevation with time, using dot to show current position"""
    )
    parser.add_argument(
        '-v', 
        '--verbose', 
        action='store_true', 
        help="Verbose output: mainly progress reports.",
        default=False
    )
    parser.add_argument(
        '-m', 
        '--model', 
        help="the elevation csv file (file only) from the extract_gague.py script. Defaults to model_gauges_elev.csv in the model dir",
        default="model_gauges_elev.csv"
    )
    parser.add_argument(
        '-t',
        '--tide',
        help="The tide gauge name as shown in header",
        default="ONE TREE I."
    )
    parser.add_argument(
        '-s',
        '--stub',
        help='short string to append onto output filenames, before the extension, e.g. using "7" would make the output "thetis_vs_obs_7.pdf"',
        default=""
    )
    parser.add_argument(
        'model_dir',
        help='The model run directory, e.g. ../sims/base_case/'
    )
    parser.add_argument(
        'output_dir',
        help='Where to put output'
    )


    args = parser.parse_args()
    verbose = args.verbose    
    model_input = args.model
    tide_gauge = args.tide
    stub = args.stub
    model_dir = args.model_dir
    model_input = os.path.join(model_dir, model_input)
    output_dir = args.output_dir

    # release times
    spring_release_times = np.arange(314880, 476881, 10800)
    neap_release_times = np.arange(1076400, 1238401, 10800)

    plt.rcParams.update({'font.size': 22})
    plt_params = {
      'legend.fontsize': 12,
      'xtick.labelsize': 12,
      'ytick.labelsize': 12,
      'axes.labelsize' : 14,
      #'figure.subplot.left' : 0.18,
      #'figure.subplot.top': 0.82,
      #'figure.subplot.right': 0.95,
      #'figure.subplot.bottom': 0.15,
      'text.usetex' : True
        }
    plt.rcParams.update(plt_params)
    
    df = pd.read_csv(model_input)
    model_times = df["Time"].to_numpy()
    
    # extract accounts for the spin-up time, so we can start from zero
    t_start = model_times[0]
    t_export = model_times[1] - model_times[0]
    t_end = model_times[-1]

    gauge_data = df[tide_gauge]
    # create heights for release points
    spring_release_heights = np.interp(spring_release_times, model_times, gauge_data)
    neap_release_heights = np.interp(neap_release_times, model_times, gauge_data)

    fig=plt.figure(figsize=(5.0,3.0),dpi=360)
    ax=fig.add_subplot(111)

    # Prettier and fixes LaTeX issue (not really needed, but left in case)
    nice_name = tex_escape(tide_gauge.replace("_"," ").title())
    ax.plot(model_times/86400.,gauge_data.to_numpy(), color="dodgerblue", lw=0.5, label="Model")
    # now plot the circle
    ax.scatter(spring_release_times/86400, spring_release_heights, color="darkorange", s=1, zorder=10)
    ax.scatter(neap_release_times/86400, neap_release_heights, color="deeppink", s=1, zorder=10)


    ax.set_xlabel("Time (days)")
    ax.set_ylabel("Water height (m)")
    fig.tight_layout()
    if not stub == "":
        stub = "_" + stub
    nice_name = nice_name.replace(" ","_")
    output_filename = "Release_times.png"
    plt.savefig(os.path.join(output_dir,output_filename), dpi=360)
    plt.close()

if __name__ == "__main__":
    main()

