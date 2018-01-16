#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 14 11:27:19 2018

@author: alcasser
"""

import hashlib

def read(file_name):
    with open(file_name, 'rb') as fo:
        return fo.read()

def verify(s_signature, m):
    p = 115792089210356248762697446949407573530086143415290314195533631308867097853951
    len_f1 = int(s_signature[3])
    print('Length of f1: {}'.format(len_f1))
    f1f2 = s_signature[4:]
    f1 = f1f2[:len_f1]
    len_f2 = int(f1f2[len_f1 + 1])
    print('Length of f2: {}'.format(len_f2))
    f2 = f1f2[len_f1 + 2:]
    
    #print(f2)
    inv_mod = 1
    #f2_i = inverse_mod(f2, p)
    #w1 = m * f2_i
    #w2 = f1 * f2_i
    
    
    # print(f1.hex())
    # print(f2.hex())
    
def main():
    s_signature = read('./server_signature.bin')
    
    random_client = read('./random_client.bin')
    random_server = read('./random_server.bin')
    curve_type = read('./server_curve_type.bin')
    named_curve = read('./server_named_curve.bin')
    pubkey_len = read('./server_pubkey_len.bin')
    pubkey = read('./server_pubkey.bin')
    
    m = hashlib.sha512(random_client + random_server + curve_type + \
                           named_curve + pubkey_len + pubkey).hexdigest()
    m = m[:64]
    verify(s_signature, m)
    
    print(pubkey.hex())
    
if __name__ == "__main__":
    main()