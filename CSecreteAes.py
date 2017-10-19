#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 15 19:30:57 2017

@author: alcasser
"""

import GFHelpers as gf
import aes
import time

def asHexMatrix(cypher):
    matrix = [[0 for i in range(4)] for j in range(4)]
    chex = hex(cypher)
    for i in range(4):
        for j in range(4):
            index = (i * 4 + j) * 2 + 2
            matrix[j][i] = chex[index:index+2]
    return matrix
        
class AesWoByteSub(aes.AES):
    def _AES__sub_bytes(self, s):
        pass

class AesWoShiftRows(aes.AES):
    def _AES__shift_rows(self, s):
        pass
        

def ByteSubEffectTest():
    aes = AesWoByteSub(master_key)
    m = 0x1597C4EF331CC28B7E6D1B2EB3EA3B95
    c = aes.encrypt(m)
    for i in range(128):
        for j in range(128):
            if (i != j):
                ci = aes.encrypt(m ^ (1 << i))
                cj = aes.encrypt(m ^ (1 << j))
                cij = aes.encrypt(m ^ (1 << i ^ 1 << j))
                print(hex(cij), end="\r", flush=True)
                assert(c == ci ^ cj ^ cij)
    print("Byte substitution effect tested   ", flush=True)
    



if __name__ == "__main__":
    master_key = 0x2b7e151628aed2a6abf7158809cf4f3c
    aes = AesWoByteSub(master_key)
    plaintext = 0x3243f6a8885a308d313198a2e0370734
    encrypted = aes.encrypt(plaintext)
    plaintextDec = aes.decrypt(encrypted)
    
    m = 0x1597C4EF331CC28B7E6D1B2EB3EA3B95
    mi = 0x1597C4EF331C828B7E6D1B2EB3EA3B95
    mj = 0x1597C4EF331CC28B7E6D1B2E93EA3B95
    mij = 0x1597C4EF331C828B7E6D1B2E93EA3B95
    
    c = aes.encrypt(m)
    ci = aes.encrypt(mi)
    cj = aes.encrypt(mj)
    cij = aes.encrypt(mij)
    cc = ci ^ cj ^ cij
    
    ByteSubEffectTest()
    m = asHexMatrix(0x1597C4EF331CC28B7E6D1B2EB3EA3B95)