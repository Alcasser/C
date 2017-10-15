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
    GFHelpers.GF_product_t()
    
    
def GF_product_TvsGF_productP(a, b, n_runs):
    #TODO: write method to return the 2 times using Tables and mult n_run
    # times
    #kek
    f, c = n_runs, 2
    results = [[0 for x in range(c)] for y in range(f)]
    for repetition in results:
        for result in repetition:
            

def generateReport(n_runs):
    GF_product_TvsGF_productP(0, 1, n_runs)
    
    

if __name__ == "__main__":
    generateReport(10)  
