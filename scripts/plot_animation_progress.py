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
        help="the elevevation csv file (file only) from the extract_gague.py script. Defaults to model_gauges_elev.csv in the model dir",
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

    # now loop over times and plot them.
    for i in range(0,len(model_times)):

        # 500 x 250 pixels
        fig=plt.figure(figsize=(5.0,2.5),dpi=100)
        ax=fig.add_subplot(111)

        # Prettier and fixes LaTeX issue (not really needed, but left in case)
        nice_name = tex_escape(tide_gauge.replace("_"," ").title())
        ax.plot(model_times/86400.,gauge_data.to_numpy(), color="dodgerblue", lw=1, label="Model")
        # now plot the circle
        ax.plot(model_times[i]/86400, gauge_data[i], color="darkorange",marker="o")

        ax.set_xlabel("Time (days)")
        ax.set_ylabel("Water height (m)")
        fig.tight_layout()
        if not stub == "":
            stub = "_" + stub
        nice_name = nice_name.replace(" ","_")
        output_filename = "Gauge_animation_"+nice_name.lower()+stub+f"_{i:05d}"+".png"
        plt.savefig(os.path.join(output_dir,output_filename), dpi=100)
        plt.close()

if __name__ == "__main__":
    main()

