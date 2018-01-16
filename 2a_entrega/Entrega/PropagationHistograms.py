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
    possibleNumberOfChanges = list(set(nchanges))
    fin = [ possibleNumberOfChanges.index(i) for i in nchanges]
    plt.hist(fin, bins=range(len(possibleNumberOfChanges) + 1), align="left")
    plt.xticks(range(len(possibleNumberOfChanges)), possibleNumberOfChanges)
    plt.title("Number of total bits changed per modification histogram")
    plt.xlabel("Number of bits changed")
    plt.ylabel("Frecuency")
    plt.show()

def propagateChangesMessagePositions():
    aesv = aes.AES(master_key)
    m = 0x1597C4EF331CC28B7E6D1B2EB3EA3B95
    c = aesv.encrypt(m)
    binc = asBinString(c)
    posChanging = {}
    for i in range(128):
        mi = m ^ (1 << i)
        ci = aesv.encrypt(mi)
        binci = asBinString(ci)
        pos = 0
        for bit in binci:
            if (bit != binc[pos]):
                if pos in posChanging:
                    posChanging[pos] += 1
                else:
                    posChanging[pos] = 1
            pos += 1
    width = 0.5
    plt.figure(figsize=(10, 12))
    plt.ylabel("Frecuency")
    plt.xlabel("Bins of positions changing")
    plt.bar(posChanging.keys(), posChanging.values(), width, color='g')
    
def propagateChangesKeyNumBits():
    key = 0x2b7e151628aed2a6abf7158809cf4f3c
    aesv = aes.AES(key)
    m = 0x1597C4EF331CC28B7E6D1B2EB3EA3B95
    c = aesv.encrypt(m)
    nchanges = []
    for i in range(128):
        keyi = key ^ (1 << i)
        aesv = aes.AES(keyi)
        ci = aesv.encrypt(m)
        nchanges.append(nDiffBits(c, ci))
    possibleNumberOfChanges = list(set(nchanges))
    fin = [ possibleNumberOfChanges.index(i) for i in nchanges]
    plt.hist(fin, bins=range(len(possibleNumberOfChanges) + 1), align="left")
    plt.xticks(range(len(possibleNumberOfChanges)), possibleNumberOfChanges)
    plt.title("Number of total bits changed on key bit modifications histogram")
    plt.xlabel("Number of bits changed")
    plt.ylabel("Frecuency")
    plt.show()

def propagateChangesKeyPositions():
    key = 0x2b7e151628aed2a6abf7158809cf4f3c
    aesv = aes.AES(key)
    m = 0x1597C4EF331CC28B7E6D1B2EB3EA3B95
    c = aesv.encrypt(m)
    binc = asBinString(c)
    posChanging = {}
    for i in range(128):
        keyi = key ^ (1 << i)
        aesv = aes.AES(keyi)
        ci = aesv.encrypt(m)
        binci = asBinString(ci)
        pos = 0
        for bit in binci:
            if (bit != binc[pos]):
                if pos in posChanging:
                    posChanging[pos] += 1
                else:
                    posChanging[pos] = 1
            pos += 1
    width = 0.5
    plt.figure(figsize=(10, 12))
    plt.ylabel("Frecuency")
    plt.xlabel("Bins of positions changing")
    plt.bar(posChanging.keys(), posChanging.values(), width, color='g')
        
 
#propagateChangesMessageNumBits()
propagateChangesMessagePositions()
#propagateChangesKeyNumBits()
propagateChangesKeyPositions()
