#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 24 17:25:38 2017

@author: alcasser
"""
from Crypto.Cipher import AES
import os
import subprocess
import hashlib
import myPkcs7
import re

p = re.compile('MPEG ADTS')

def read_file(file_name):
    with open(file_name, 'rb') as fo:
        ciphertext = fo.read()
    return ciphertext

def write_file(file_name, text):
    with open(file_name[:-4] + '.dec', 'wb') as fo:
        fo.write(text)
        
def decrypt_first(ciphertext, key):
    iv = ciphertext[:AES.block_size]
    cipher = AES.new(key, AES.MODE_OFB, iv)
    plaintext = cipher.decrypt(ciphertext[AES.block_size:])
    return plaintext

def decrypt_back(ciphertext):
    iv = ciphertext[:AES.block_size]
    plaintext = 0
    for i in range(0x10000):
        decKS = (iv + os.urandom(2))
        key = hashlib.sha256(decKS).digest()[0:16]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = cipher.decrypt(ciphertext[AES.block_size:])
        try:
            message = myPkcs7.decode(plaintext)
            write_file('test.enc', message)
            out = subprocess.run(['open', './test.dec'], stdout=subprocess.PIPE)
            print(out)
            print(i)
            if(plaintext[-1] == 16 and plaintext[-2] == 16):
                break;
        except Exception as ex:
            pass                
            
        

    
def decrypt_file(file_name, key):
    ciphertext = read_file(file_name)
    dec = decrypt_first(ciphertext, key)
    write_file(file_name, dec)

def decrypt_back_file(file_name):
    ciphertext = read_file(file_name)
    dec = decrypt_back(ciphertext)
    # write_file(file_name, dec)
        

if __name__ == '__main__':
    fk = open('./2017_09_26_13_22_04_albert.lopez.alcacer.key', 'rb')
    firstEncKey = fk.read()
    print('Key of first message: {}\n'.format(firstEncKey))
    decrypt_file('./2017_09_26_13_22_04_albert.lopez.alcacer.enc', firstEncKey)
    decrypt_back_file('./2017_09_26_13_22_04_albert.lopez.alcacer.puerta_trasera.enc')
    call(["ls", "-l"])