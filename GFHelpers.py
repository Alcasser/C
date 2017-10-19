#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AES
@author: alcasser
"""

def asBinString(aInt):
    return '{0:08b}'.format(aInt)

def addPolyArrayXor(aPolyArray):
    resPoly = aPolyArray[0]
    i = 1;
    while i < len(aPolyArray):
        resPoly = resPoly ^ aPolyArray[i]
        i += 1
    return resPoly

def reducePoly(aPoly):
    ir = 0x1B
    sp = asBinString(aPoly)
    length = len(sp)
    if (length < 9): return aPoly
    prange = range(0, length - 8)
    sumArray = []
    for i in prange:
        if (sp[i] == '1'):
            # print('Substitute by poly {} to reduce'.format(asBinString(ir << (length - 9 - i))))
            sumArray.append(ir << (length - 9 - i))
    sumArray.append(aPoly & 0xFF)
    reducedPoly = addPolyArrayXor(sumArray)
    if (len(asBinString(reducedPoly)) > 8):
        return reducePoly(reducedPoly)
    else:
        return reducedPoly

def GF_tables():
    exponential = []
    logarithm = [None]*256
    g = 0x03
    exponential.append(0x01)
    logarithm[exponential[-1]] = 0
    exponential.append(g)
    logarithm[exponential[-1]] = 1
    for i in range(2,255):
        exponential.append(GF_product_p(exponential[-1], g))
        logarithm[exponential[-1]] = i
    return exponential, logarithm
    
def GF_product_p(a, b):
    if (a == 0 or b == 0): return 0
    bb = asBinString(b)
    sumArray = [] 
    length = len(bb);
    for i in range(length):
        if (bb[length - 1 - i] == '1'):
            sumArray.append(a << i)
    resPoly = addPolyArrayXor(sumArray)
    return reducePoly(resPoly)
    
# http://www.cs.utsa.edu/~wagner/laws/FFM.html
def GF_product_t(a, b, exponentialCalc, logarithmCalc):
    if (a == 0 or b == 0): return 0
    expIndex = logarithmCalc[a] + logarithmCalc[b]
    if (expIndex >= 255): expIndex = expIndex - 255
    return exponentialCalc[expIndex]
        
def calcOrder(a, card):
    check = [False] * 256
    check[0] = True
    check[a] = True
    k = 1
    tmp = a
    while (tmp != 1 and k < card):
        tmp = GF_product_p(tmp, a)
        check[tmp] = True
        k = k + 1
    return k
         
def GF_generador():
    generators = []
    for i in range(1, 256):
        k = calcOrder(i, 256)
        if (k == 255):
            generators.append(i)
    return generators
        
def GF_invers(a, exponentialCalc, logarithmCalc):
    if (a == 0): return 0
    exp = logarithmCalc[a]
    invExp = (0xFF - exp) % 255
    return exponentialCalc[invExp]

def testInv(exponentialCalc, logarithmCalc):
    for i in range(1, 256):
        assert (GF_product_p(i, GF_invers(i, exponentialCalc, logarithmCalc)) == 1)
        

if __name__ == "__main__":
    exp, log = GF_tables()
    testInv(exp, log)
    print("Valid inv")
    gens = GF_generador()
    print(gens)