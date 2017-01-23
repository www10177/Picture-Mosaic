#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import pandas
from PIL import Image
from pylab import *
from scipy.fftpack import dct
import sys


def zigzagIndex(n):
    def move(i, j):
        if j < (n - 1):
            return max(0, i - 1), j + 1
        else:
            return i + 1, j

    a = [[0] * n for _ in xrange(n)]
    x, y = 0, 0
    for v in xrange(n * n):
        a[y][x] = v
        if (x + y) & 1:
            x, y = move(x, y)
        else:
            y, x = move(y, x)
    return a

def zigzag(list):
    back = [[ 0 for _ in xrange(8 * 8)]for _ in xrange(3)]
    for x in xrange(3):
        index = zigzagIndex(8)
        for i in xrange(8):
            for j in xrange(8):
                 back[x][index[i][j]] = list[x][i][j]
    return back

def Convert (query, mode):
    if(query.mode != "RGB"):
        query = query.convert("RGB")
    if mode == "avgColor":
        width,height = query.size
        pixel = query.load()
        Avg = [0,0,0]

        for i in xrange(width):
            for j in xrange(height):
                R,G,B = pixel[i,j]
                Avg[0] += R
                Avg[1] += G
                Avg[2]+= B

        pixelAmount = width * height

        for x in xrange(len(Avg)):
            Avg[x]/= pixelAmount

        return Avg


    if mode == "ColorLayout":
        width,height = query.size
        partitionW = width / 8
        partitionH = height / 8
        partitionImR =  [[0 for i in xrange(8)] for j in xrange(8)]
        partitionImG = [[0 for i in xrange(8)] for j in xrange(8)]
        partitionImB = [[0 for i in xrange(8)] for j in xrange(8)]
        pixel = query.load()
        for x in xrange(width):
            for y in xrange(height):
                xIndex = x/partitionW
                yIndex = y/partitionH
                if(xIndex < 8 and yIndex < 8):
                    partitionImR[xIndex][yIndex] += pixel[x,y][0]
                    partitionImG[xIndex][yIndex] += pixel[x,y][1]
                    partitionImB[xIndex][yIndex] += pixel[x,y][2]
        divisor = partitionH*partitionW
        for x in xrange(8):
            for y in xrange(8):
                partitionImR[x][y] /= divisor
                partitionImG[x][y] /= divisor
                partitionImB[x][y] /= divisor
        ImDct = [0 for x in xrange(3)]
        ImDct[0] = dct(partitionImR)
        ImDct[1] = dct(partitionImG)
        ImDct[2] = dct(partitionImB)
        FinalList = zigzag(ImDct)
        return FinalList


