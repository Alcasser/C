#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 15 20:19:05 2017

@author: alcasser
"""
import time
import GFHelpers

def timeForGF_product_T(a, b):
    exponentialT, logarithmT = GFHelpers.GF_tables()
    start_time = time.time()
    GFHelpers.GF_product_t(a, b, exponentialT, logarithmT)
    stime = time.time() - start_time
    return stime

def timeForGF_product_P(a, b):
    start_time = time.time()
    GFHelpers.GF_product_p(a, b)
    stime = time.time() - start_time
    return stime

    
def GF_product_TvsGF_productP(a, b, n_runs):
    f, c = n_runs, 2
    results = [[0 for x in range(c)] for y in range(f)]
    for repetition in results:
        repetition[0] = timeForGF_product_T(a, b)
        repetition[1] = timeForGF_product_P(a, b)
    return results

def generateReport(n_runs):
    results = GF_product_TvsGF_productP(0, 0x5f, n_runs)
    print(results)
    
    

if __name__ == "__main__":
    generateReport(10)  
