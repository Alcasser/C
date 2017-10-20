#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 20:27:54 2017

@author: alcasser
"""

import aes
import matplotlib.pyplot as plt

master_key = 0x2b7e151628aed2a6abf7158809cf4f3c
            
def asBinString(aInt):
    return '{0:0128b}'.format(aInt)

def nDiffBits(cyph1, cyph2):
    binc1 = asBinString(cyph1)
    binc2 = asBinString(cyph2)
    ndiffs = 0
    for i in range(len(binc1)):
        if (binc1[i] != binc2[i]):
            ndiffs += 1
    return ndiffs

def propagateChangesMessageNumBits():
    aesv = aes.AES(master_key)
    m = 0x1597C4EF331CC28B7E6D1B2EB3EA3B95
    c = aesv.encrypt(m)
    nchanges = []
    for i in range(128):
        mi = m ^ (1 << i)
        ci = aesv.encrypt(mi)
        nchanges.append(nDiffBits(c, ci))
    possibleChanges = list(set(nchanges))
    fin = [ possibleChanges.index(i) for i in nchanges]
    plt.hist(fin, bins=range(len(possibleChanges) + 1), align="left")
    plt.xticks(range(len(possibleChanges)), possibleChanges)
    plt.title("Number of bits changed per modification histogram")
    plt.xlabel("Number of bits changed")
    plt.ylabel("Number of modifications")
    plt.show()

def propagateChangesMessagePositions():
    pass
        
 
propagateChangesMessage()

