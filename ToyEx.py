# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 15:43:34 2015

@author: Parker Williams
"""

import numpy as np
import os
import cv2
#import skimage as sk
#import skimage.io as io
#from skimage import feature

#all_Good_Images = np.zeros((1,120000))
#all_Bad_Images = np.zeros((1,120000))

ImgSize = 200; # images are squares; length of the side 

all_Good_Images = np.zeros((1,ImgSize**2))
all_Bad_Images = np.zeros((1,ImgSize**2))

#for each inmage in the folder, read it in

for filename in os.listdir('good_images'):
    try:
        #grab the images
        currentimage = cv2.imread('good_images/'+filename,0)#0: greyscale

        print "working on " + filename        
        
        #process
        #canny1 = feature.canny(currentimage)
        #canny3 = feature.canny(currentimage,sigma = 3)
        #stack processes images
        #stacked = np.vstack([currentimage,canny1,canny3])
        stacked = currentimage
        
        #flatten
        flat = np.atleast_2d(np.reshape(stacked,(stacked.shape[0]*stacked.shape[1],1)))
       
        
        #finally add it to master
        all_Good_Images = np.append(all_Good_Images,flat.T,axis=0)
        print  str(all_Good_Images.shape) 

    except:
        print "Error with " + filename

all_Good_Images = np.delete(all_Good_Images,0,0)
print 'number of good images ' + str(len(all_Good_Images))


for filename in os.listdir('bad_images'):
    try:
        #grab the images
        currentimage = cv2.imread('bad_images/'+filename,0)#0:greascale

        print "working on " + filename        
        
        #process
        #canny1 = feature.canny(currentimage)
        #canny3 = feature.canny(currentimage,sigma = 3)
        #stack processes images
        stacked = currentimage
        
        #flatten
        flat = np.atleast_2d(np.reshape(stacked,(stacked.shape[0]*stacked.shape[1],1)))
        
        #finally add it to master
        all_Bad_Images = np.append(all_Bad_Images,flat.T,axis=0)
        print 'all_Bad_Images dimension' + str(all_Bad_Images.shape)
    except:
        print "Error with " + filename


all_Bad_Images = np.delete(all_Bad_Images,0,0)
print 'number of bad images ' +str(len(all_Bad_Images))


#data are ndarray; they are vectorized images
print "opening good data"

gx=all_Good_Images
glen = gx.shape[0]
gy = np.atleast_2d(np.ones(glen)).T
gdata = np.hstack((gx,gy))

print "opening bad data"

bx = all_Bad_Images
blen = bx.shape[0]
by = np.atleast_2d(np.zeros(blen)).T
bdata = np.hstack((bx,by))

print "shuffling data"

#shuffle the data
alldata = np.vstack((gdata,bdata))
#np.random.shuffle(alldata)

print "break into training validation and testing"

#decide the sizes for training, validation and testing
m=alldata.shape[0]
n=alldata.shape[1]

m_training = np.floor(m/11)*8
m_training = m_training.astype(int)
m_validation = np.floor(m/11)*2
m_validation = m_validation.astype(int)
m_test = m -m_training-m_validation

print "split data"

#split data into x and y
x = alldata[:,:-1] 
print str(x.shape)
y = alldata[:,-1]
print y.shape

#split data into training, val, and test
print "dump split data"
np.save(open('train_x.npy','wb'),x[range(0,m_training)].astype(np.float32))
np.save(open('train_y.npy','wb'),y[range(0,m_training)].astype(np.float32))
np.save(open('val_x.npy','wb'),x[range(m_training,m_training+m_validation)].astype(np.float32))
np.save(open('val_y.npy','wb'),y[range(m_training,m_training+m_validation)].astype(np.float32))
np.save(open('test_x.npy','wb'),x[range(m_validation+m_test,m)].astype(np.float32))
np.save(open('test_y.npy','wb'),y[range(m_validation+m_test,m)].astype(np.float32))











