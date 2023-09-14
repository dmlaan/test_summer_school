import numpy as np  # version 1.24.2
import pims  # PIMS version 0.6.1

"""
In this script, functions will be defined that will be used in the code: particle_locating_copy.py
"""

@pims.pipeline  # here we are defining a pipeline that will convert an RGB movie frame into a grayscale image.
def as_grey(frame):
    red = frame[:, :, 0]
    green = frame[:, :, 1]
    blue = frame[:, :, 2]
    return 0.05 * red + 0.99 * green + 0.05 * blue

def calc_bgframe(frames, n=10):
    path = "/Shared/analysis_did_feb2023/particle_tracking"  # specify the path where your videos are saved
    # Calculate the background by taking the median frame of n frames evenly distributed in the stack
    ind = np.arange(0, len(frames), np.round(len(frames) / n), dtype=int)
    # Calculate the background using the median
    substack = frames[ind]
    bgd = np.median(substack, axis=0)
    return bgd

@pims.pipeline  # this pipeline subtracts the background for each movie frame
def bgd_sub(frame, bgframe):
    return np.absolute(frame - bgframe)

def bg_sliding_window(video, n=2000):
    """
    Calculates the background by taking the median of n frames locally.
    Substracts background frame from original image
    The result is that all objects in the video that are not moving for a certain period (=background), are removed
    """
    bg_subs = pims.Frame(np.zeros([len(video), video[0].shape[0], video[0].shape[1]]))
    last_bg = np.median(video[-n:-1], axis=0)  # for some reason I get 2 ind less
    for k in range(0, len(video) - n, n):
        # Calculate the backgrounds using the median
        substack = video[k : k + n]
        bgd = np.median(substack, axis=0)
        bg_subs[k : k + n] = np.abs(video[k : k + n] - bgd)
    print(k)
    bg_subs[-n:-1] = np.abs(video[-n:-1] - last_bg)
    return bg_subs