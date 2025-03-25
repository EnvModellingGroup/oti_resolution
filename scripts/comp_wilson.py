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
import re
import argparse
import uptide
import pytz

output = "Comparison_plots"

def tex_escape(text):
    """
        :param text: a plain text message
        :return: the message escaped to appear correctly in LaTeX
    """
    conv = {
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\^{}',
        '\\': r'\textbackslash{}',
        '<': r'\textless{}',
        '>': r'\textgreater{}',
    }
    regex = re.compile('|'.join(re.escape(str(key)) for key in sorted(conv.keys(), key = lambda item: - len(item))))
    return regex.sub(lambda match: conv[match.group()], text)

def main():

    parser = argparse.ArgumentParser(
         prog="plot gauges",
         description="""Plot  model gauges againt theoretical tides"""
    )
    parser.add_argument(
        '-v', 
        '--verbose', 
        action='store_true', 
        help="Verbose output: mainly progress reports.",
        default=False
    )
    parser.add_argument(
        '-e', 
        '--elev', 
        help="the elevation csv file (file only) from the extract_gague.py script. Defaults to model_gauges_elev_Wilson.csv in the model dir",
        default="model_gauges_elev_Wilson.csv"
    )
    parser.add_argument(
        '--vel', 
        help="the velocity csv file (file only) from the extract_gague.py script. Defaults to model_gauges_speed_Wilson.csv in the model dir",
        default="model_gauges_speed_Wilson.csv"
    )

    parser.add_argument(
        '-t',
        '--tide',
        help="The tide gauge file, including path. Default is '../data/wilson_gauges.csv'",
        default="../data/wilson_gauges.csv"
    )
    parser.add_argument(
        '-s',
        '--stub',
        help='short string to append onto output filenames, before the extension, e.g. using "7" would make the output "thetis_vs_obs_7.pdf"'
    )
    parser.add_argument(
        '--labels',
        nargs="+",
        help='The label to use in the plot for each model dir. Use -- after these arguments'
    )
    parser.add_argument(
        'model_dirs',
        nargs="+",
        help='The model run directory, e.g. ../sims/base_case/'
    )

    args = parser.parse_args()
    verbose = args.verbose    
    model_elev_file = args.elev
    model_speed_file = args.vel
    tide_gauges = args.tide
    stub = args.stub
    model_dirs = args.model_dirs
    labels = args.labels
    model_elev = []
    model_speed = []
    for model_dir in model_dirs:
        model_elev.append(os.path.join(model_dir, model_elev_file))
        model_speed.append(os.path.join(model_dir, model_speed_file))


    model_elev_data = []
    model_speed_data = []
    model_times = []
    for model in model_elev:
        # read in the model data first to make sure we use the times from that
        df = pd.read_csv(model)
        model_elev_data.append(df)
        model_times.append(df["Time"].to_numpy())

    # same for velocity
    for model in model_speed:
        # read in the model data first to make sure we use the times from that
        df = pd.read_csv(model)
        model_speed_data.append(df)

    
    # sort out which is the shortest model time and constrain all data to that
    min_time = 1e30
    n_times = 0
    for t in model_times:
        if t[-1] < min_time:
            min_time = t[-1]
            n_times = len(t)

    t_start = model_times[0][0]
    t_export = model_times[0][1] - model_times[0][0]
    t_end = min_time


    colours = {labels[0]: '#377eb8', 
               labels[1]: '#ff7f00', 
               labels[2]: '#4daf4a',
    #           labels[3]: '#a65628'
               }
    linestyle = {"C": "solid", 
                 "B": "dotted", 
                 "E": "dashed", 
                 "D": "dashdot"}
    plt_params = {
      'legend.fontsize': 12,
      'xtick.labelsize': 12,
      'ytick.labelsize': 12,
      'axes.labelsize' : 14,
      'figure.subplot.left' : 0.18,
      'figure.subplot.top': 0.82,
      'figure.subplot.right': 0.95,
      'figure.subplot.bottom': 0.15,
      'text.usetex' : True
        }
    plt.rcParams.update(plt_params)
    plt.rcParams.update({'font.size': 22})    

    # output dir is the run name, minus the csv file, which we discard
    output_dir, filename = os.path.split(model_elev[0])
    # try make the output dir
    os.makedirs(os.path.join(output_dir,output), exist_ok=True)

    if verbose:
        print("Reading in tidal gauges")
    # tide gauge data comes back as two nested dicts
    #{location_name: {M2Amp: x, M2Phase:, y, etc, etc}
    tide_gauge_data = read_tide_gauge_data(tide_gauges)
    # restrict names to C, B and E

    print("Saving output in", output_dir+"/"+output)
    start = 112
    stop = 145

    fig_summary=plt.figure(figsize=(8.3,11.7),dpi=360)
    plot_no = 1
    for times, model, label in zip(model_times, model_elev_data, labels):
        ax=fig_summary.add_subplot(3, 1, plot_no)
        model_lns = []
        for name in tide_gauge_data:
            mod_ln = ax.plot(times[start:stop]/3600., model[name].to_numpy()[start:stop], linestyle=linestyle[name], color=colours[label], lw=1, label=name)
            model_lns.append(mod_ln)
        ax.set_xlabel("Time (hrs)")
        ax.set_ylabel("Water height (m)")
        leg = ax.legend(loc='lower right',ncol=1)
        leg.get_frame().set_edgecolor('k')
        ax.set_title(label)
        plt.tight_layout()
        ax.set_ylim([-1,1])
        plot_no=plot_no+1
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir,output,"comp_wilson_tidal_plot.pdf"), dpi=180, bbox_inches = 'tight', pad_inches = 0)
    plt.close()


    fig_summary=plt.figure(figsize=(8.3,11.7),dpi=360)
    plot_no = 1
    for times, model, label in zip(model_times, model_speed_data, labels):
        ax=fig_summary.add_subplot(3, 1, plot_no)
        model_lns = []
        for name in tide_gauge_data:
            mod_ln = ax.plot(times[start:stop]/3600., model[name].to_numpy()[start:stop], linestyle=linestyle[name], color=colours[label], lw=1, label=name)
            model_lns.append(mod_ln)
        ax.set_xlabel("Time (hrs)")
        ax.set_ylabel("Speed (m/s)")
        leg = ax.legend(loc='lower right',ncol=1)
        leg.get_frame().set_edgecolor('k')
        ax.set_title(label)
        plt.tight_layout()
        ax.set_ylim([0,1.2])
        plot_no=plot_no+1
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir,output,"comp_wilson_speed_plot.pdf"), dpi=180, bbox_inches = 'tight', pad_inches = 0)
    plt.close()

        
if __name__ == "__main__":
    main()
