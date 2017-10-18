#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 15 19:30:57 2017

@author: alcasser
"""

import GFHelpers as gf


a = 0xFF
b = 0xFF
exponential, logarithm = gf.GF_tables()
gf.testInv(exponential, logarithm)
print('Product using multiplication: {}'.format(gf.GF_product_p(a,b)))
print('Product using tables: {}'.format(gf.GF_product_t(a,b, exponential, logarithm)))
g = gf.GF_generador()
print('Generators of GF(256): {}'.format(g))
inva = gf.GF_invers(a, exponential, logarithm)
one = gf.GF_product_p(inva, a)
gens = gf.GF_generador()   
