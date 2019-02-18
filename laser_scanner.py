#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 16 12:58:59 2019

@author: sleek-eagle
"""

import math
import matplotlib.pyplot as plt
import numpy as np

pi =  3.141592653589793
point = [8,4]

#********laser scanner parameters
#angle limits 
MIN_ANGLE = 0
MAX_ANGLE = 3*pi/2
#minimum range in units
MIN_RANGE=0
#max range in unites
MAX_RANGE=8
#measure of resolution. Degrees between adjecent scan rays
INCREMENT = 0.03
#*********************************

#line segments defined as two points
#walls around the world
line1 = [[0,0],[11,0]]
line2 = [[0,0],[0,11]]
line3 = [[0,11],[11,11]]
line4 = [[11,11],[11,0]]
turt1 = [[5,5],[6,5]]
turt2 = [[5,5],[5,6]]
turt3 = [[5,6],[6,6]]
turt4 = [[6,5],[6,6]]

lines = [line1,line2,line3,line4,turt1,turt2,turt3,turt4]



def get_theta_dists_and_plot(is_plot):
    pts = get_points_thetas(point,lines)
    points = []
    points.append(point)
    theta_dists = []
    for pt in pts:
        if (pt[1] != -1):
            points.append(pt[1][0])
            theta_dists.append([pt[0],pt[1][1]])
        else:
            theta_dists.append([pt[0],pt[1]])
    points = np.array(points)
    if(is_plot):
        plt.scatter(points[:,0],points[:,1])
    return theta_dists
    

    

def get_points_thetas(point,lines):
    angle = MIN_ANGLE
    thetas = []
    while(angle <= MAX_ANGLE):
        thetas.append(angle)
        angle+=INCREMENT
    points_theta = []
    for theta in thetas:
        points_theta.append([theta , get_closest_valid_point(point,theta,lines)])
    return points_theta

def get_closest_valid_point(point,theta,lines):
    points = get_valid_inter_points(point,theta,lines)
    dists = []
    for pt in points:
        if(len(pt) == 0):
            dists.append(5000)
            continue
        dists.append(get_dist(pt,point))
    #get the point with the min distance
    if(len(dists)>0):
        min_ind = dists.index(min(dists))  
        #check if this is within scanner limits
        if ((min(dists) >= MIN_RANGE) and (min(dists) <= MAX_RANGE)):
            return [points[min_ind],min(dists)]
        else:
            return -1
    else:
        return -1
    

#get distance between points
def get_dist(point1,point2):
    return math.sqrt((point1[0]-point2[0])*(point1[0]-point2[0]) + (point1[1]-point2[1])*(point1[1]-point2[1]))

#get valid intersection point
def get_valid_inter_points(point,theta,lines):
    points = []
    for line in lines:
        int_point = get_intersection(point[0],point[1],theta,line[0][0],line[0][1],line[1][0],line[1][1])
        if(int_point != -1):
            if(check_point_in(line[0],line[1],[int_point[0],int_point[1]]) and check_point_correct_side([point[0],point[1]],theta,[int_point[0],int_point[1]])):
                points.append([int_point[0],int_point[1]])
    return points
#returns the positive angle i.e -pi becomes + pi
def get_positive_angle(alpha):
    if (abs(alpha) > 2*pi):
        if(alpha < 0):
            return -(-alpha)%(2*pi)
        else:
            return alpha%(2*pi)
    else:
        if(alpha < 0):
            return (2*pi + alpha)
        else:
            return alpha
    
    
def check_point_correct_side(point,theta,inter_point):
    if(abs(theta-pi/2) < 0.001):
        if((inter_point[1]-point[1]) > 0):
            return True
    if(abs(theta-0) < 0.001):
        if((inter_point[0]-point[0]) > 0):
            return True
    if(abs(theta-pi) < 0.001):
        if((inter_point[0]-point[0]) < 0):
            return True
    if(abs(theta+pi) < 0.001):
        if((inter_point[0]-point[0]) < 0):
            return True
    if(abs(theta + pi/2) < 0.001):
        if((inter_point[1]-point[1]) < 0):
            return True
    this_angle = math.atan2((inter_point[1]-point[1]),(inter_point[0]-point[0]))
    if (abs(get_positive_angle(this_angle) - get_positive_angle(theta)) < 0.01):
        return True
    return False

def check_point_in(point1,point2,point):
    max_x = max(point1[0],point2[0])
    min_x = min(point1[0],point2[0])
    max_y = max(point1[1],point2[1])
    min_y = min(point1[1],point2[1])
    #check if on the same line
    if((point1[1]-point2[1])*(point1[0]-point[0]) == (point1[1]-point[1])*(point1[0]-point2[0])):
        if((point[0] <= max_x) and (point[0] >= min_x) and (point[1] <= max_y) and (point[1] >=min_y)):
            return True
    return False

def get_intersection(a,b,theta,a1,b1,a2,b2):
    tan_theta=0
    lamb=0
    try:
        tan_theta = math.tan(theta)
        lamb = (b2-b1)/(a2-a1)
    except Exception as e:
        print(e)
         
    #check for corner cases
    #scanner line is parallel to y axis
    x = 0
    y = 0
    #both lines parallel to y
    if((abs(theta - pi/2) < 0.001) and (abs(a2-a1) < 0.01)):
        #print("scanner parallel to y and other line paralle to y")
        return -1
    #just the other line parallel to y
    elif(abs(a2-a1) < 0.01):
        #print("just the other line paralle to y")
        x = a1
        y = (a1-a)*tan_theta + b
        return x,y
    #just hte scanner parallel ot y
    elif(abs(theta - pi/2) < 0.001):
        #print("just the scanner parallel ot y")
        x = a
        y = lamb*(a-a2) + b2
        return x,y
    else:
        #print("no line is paralle to y")
        #both lines parallel to x axis
        if((abs(tan_theta) < 0.01) and (abs(lamb) < 0.01)):
            #print("both lines are parallel to x axis")
            return -1
        else:
            #lines are of equal gradient
            if(abs(tan_theta - lamb) < 0.001):
                return -1
            if(abs(tan_theta) < 0.001):
                y = b
                x = (b-b2)/lamb + a2
                return x,y
            elif(abs(lamb) < 0.01):
                y=b2
                x=(b2-b)/tan_theta + a
                return x,y
            #print("at least one line is not paralle to x and no line is parallel to y")
            #print(tan_theta)
            #print(lamb)
            x = (b2-b-lamb*a2 + a*tan_theta)/(tan_theta - lamb)
            y = lamb * (x - a2) + b2
            return x,y
            

