#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 10:37:52 2019

@author: sleek-eagle
"""

import laser_scanner as ls
import math

theta_dists = ls.get_theta_dists_and_plot(True)

#recreate the cartesian map from the laser scanner readings
coords = []
for reading in theta_dists:
    if(reading[1]!= -1):
        x = reading[1] * math.cos(reading[0])
        y = reading[1] * math.sin(reading[0])
        coords.append([x,y])
points = np.array(coords)
plt.scatter(points[:,0],points[:,1])






