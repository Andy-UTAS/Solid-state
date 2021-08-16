#!/usr/bin/python

"""
SSP.py: a program to deliver required content for jupyter notebooks to compliment the solid-state course
"""

######### Make default plot style #########
import matplotlib

# Define the default plot style through rcParams
def setplotstyle():
    matplotlib.rcParams['text.usetex'] = False
    matplotlib.rcParams['figure.figsize'] = (10, 7)
    matplotlib.rcParams['font.size'] = 16
    matplotlib.rcParams['axes.linewidth'] = 2.5
    for p in ['xtick', 'ytick']:
        matplotlib.rcParams[p+'.major.size'] = 10
        matplotlib.rcParams[p+'.minor.size'] = 2.5
        matplotlib.rcParams[p+'.major.width'] = 2.5
        matplotlib.rcParams[p+'.major.width'] = 1.5

def draw_classic_axes(ax, x=0, y=0, xlabeloffset=.1, ylabeloffset=.07):
    ax.set_axis_off()
    x0, x1 = ax.get_xlim()
    y0, y1 = ax.get_ylim()
    ax.annotate(
        ax.get_xlabel(), xytext=(x1, y), xy=(x0, y),
        arrowprops=dict(arrowstyle="<-"), va='center'
    )
    ax.annotate(
        ax.get_ylabel(), xytext=(x, y1), xy=(x, y0),
        arrowprops=dict(arrowstyle="<-"), ha='center'
    )
    for pos, label in zip(ax.get_xticks(), ax.get_xticklabels()):
        ax.text(pos, y - xlabeloffset, label.get_text(),
                ha='center', va='bottom')
    for pos, label in zip(ax.get_yticks(), ax.get_yticklabels()):
        ax.text(x - ylabeloffset, pos, label.get_text(),
                ha='right', va='center')

######### Import packages #########
import pandas as pd # panads for data manipulation
import numpy as np # numpy for all things mathematical/numerical
import matplotlib.pyplot as plt # matplotlib.pyplot for plotting
import matplotlib.animation as animation # matplotlib.animation for making animations
import plotly.offline as py
import plotly.graph_objs as go
from IPython.display import HTML 
import wikitables
import scipy.constants as const # scipy.constants for physical constants
from scipy.optimize import curve_fit # scipy.optimize for curve fitting
import scipy.integrate as integrate #scipy.integrate for numerical integration

######### "Global variables" (not actually gloabl variables in the python sense) #########
R = const.R
hbar = const.hbar
kb = const.k

setplotstyle() # Set the plot style