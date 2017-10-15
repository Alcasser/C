#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 15 19:30:57 2017

@author: alcasser
"""

import GFHelpers



def main():
    a = 0xFF
    b = 0xFF
    exponential, logarithm = GFHelpers.GF_tables()
    GFHelpers.testInv(exponential, logarithm)
    print('Product using multiplication: {}'.format(GFHelpers.GF_product_p(a,b)))
    print('Product using tables: {}'.format(GFHelpers.GF_product_t(a,b, exponential, logarithm)))
    g, failResult = GFHelpers.GF_generador()
    print('Generators of GF(256): {}'.format(g))
    inva = GFHelpers.GF_invers(a, exponential, logarithm)
    one = GFHelpers.GF_product_p(inva, a)


if __name__ == "__main__":
    main()    
