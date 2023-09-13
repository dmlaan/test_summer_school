"""" Locating cells in microscopy videos

The goal is to analyse swimming ciliates in videos of 5 minutes, imaged with 30 frames per second. (mp4 format)
Before tracking the cells and obtaining the trajectories, the cells need to be found in the video.
This code finds per frame the particle locations of the cells.

In a next code these particle locations will be linked to trajectories.

Authors: Guillermina Ramirez, Daphne laan
Contact: daphne.laan@epfl.ch
Date created: ????
Status: in progress
"""

##################
# Review history #
##################

# Reviewed by Name Date #


#############
# Libraries #
#############
# Python version 3.9 is used

import glob as glob  # glob2 version 0.7

import matplotlib.pyplot as plt  # matplotlib version 3.6.3
import numpy as np  # version 1.24.2
import pims  # PIMS version 0.6.1
import trackpy as tp  # version 0.4.2
from skimage.filters import (  # scikit-image version 0.19.3
    difference_of_gaussians, gaussian, median)


# define path to files to track
path = "/Shared/analysis_did_feb2023/particle_tracking/"  # specify the path where your videos are saved

# When analyzing 1 video
file = "1Param1_3.mp4"

# When analyzing multiple videos at the same time
# files = glob.glob(path + '*.mp4')
# files.sort()
# file = files[0]


video = as_grey(pims.open(file))
bgd = calc_bgframe(video, n=2000)
bgd_subs = bgd_sub(video, bgd)  # remove background
bgd_subs = video
sigma = 1
n = 2000
im = bg_sliding_window(video, n=n)

# %% This part is to save the preprocessed video
# from skimage import io
# import imageio
# im = io.imread(video)
# imageio.mimwrite(file[:-4]+'_preprocessed.mp4', im, fps=30, macro_block_size=1)


# %%
# Now that we have a preprocessed video we will first identify cells. First analyze a few movie frames individually
# the values chosen for diameter and minmass will change the output
#TODO
diameter = 15 #TODO change name; in pixels
minmass = 1500 #TODO change name

#TODO test if parameters work
frame = 400
test = tp.locate(im[frame], diameter=diameter, minmass=minmass, preprocess="False")
tp.annotate(test, im[frame])
# %%
# Once you have determined which parameters work the best you can process several frames from the video. If your
# video is long this can take a while.

f = tp.batch(
    im, processes=0, diameter=diameter, minmass=minmass, preprocess="False"
)  # It is key to have the parameter processes set to zero or this freaks out
#TODO change text, add input int float...

np.savetxt(file[0:-4] + "_positions.txt", f, fmt="%10.2f", delimiter=" ", newline="\n")

# Now we will save the pandas data frame with all particle positions for further analysis
f.to_pickle(file[0:-4] + "_particles.pkl")

partfind_params = {}
partfind_params["nwindow"] = n
partfind_params["sigma"] = sigma
partfind_params["diameter"] = diameter
partfind_params[
    "minmass"
] = minmass  # list of parameter names, will be used later to store settings

savepath = file[:-4] + "_locate_params.txt"
with open(savepath, "w") as data:  # save dictionary to text file
    data.write(str(partfind_params))
# Now we will save the pandas data frame with all particle positions for further analysis
f.to_pickle(file[0:-4] + "_particles.pkl")

partfind_params = {}
partfind_params["nwindow"] = n
partfind_params["sigma"] = sigma
partfind_params["diameter"] = diameter
partfind_params[
    "minmass"
] = minmass  # list of parameter names, will be used later to store settings

savepath = file[:-4] + "_locate_params.txt"
with open(savepath, "w") as data:  # save dictionary to text file
    data.write(str(partfind_params))
