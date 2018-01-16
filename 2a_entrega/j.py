#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 22:00:43 2017

@author: alcasser
"""

finalGrades = [-3, -3, 10, 2, 10, 0, 7, 7, 12, -3, 7, 0, 12, 12, 12 ,12, 12, 0, 0, 0, 4]
possibleGrades = [-3, 0, 2, 4, 7, 10, 12]
fin = [ possibleGrades.index(i) for i in finalGrades]
plt.hist(fin, bins=range(8), align="left")
plt.xticks(range(7), possibleGrades)

plt.title("Final Grades plot")
plt.xlabel("All possible grades")
plt.ylabel("Number of students")
plt.show()
print(bin(0x1597C4EF331CC28B7E6D1B2EB3EA3B95)[2:])