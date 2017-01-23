#!/usr/bin/env python
# -*- coding: utf-8 -*-
from library import *
import os

path = "./dataset/"
path,dirs,dataset = os.walk(path).next()
csvLocation = "./offlineData/"
#Color histogram Generator
while os.path.exists(csvLocation + "avgColor.csv"):
    option = raw_input("avgColor.csv existed, would you like to override it ? (Y/N)")
    print option
    if (option == "y" or option == "Y" ):
        os.remove(csvLocation + "avgColor.csv")
        for baseImgName in dataset:
            print("Processing   " + baseImgName + " in avgColor" )
            path = "./dataset/"
            query = Image.open(path + baseImgName)
            data = pandas.DataFrame(Convert(query, "avgColor"))
            with open(csvLocation + "avgColor.csv", "a") as saveLocation:
                data.to_csv(saveLocation, header=True, index_label=baseImgName)
        break
    elif (option == "n" or option == "N" ):
        break


# Color Layout Generator
while os.path.exists(csvLocation +  "ColorLayout.csv"):
    option = raw_input( "ColorLayout.csv existed, would you like to override it ? (Y/N)")
    print option
    if (option == "y" or option == "Y" ):
        os.path.exists(csvLocation + "Colorlayout.csv")
        for baseImgName in dataset:
            print("Processing   " + baseImgName + " in Color Layout")
            path = "./dataset/"
            query = Image.open(path + baseImgName)
            data = pandas.DataFrame(Convert(query, "ColorLayout"))
            with open(csvLocation + "ColorLayout.csv", "a") as saveLocation:
                data.to_csv(saveLocation, header=True, index_label=baseImgName)
        break
    elif (option == "n" or option == "N" ):
        break

