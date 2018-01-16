#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 15 20:19:05 2017

@author: alcasser
"""
import time
import GFHelpers as gf
import quicksort as quick
import numpy as np
import matplotlib.pyplot as plt

def timeForGF_product_T(a, b):
    exponentialT, logarithmT = gf.GF_tables()
    start_time = time.process_time()
    gf.GF_product_t(a, b, exponentialT, logarithmT)
    stime = time.process_time() - start_time
    return stime

def timeForGF_product_P(a, b):
    start_time = time.process_time()
    gf.GF_product_p(a, b)
    stime = time.process_time() - start_time
    return stime

def GF_product_TvsGF_productP(n_runs, b):
    resultsMedian = [[0.0, 0.0] for y in range(256)]
    for i in range(256):
        repetitionsProductT = []
        repetitionsProductP = []
        for _ in range(n_runs):
            repetitionsProductT.append(timeForGF_product_T(i, b))
        for _ in range(n_runs):
            repetitionsProductP.append(timeForGF_product_P(i, b))
        quick.quickSort(repetitionsProductT)
        quick.quickSort(repetitionsProductP)
        med = n_runs // 2
        resultsMedian[i][0] = repetitionsProductT[med]
        resultsMedian[i][1] = repetitionsProductP[med]
    return resultsMedian

def graphResutlsAsBarChart(results, value):
    n_groups = 256
    
    medians_table = [results[i][0] for i in range(256)]
    
    
    mediants_poly = [results[i][1] for i in range(256)]
    
    fig, ax = plt.subplots()
    
    index = np.arange(n_groups)
    bar_width = 0.75
    
    opacity = 1
    
    rects1 = plt.bar(index, medians_table, bar_width,
                     alpha=opacity,
                     color='b',
                     label='Product using tables')
    
    rects2 = plt.bar(index + bar_width, mediants_poly, bar_width,
                     alpha=opacity,
                     color='r',
                     label='Product of polynomials')
    
    plt.xlabel('GF(256)')
    plt.ylabel('Time (s)')
    plt.title('Time comparison multiplying all elements in GF(256) by {}'.format(value))
    plt.xticks(index + bar_width / 2, ())
    plt.legend()
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    #results02 = GF_product_TvsGF_productP(10, 0x02)
    #results03 = GF_product_TvsGF_productP(10, 0x03)
    #results09 = GF_product_TvsGF_productP(10, 0x09)
    #results0B = GF_product_TvsGF_productP(10, 0x0B)
    #results0D = GF_product_TvsGF_productP(10, 0x0D)
    results0E = GF_product_TvsGF_productP(10, 0x0E)
    graphResutlsAsBarChart(results0E, 0x0E)