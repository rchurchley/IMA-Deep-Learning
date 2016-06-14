# Image Anomaly Detection with Neural Networks

This repository contains the experiments and final report of Team 5 at the [Mathematical Modeling in Industry workshop](https://www.ima.umn.edu/2014-2015/MM8.5-14.15) held at the IMA in Minneapolis in August 2015. 
The contributors to this repository are graduate students and advanced undergraduates working under the guidance of an industry mentor on a real-world industrial problem.

The contents of this repository have been frozen as of the submission of the group's final report in September 2015.
Further work inspired by this project can be found under the name [target-deep-learning](https://github.com/rchurchley/target-deep-learning).

## Abstract

Retailers currently manage very large numbers of digital photographs, typically within a very narrow scope.
Nearly all images are subject to some form of image manipulation, and because of the sheer number of images, some errors are inevitable. 
Leveraging the focused nature of the data (photos of similar objects, already categorized) it is hoped that it may be feasible for a convolutional neural network to learn to detect anomalous images.

Image manipulation errors, however, may come in many forms. 
Some high-profile cases have three models with seven hands between them due to bad photo compositing; more commonly, overzealous smudging, erasing, or stretching leads to models with bizarre proportions, artificial smoothness, or missing parts.

Given the wide range of potential anomalies — and lack of a labeled set of “anomalous” pictures at the scale we need for neural network training — we need to focus on a particular type of error which is easily reproduced programmatically. 
In this project, we consider the problem of detecting white rectangles added to an image, simulating the type of error where portions of an image are damaged or deleted.

We built several convolutional neural networks using the [Lasagne](https://github.com/Lasagne/Lasagne) Python library built on top of [Theano](https://github.com/Theano/Theano).
Each network was trained up to four datasets using the GPU architecture on the Minnesota Supercomputing Institute’s Mesabi compute cluster.
Our final report summarizes the partial progress made by our networks over the course of the workshop.
