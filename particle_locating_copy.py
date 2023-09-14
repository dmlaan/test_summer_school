"""" Locating cells in microscopy videos

The goal is to analyse swimming cells in videos of 5 minutes, imaged with 30 frames per second. (mp4 format)
Before tracking the cells and obtaining the trajectories, the cells need to be found in the video.
This code finds the particle locations of the cells for each frame.
It can take a couple of minutes to finish the code because the videos are 5 minutes, which have 9000 frames.

The output will be a pickle file containing the particle locations for each frame, which can be opened and used in Python.
In a next code these particle locations will be linked to trajectories.

Authors: Guillermina Ramirez, Daphne laan
Contact: daphne.laan@epfl.ch
Date created: Feb2023
Status: Finished
"""

##################
# Review history #
##################
# This script has not been reviewed yet

#############
# Libraries #
#############
# Python version 3.9 is used
import numpy as np  # version 1.24.2
import pims  # PIMS version 0.6.1
import trackpy as tp  # version 0.4.2
from functions_image_analysis import as_grey, calc_bgframe, bgd_sub, bg_sliding_window #fuctions used in this script which are saved in a functions script
from skimage import io #scikit_image version 0.19.3
import imageio #version 2.25.1
import glob as glob  # glob2 version 0.7

###################
# Start of script #
###################

# define path to files to track
path = "/Users/laan/Desktop/Workspace/test_summer_school/"  # specify the path where your videos are saved

# When analyzing 1 video
file = "test_video.mp4"

# When analyzing multiple videos at the same time
# files = glob.glob(path + '*.mp4')
# files.sort()
# file = files[0]

#preprocessing of the video: removing the background for each frame
sigma = 1
n = 2000 #the amount of frames to average over when subtracting the background
video = as_grey(pims.open(file)) #frames in video converted to greyscale image
bgd = calc_bgframe(video, n=n)
bgd_subs = bgd_sub(video, bgd)  # remove background
bgd_subs = video
im = bg_sliding_window(video, n=n)

# This part is to save the preprocessed video, with the same speed and size as the original video
im = io.imread(video)
imageio.mimwrite(file[:-4]+'_preprocessed.mp4', im, fps=30, macro_block_size=1)

# %%
# Now that we have a preprocessed video we will first identify cells. First analyze a few movie frames individually
# the values chosen for diameter and minmass will change the output
diameter_px = 15 #size of particles in pixels
minmass_intensity = 1500 #minimum integrated brightness

#To test which parameters work best, you can locate the particles for one frame first instead of the whole video
frame = 400
test = tp.locate(im[frame], diameter=diameter_px, minmass=minmass_intensity, preprocess="False")
tp.annotate(test, im[frame])

#%%
# Once you have determined which parameters work the best you can process several frames from the video. If your
# video is long this can take a while.
f = tp.batch(
    im, processes=0, diameter=diameter_px, minmass=minmass_intensity, preprocess="False"
)  # It is key to have the parameter processes set to zero or this freaks out

#save coordinates of particles for each frame
np.savetxt(file[0:-4] + "_positions.txt", f, fmt="%10.2f", delimiter=" ", newline="\n")
# Now we will save the pandas data frame with all particle positions for further analysis
f.to_pickle(file[0:-4] + "_particles.pkl")

# list of parameter names, will be used later to store settings
partfind_params = {}
partfind_params["nwindow_in_frames"] = n
partfind_params["diameter_in_pixels"] = diameter_px
partfind_params["minmass"] = minmass_intensity

#store parameters used in text file
savepath = file[:-4] + "_locate_params.txt"
with open(savepath, "w") as data:  # save dictionary to text file
    data.write(str(partfind_params))