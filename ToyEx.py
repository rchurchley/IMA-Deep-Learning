# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 15:43:34 2015

@author: Parker Williams
"""

import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import os
import skimage as sk
import skimage.io as io


from skimage import feature

all_Images = np.array([])

#for each inmage in the folder, read it in

for filename in os.listdir('ToyExImages'):
    try
        #grab the images
        currentimage = io.imread('ToyExImages/'+filename,as_grey = True)
        
        #process
        canny1 = sk.filter.canny(currentimage)
        canny3 = sk.filter.canny(currentimage,sigma = 3)
        #stack processes images
        stacked = np.vstack([currentimage,canny1,canny3])
        
        #flatten
        flat = np.reshape(stacked,stacked.shape[0]*stacked.shape[1])
        
        #finally add it to master
        np.append(all_Images,flat)
    except:
        print "Error with " + filename

#Process it






