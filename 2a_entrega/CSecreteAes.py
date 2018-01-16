#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 15 19:30:57 2017

@author: alcasser
"""

import aes

master_key = 0x2b7e151628aed2a6abf7158809cf4f3c

def asHexMatrix(cypher):
    matrix = [[0 for i in range(4)] for j in range(4)]
    chex = hex(cypher)
    for i in range(4):
        for j in range(4):
            index = (i * 4 + j) * 2 + 2
            matrix[j][i] = chex[index:index+2]
    return matrix

def printMatrix(aMatrix):
    for i in range(len(aMatrix)):
        print(aMatrix[i])

class AesWoByteSub(aes.AES):
    def _AES__sub_bytes(self, s):
        pass

class AesWoShiftRows(aes.AES):
    def _AES__shift_rows(self, s):
        pass

class AesWoMixColumns(aes.AES):
    def _AES__mix_columns(self, s):
        pass

def byteSubEffectTest():
    aes = AesWoByteSub(master_key)
    m = 0x1597C4EF331CC28B7E6D1B2EB3EA3B95
    c = aes.encrypt(m)
    print("Byte substitution effect in progress...")
    for i in range(128):
        for j in range(128):
            if (i != j):
                ci = aes.encrypt(m ^ (1 << i))
                cj = aes.encrypt(m ^ (1 << j))
                cij = aes.encrypt(m ^ (1 << i ^ 1 << j))
                #print(hex(cij), end="\r", flush=True)
                assert(c == ci ^ cj ^ cij)
    print("Byte substitution effect tested   ", flush=True)
    
def shiftRowsEffectTest():
    aes = AesWoShiftRows(master_key)
    m = 0x1597C4EF331CC28B7E6D1B2EB3EA3B95
    c = aes.encrypt(m)
    hexC = hex(c)
    for i in range(4):
        mi = m ^ (1 << i * 32)
        ci = aes.encrypt(mi)
        hexCi = hex(ci)
        a = 8 * (3 - i) + 2
        # accedir a la columna que varia
        # +2 per eliminar el 0x
        b = a + 8
        print("Only columns: {} and {} different".format(hexC[a:b],
              hexCi[a:b]))
        printMatrix(asHexMatrix(c))
        print("")
        printMatrix(asHexMatrix(ci))
        print("")
    
def mixColumnsEffectTest():
    aes = AesWoMixColumns(master_key)
    m = 0x1597C4EF331CC28B7E6D1B2EB3EA3B95
    c = aes.encrypt(m)
    for i in range(4):
        mi = m ^ (1 << i * 32)
        ci = aes.encrypt(mi)
        print("Only one byte modified")
        printMatrix(asHexMatrix(c))
        print("")
        printMatrix(asHexMatrix(ci))
        print("")

if __name__ == "__main__":
    byteSubEffectTest()
    # shiftRowsEffectTest()
    # mixColumnsEffectTest()