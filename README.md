<!-- 
<a name="readme-top"></a>
<!--
-->

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

This repository contains 2 python scripts:
* One is the code to run --> particle_locating_copy.py
* The other one is a python script containing functions used by the code --> functions_image_analysis.py

The mp4 video can be used to test the script. 

The script locates cells in microscopy videos
The goal is to analyse swimming cells in videos of 5 minutes, imaged with 30 frames per second. (mp4 format)
Before tracking the cells and obtaining the trajectories, the cells need to be found in the video.
This code finds the particle locations of the cells for each frame.
It can take a couple of minutes to finish the code because the videos are 5 minutes, which have 9000 frames.

The output will be a pickle file containing the particle locations for each frame, which can be opened and used in Python.
In a next code these particle locations will be linked to trajectories.


### Built With

* Python


### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/dmlaan/test_summer_school.git
   ```
2. Install Python version 3.9
3. Install packages listed in the Python scripts


<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.



<!-- CONTACT -->
## Contact

Daphne Laan - daphne.laan@epfl.ch

Project Link: [https://github.com/dmlaan/test_summer_school](https://github.com/dmlaan/test_summer_school)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

