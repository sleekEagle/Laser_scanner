#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 10:37:52 2019

@author: sleek-eagle
"""

import laser_scanner as ls
import math
from matplotlib import pyplot as plt



theta_dists = ls.get_theta_dists_and_plot(True)
coords = get_cartesian(theta_dists,True)
around = get_map(coords,True)


hori_lines = []
for y in range(0,around.shape[0]):
    started=False
    start=-1
    not_count=0
    for x in range(0,around.shape[1]):
        if((not started) and  (around[y,x] == 1)):
            started=True
            start=x
            not_count=0

        elif(started): 
            if(around[y,x] == 1):
                not_count = 0
            if((around[y,x] == 0)):
                not_count+=1
                
            if((not_count > 5) or (x == (around.shape[1]-1))):
                started=False
                end = x
                #save line
                if(not_count > 5):
                    end-=5
                if((end-start) > 5):
                    hori_lines.append([[y,start],[y,end]])
                not_count=0
            
        




#recreate the cartesian map from the laser scanner readings
def get_cartesian(theta_dists,is_plot):
    coords = []
    for reading in theta_dists:
        if(reading[1]!= -1):
            x = reading[1] * math.cos(reading[0])
            y = reading[1] * math.sin(reading[0])
            coords.append([x,y])
    points = np.array(coords)
    if(is_plot):
        plt.scatter(points[:,0],points[:,1])
    
    coords = np.array(coords)
    return coords
    

#get encoded map given cartesian coordinates (0 is a free space 1 is occupied e.g by wall or another obstacle detected by laser scanner)
def get_map(coords, is_plot):
    x_coords = coords[:,0]
    y_coords = coords[:,1]
    
    min_x = math.floor(min(x_coords))
    max_x = math.ceil(max(x_coords))
    min_y = math.floor(min(y_coords))
    max_y = math.ceil(max(y_coords))
    
    increment = 0.1
    
    # detect horizontal lines
    
    x_range = np.arange(min_x,max_x+increment,increment)
    y_range = np.arange(min_y,max_y+increment,increment)
    around = np.zeros([y_range.shape[0],x_range.shape[0]],np.int8)
    
    x_step = (max_x - min_x)/x_range.shape[0]
    y_step = (max_y - min_y)/y_range.shape[0]
    for coord in coords:
        x = int((coord[0] - min_x)/x_step)
        y = int((coord[1] - min_y)/y_step)
        if(x >= around.shape[1]):
            x = around.shape[1]-1
        if(y >= around.shape[0]):
            y = around.shape[0]-1
        around[y,x] = 1
        print(x,y)
    if(is_plot):
        plt.imshow(np.flip(around,0), interpolation='nearest')
    return around
    
    
        

def get_closest_coord_dist(x,y,coords):
    dists = []
    for coord in coords:
        dist = ls.get_dist([x,y],[coord[0],coord[1]])
        dists.append(dist)
    return [coords[dists.index(min(dists))],min(dists)]
        