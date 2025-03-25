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
        '-m', 
        '--model', 
        help="the elevevation csv file (file only) from the extract_gague.py script. Defaults to model_gauges_elev.csv in the model dir",
        default="model_gauges_elev.csv"
    )
    parser.add_argument(
        '-t',
        '--tide',
        help="The tide gauge file, including path. Default is '../data/tide_gauges.csv'",
        default="../data/tide_gauges.csv"
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
    model_input_file = args.model
    tide_gauges = args.tide
    stub = args.stub
    model_dirs = args.model_dirs
    labels = args.labels
    model_input = []
    for model_dir in model_dirs:
    	model_input.append(os.path.join(model_dir, model_input_file))

    plt.rcParams.update({'font.size': 22})
    #################################################
    # assumes you've run extract_guage.py and obtained the file for that

    constituents =  ['M2', 'S2', 'K1', 'O1', "Q1", "P1", "N2", "K2"]
    #constituents =  params.constituents

    model_data = []
    model_times = []
    for model in model_input:
        # read in the model data first to make sure we use the times from that
        df = pd.read_csv(model)
        model_data.append(df)
        model_times.append(df["Time"].to_numpy())
    
    # sort out which is the longest model time to use as the "gauges" time
    max_time = 0
    for t in model_times:
        if t[-1] > max_time:
            max_time = t[-1]

    t_start = model_times[0][0]
    t_export = model_times[0][1] - model_times[0][0]
    t_end = max_time
    tide = uptide.Tides(constituents)  # select which constituents to use from the tide gauge data
    tide.set_initial_time(params.start_datetime+datetime.timedelta(hours=10))

    colours = ['#377eb8', '#ff7f00', '#4daf4a',
               '#a65628', '#984ea3', '#f780bf',
               '#999999', '#e41a1c', '#dede00']
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

    # output dir is the run name, minus the csv file, which we discard
    output_dir, filename = os.path.split(model_input[0])
    # try make the output dir
    os.makedirs(os.path.join(output_dir,"Tidal_Validation"), exist_ok=True)

    if verbose:
        print("Reading in tidal gauges")
    # tide gauge data comes back as two nested dicts
    #{location_name: {M2Amp: x, M2Phase:, y, etc, etc}
    tide_gauge_data = read_tide_gauge_data(tide_gauges)

    print("Saving output in", output_dir+"/Tidal_Validation")

    # now loop over tide gauges and plot them.
    for name in tide_gauge_data:
        # pull amplitude
        obs_amps = []
        obs_phases = []
        for t in constituents:
            obs_amps.append(float(tide_gauge_data[name][t+" amp"]))
            obs_phases.append(np.radians(float(tide_gauge_data[name][t+" phase"])))

        t = np.arange(t_start, t_end, t_export)
        eta = tide.from_amplitude_phase(obs_amps, obs_phases, t)

        fig_summary=plt.figure(figsize=(12.0,6),dpi=360)
        ax=fig_summary.add_subplot(111)

        # Prettier and fixes LaTeX issue
        nice_name = tex_escape(name.replace("_"," ").title())
        obs_ln = ax.plot(t / 86400., eta, color="grey", lw=3, label="Tide gauge", alpha=0.4)
        i = 0
        model_lns = []
        for times, model, label in zip(model_times, model_data, labels):
            mod_ln = ax.plot(times/86400., model[name].to_numpy(), color=colours[i], lw=1, label=label, alpha=0.5)
            model_lns.append(mod_ln)
            i = i+1
        ax.set_xlabel("Time (days)")
        ax.set_ylabel("Water height (m)")
        leg = ax.legend(loc='lower right',ncol=1)
        leg.get_frame().set_edgecolor('k')
        ax.set_title(nice_name)
        if not stub is None:
            name = name +"_" + stub
        plt.savefig(os.path.join(output_dir,"Tidal_Validation","comp_tidal_plot_"+name+".pdf"), dpi=180, bbox_inches = 'tight', pad_inches = 0)
        plt.close()
        
if __name__ == "__main__":
    main()
