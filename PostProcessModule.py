import numpy as np
from numpy import *
import os
import logging
import random
import k_means as kMeans
from copy import deepcopy
def extract_feature(inputRawImage, inputLabel):
    width, height = inputLabel.shape
    features=[]
    upperbrand=[]
    downbrand=[]
    center=[0,0]
    pointCount=0
    for i in range(width):
        for j in range(height):
            if(inputLabel[i][j]==1):
                center = center + [(float)(i), (float)(j)]
                pointCount = pointCount+1
    if pointCount > 0:
        center[0] = center[0] / pointCount
        center[1] = center[1] / pointCount
    for i in range(width):
        x=height-1
        for j in range(height):
            if(inputLabel[i][j]==1):
                x = j
                break
        upperbrand.append(x)
    for i in range(width):
        x = 0
        for j in range(height):
            if(inputLabel[i][height-1-j]==1):
                x = height-1-j
                break
        downbrand.append(x)
    for i in range(width):
        for j in range(height):
            if(inputLabel[i][j]==1):
                feature=[]
                feature.append(i)
                feature.append(j)
                feature.append(abs(i-center[0]))
                feature.append(abs(j-center[1]))
                feature.append(inputRawImage[i][j][0])
                feature.append(inputRawImage[i][j][1])
                feature.append(inputRawImage[i][j][2])
                feature = map(float, feature)
                features.append(feature)
    maxFeature=deepcopy(features[0])
    minFeature=deepcopy(features[0])
    for feature in features:
        for i in range(7):
            if feature[i] > maxFeature[i]:
                maxFeature[i]=feature[i]
            if feature[i] < minFeature[i]:
                minFeature[i]=feature[i]
    for i in range(5):
        if(maxFeature[i+2]-minFeature[i+2]>100000):
            for idx in range(len(features)):
                features[idx][i+2] = features[idx][i+2]/(maxFeature[i+2]-minFeature[i+2])
                #if i > 1:
                #    features[idx][i+2] = features[idx][i+2]/1.732
    return features
    


def lip_segmentation(inputRawImage, inputLabel):
    retLabel = inputLabel
    width,height=retLabel.shape
    for i in range(width):
        for j in range(height):
            retLabel[i][j]==0
    features=extract_feature(inputRawImage,inputLabel)
    center,clusterResult=kMeans.kMeans(mat(features),2)
    distance=sqrt(sum(power(center[0,2:]-center[1,2:],2)))
    for i in range(len(clusterResult)):
        x = features[i][0]
        y = features[i][1]
        if distance > 0:
            retLabel[x][y] = clusterResult[i,0]+1
        else:
            retLabel[x][y] = 2
    return distance,retLabel

def extract_feature2(inputRawImage, featureImage, inputLabel):
	width,height=inputLabel.shape
	features=[]
	cropWidth, cropHeight, channels = featureImage.shape
	rate = width / cropWidth
	for x in range(width):
		for y in range(height):
			if (inputLabel[x][y] == 1):
				feature=[]
				feature.append(x)
				feature.append(y)
				new_x = x / rate
				new_y = y / rate
				exFea=featureImage[new_x][new_y]
				for z in exFea:
					feature.append(z)
				features.append(feature)
	return features

def lip_segmentation2(inputRawImage, featureImage, inputLabel):
    retLabel = inputLabel
    width,height=retLabel.shape
    for i in range(width):
        for j in range(height):
            retLabel[i][j]==0
	for i in range(width):
		for j in range(height):
			retLabel[i][j] = 255 * math.exp(featureImage[i][j][0])/( math.exp(featureImage[i][j][0]) + math.exp(featureImage[i][j][1]))
			print retLabel[i][j]
			if(retLabel[i][j]>128):
				retLabel[i][j] = (retLabel[i][j]-128) * 2
			else:
				retLabel[i][j] = 0
	return 0, retLabel
    features=extract_feature2(inputRawImage, featureImage, inputLabel)
    center,clusterResult=kMeans.kMeans(mat(features),2)
    distance=sqrt(sum(power(center[0,2:]-center[1,2:],2)))
    for i in range(len(clusterResult)):
        x = features[i][0]
        y = features[i][1]
        if distance > 0:
            retLabel[x][y] = clusterResult[i,0]+1
        else:
            retLabel[x][y] = 2
    return distance,retLabel
def eval_overlap(pred,inputLabel):
	width, height = inputLabel.shape
	count = 0
	for x in range(width):
		for y in range(height):
			if(inputLabel[x][y]==pred[x][y]):
				count += 1
	return float(count)/float(width*height)
