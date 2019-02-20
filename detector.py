#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 10:37:52 2019

@author: sleek-eagle
"""

import laser_scanner as ls
import math
from matplotlib import pyplot as plt
from numpy import linalg as la

TURT_SIDE = 1 

theta_dists = ls.get_theta_dists_and_plot(True)
coords = get_cartesian(theta_dists,True)
around,x_step,y_step = get_map(coords,True)
hori_lines, ver_lines = get_lines(around)

real_hori_lines,real_hori_points = get_real_lines(hori_lines,coords,x_step,y_step)
real_ver_lines,real_ver_points = get_real_lines(ver_lines,coords,x_step,y_step)
real_hori_lines = np.array(real_hori_lines).reshape((len(real_hori_lines),4))
real_ver_lines = np.array(real_ver_lines).reshape((len(real_ver_lines),4))

real_hori_lines=np.append(real_hori_lines,np.zeros((real_hori_lines.shape[0],1)),axis=1)
real_ver_lines=np.append(real_ver_lines,np.zeros((real_ver_lines.shape[0],1)),axis=1)

#************************************************
#****detect turtle and walls
#************************************************

#phase 1

#if line len is greater than TURT_SIDE this should be a wall. so mark that so
check_wall_len(real_hori_lines)
check_wall_len(real_ver_lines)

#phase 2
#detect verticle and hori lines which form corners and check if they are internal corners like in the case of walls of external corners 
#line in the case of turtle. If internal walls, mark both lines as walls

for row1 in range(real_hori_lines.shape[0]):
    for row2 in range(real_ver_lines.shape[0]):
        line1 = [[real_hori_lines[row1,0],real_hori_lines[row1,1]],[real_hori_lines[row1,2],real_hori_lines[row1,3]]]
        line2 = [[real_ver_lines[row2,0],real_ver_lines[row2,1]],[real_ver_lines[row2,2],real_ver_lines[row2,3]]]
        angle = get_intersect_points(line1,line2)
        print([line1,line2])
        print("angle.....")
        print(angle)
        if(angle == -1):
            continue
        
        p1 = np.array((angle[0][0],angle[0][1]))
        m = np.array((angle[1][0],angle[1][1]))
        p2 = np.array((angle[2][0],angle[2][1]))
        base = np.array((0,0))
        
        if(is_external(p1,m,p2,base)):
            real_hori_lines[row1,4]=2
            real_ver_lines[row2,4]=2
        else:
            real_hori_lines[row1,4]=1
            real_ver_lines[row2,4]=1  
            
            
            
#get the turtle position
hori_line = real_hori_lines[np.where(real_hori_lines[:,4]==2)]
vert_line = real_ver_lines[np.where(real_ver_lines[:,4]==2)]

if(((vert_line.shape[0] > 1) and (hori_line.shape[0] > 1)) or ((vert_line.shape[0]==0) and (hori_line.shape[0]==0))):
    print("cannot get positions")
else:
    if(vert_line.shape[0] == 1):
        pos = (vert_line[0][0] + vert_line[0][2])/2 , 

            
plt.scatter(np.array(real_points1)[:,0],np.array(real_points1)[:,1])
plt.scatter(np.array(real_points2)[:,0],np.array(real_points2)[:,1])
            
            
            
        
        
        
        
        
        



#check is 3 points form an internal or external corner
def is_external(p1,m,p2,base):
    m_p1 = p1-m
    m_p2 = p2-m
    m_p1_plus_m_p2 = m_p1 + m_p2
    m_base = base - m
    
    #check if m_base and m_p1_plus_m_p2 have the same direction by taking 
    dot_prod = np.dot(m_base,m_p1_plus_m_p2)
    
    if(dot_prod < 0):
        return True
    return False

#distance from a point to a line
#p1 is the point 
#p2 and p3 forms the line. All points are tuple format. i.e (x,y)
def get_dist_pt_line(p1,p2,p3):
    p1 = np.asarray(p1)
    p2 = np.asarray(p2)
    p3 = np.asarray(p3)
    
    d = la.norm(np.cross(p2-p1, p1-p3))/la.norm(p2-p1)
    return d





#check if two lines make a corner. i.e check for a common point
line1 = [[-2.7, 0.9], [-1.9, 0.9]]
line2 = [[-2.04, 0.95], [-2.04, 1.94]]
def get_intersect_points(line1,line2):
    lines = [line1,line2]
    ALLOW = 0.2
    for i in range(0,2):
        for j in range(0,2):
            dist = get_line_len([line1[i][0],line1[i][1],line2[j][0],line2[j][1]])
            print(dist)
            if(dist < ALLOW):
                pt1 = line1[1-i]
                pt2 = line2[1-j]
                mid = line1[i]
                return [pt1,mid,pt2]
    return -1



def check_wall_len(array):  
    #if lines are longer than TURT_SIDE they are walls for sure
    #4th column is the entity type
    #0 for not validated yet
    #1 is walls
    #2 is turtle
    for row in range(0,array.shape[0]):
        length = get_line_len(array[row,:])
        if(length > TURT_SIDE):
            array[row,4] = 1
        





#a line is two points in the format [[x1,y1],[x2,y2]]
def get_line_len(line):
    return math.sqrt((line[0] - line[2])*(line[0] - line[2]) + (line[1] - line[3])*(line[1] - line[3]))

def get_real_lines(lines,coords,x_step,y_step):
    real_lines = []
    real_points = []
    for line in lines:
        real_coords1 =  get_real_coords_from_map(line[0],coords,x_step,y_step)
        real_coords2 =  get_real_coords_from_map(line[1],coords,x_step,y_step)
        real_lines.append([real_coords1,real_coords2])
        real_points.append(real_coords1)
        real_points.append(real_coords2)

    return real_lines, real_points

def get_real_coords_from_map(point,coords,x_step,y_step):
    x=point[0]
    y=point[1]
    x_coords = coords[:,0]
    y_coords = coords[:,1]
    min_x = math.floor(min(x_coords))
    max_x = math.ceil(max(x_coords))
    min_y = math.floor(min(y_coords))
    max_y = math.ceil(max(y_coords))
    real_x = min_x + x_step*x
    real_y = min_y + y_step*y
    return real_x,real_y            
        
def get_lines(around):
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
                        hori_lines.append([[start,y],[end,y]])
                    not_count=0
                    
    ver_lines = []
    for x in range(0,around.shape[1]):
        started=False
        start=-1
        not_count=0
        for y in range(0,around.shape[0]):
            if((not started) and  (around[y,x] == 1)):
                started=True
                start=y
                not_count=0
    
            elif(started): 
                if(around[y,x] == 1):
                    not_count = 0
                if((around[y,x] == 0)):
                    not_count+=1
                    
                if((not_count > 5) or (y == (around.shape[0]-1))):
                    started=False
                    end = y
                    #save line
                    if(not_count > 5):
                        end-=5
                    if((end-start) > 5):
                        ver_lines.append([[x,start],[x,end]])
                    not_count=0
                    
    return hori_lines, ver_lines
    
    



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
    return around,x_step,y_step
    
    
        

def get_closest_coord_dist(x,y,coords):
    dists = []
    for coord in coords:
        dist = ls.get_dist([x,y],[coord[0],coord[1]])
        dists.append(dist)
    return [coords[dists.index(min(dists))],min(dists)]
        