# -*- coding: utf-8 -*-
"""
Created on Wed Aug 21 13:14:52 2019

@author: HCRuiz
"""
import numpy as np
from SkyNEt.modules.Classifiers import perceptron 

def accuracy_fit(self, output, target, clip=35):
#        print('shape of target = ', target.shape)
    if np.any(np.abs(output)>clip):
        acc = 0
        print(f'Clipped at {clip} nA')
    else:
        x = output[:,np.newaxis]
        y = target[:,np.newaxis]
#        print('shape of x,y: ', x.shape,y.shape)
        acc, _, _ = perceptron(x,y)
    return acc

def corr_fit(self, output, target, clip=35):
    if np.any(np.abs(output)>clip):
        print(f'Clipped at {clip} nA')
        corr = -1
    else:
        x = output[:,np.newaxis]
        y = target[:,np.newaxis]
        X = np.stack((x, y), axis=0)[:,:,0]
        corr = np.corrcoef(X)[0,1]
#        print('corr_fit')
    return corr
