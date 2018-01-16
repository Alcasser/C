#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 18:36:23 2017

@author: alcasser
"""

from Crypto.PublicKey import RSA
from Crypto.PublicKey.RSA import importKey
from math import gcd
from glob import glob


n = 25747548551694293442855127134507413839409760174426694340687906994315509868115948986472859343852141088119082418000653756880246181799442129897249018288615522880241723820673498084394582984667505015101496926221902584286921942833076158207013384371112952747040886614261710028603133862046494740372272362683728741797679853669464636738016563031657070715497560685330070280121885111384164060665239899689520825604041357942894282821596681352542026663294646933565034034752158140293605018863484101953727846700929176507137420356167169371491364907682752782587976306685048348346679214900983030767267634869313982553661426520937059176269
e = 65537

'''
https://news.ycombinator.com/item?id=3591429
Posting what I said in the other thread: As far as I can tell, this is what they're doing: if two different keys have a factor in common (i.e. A=PQ, B=PR), then you
can use Euclid's algorithm (which just requires repeated subtraction, and is thus really easy) to find P (=gcd(A,B)), and then just use division to find Q (=A/P) and R (=B/P) easily.
So what the researchers did, apparently, was to gather all the RSA public keys they could find (6 million or so) and then calculate the gcds of all pairs of keys.
Whenever they found a gcd that wasn't equal to 1, they'd cracked (at least) 2 keys.
'''

for filename in glob('*pubkeyRSA_RW*.pem'):
    f = open(filename)
    key = importKey(f.read())
    if gcd(n, key.n) != 1:
        print (f.name)
        print ("key.n = " + str(key.n))
        p = gcd(n, key.n)
        break
        
print ("p = " + str(p))
d = int(input('d = '))
privateKey = RSA.construct((n,e,d))
f = open('priv_key_rw.pem', 'wb')
f.write(privateKey.exportKey('PEM'))
f.close
print("The private key has been generated")
