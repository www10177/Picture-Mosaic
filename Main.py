#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from library import *
from Tkinter import *
import tkFileDialog
from ttk import *
from PIL import Image
import csv
#Variables
csvFileLocation = "./offlineData/"
datasetLocation = "./dataset/"
#GUI
class GUI(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.parent = parent

        self.initUI()

    def initUI(self):
        self.parent.title("Picture Mosaic")

        self.pack(fill=BOTH, expand=1)


        self.fileName = StringVar(value="./sample.jpg")
        self.saveName = StringVar(value="./sample-Mosaic.jpg")
        self.col = StringVar(value="50")
        self.row = StringVar(value="50")
        #vcmd to check let entry only can input number
        vcmd = (self.register(self.validate),
                '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

        #init materials
        Button(self, text="Open ...", command=openFile).grid(row=0, column=0, pady=5)
        Label(self, textvariable=self.fileName).grid(row=0, column=1, columnspan=10, pady=5, sticky=W)

        Button(self, text="Save ...", command=saveAs).grid(row=1, column=0, pady=5)
        Label(self, textvariable=self.saveName).grid(row=1,column = 1,columnspan=10, pady=5, sticky=W)

        mode = StringVar(self)
        mode.set("Average Color")
        Label(self, text="Select Mode: ").grid(row=2, column=0,sticky=W)
        om = OptionMenu(self, mode, "","Average Color","Color Layout")
        om.grid(row=2, column=1, sticky=W)

        Label(self, text="Partition Size : ").grid(row=2, column=2,padx=10, sticky=W)
        self.colE =Entry(self,textvariable = self.col,width = 4, validate = 'key', validatecommand = vcmd)
        self.colE.grid(row=2, column=3, pady = 1 ,sticky = W)
        Label(self, text="x").grid(row=2, column=3,padx=45,sticky=W+E)
        self.rowE = Entry(self,textvariable = self.row,width = 4, validate = 'key', validatecommand = vcmd)
        self.rowE.grid(row=2, column=3,sticky=W,padx=70)

        Button(self,text="Show Picture",command=lambda:openPic(self.saveName.get())).grid(row=4,column=1,pady=5)


        Button(self, text="Run", command=lambda:
        Mosaic(self.fileName.get(), mode.get(),self.saveName.get(),int(self.rowE.get()),int(self.colE.get())))\
            .grid(row=4,column=0,pady=5)

    def validate(self, action, index, value_if_allowed,prior_value, text, validation_type, trigger_type, widget_name):
        if text in '0123456789':
            return True
        else:
            return False
def openPic(saveName):
    im = Image.open(saveName)
    im.show()
def saveAs():
    #initName=app.fileName.get()[0:-4]+"-Mosaic.jpg"
    initName = "Mosaic.jpg"
    saveName = tkFileDialog.asksaveasfile(initialdir = "./",filetypes=[("Image","*.jpg")],initialfile=initName)
    app.saveName.set(saveName.name)
def openFile ():
    fileName = tkFileDialog.askopenfilename(initialdir = "./")
    app.fileName.set(fileName)

#GUI END
#Main Operation

def avgColorCal(query,data):
    qAvg = Convert(query,"avgColor")
    distance = sys.float_info.max
    nearest = data[0][0]
    for i  in xrange(0,len(data),4):
        temp = 0
        for y in xrange(1,4):
            temp += pow(float(data[i+y][1])-qAvg[y-1],2)
        temp = sqrt(temp)
        if temp < distance:
            nearest = data[i][0]
            distance = temp
    return nearest
def ColorLayoutCal(query,data):
    qColor = Convert(query,"ColorLayout")
    distance = sys.float_info.max
    nearest = data[0][0]
    for i in xrange(0, len(data), 4):
        temp = 0
        for y in xrange(1, 4):
            localTemp=0
            for z in xrange(1, 64):
                localTemp += pow(abs(float(data[i+y][z])-qColor[y-1][z-1]),2)
            temp += sqrt(localTemp)
        if temp < distance:
            nearest = data[i][0]
            distance = temp
    return nearest
def Mosaic(filename,mode,saveName,row,col):
    query = Image.open(filename)
    width, height = query.size
    if(mode == "Average Color"):
        getNearest=avgColorCal
        csvName='avgColor.csv'
    elif mode == 'Color Layout':
        getNearest=ColorLayoutCal
        csvName='ColorLayout.csv'
    with open(csvFileLocation + csvName, "r") as _csv:
        data = csv.reader(_csv)
        data = [r for r in data]
        boxH = height / row
        boxW = width / col
        box = (0, 0, boxW, boxH)
        dataSetSize = Image.open(datasetLocation + "ukbench00000.jpg").size
        resultIm = Image.new("RGB", (boxW*col,boxH*row))
        for i in xrange(row):
            for j in xrange(col):
                piece = query.crop(box)
                nearest = getNearest(piece, data)
                newIm = Image.open(datasetLocation + nearest)
                newIm = newIm.resize((boxW, boxH))
                reSize = (i * dataSetSize[0], j * dataSetSize[1], (i + 1) * dataSetSize[0], (j + 1) * dataSetSize[1])
                resultIm.paste(newIm, box)
                box = (box[0] + boxW, box[1], box[2] + boxW, box[3])
                print str(i) + "   " + str(j) + "         " + nearest
            box = (0, box[1] + boxH, boxW, box[3] + boxH)
    resultIm.save(saveName, "JPEG", quality=80, optimize=True, progressive=True)
    openPic(saveName)


if __name__ == '__main__':
    root = Tk()
    size = 220, 220
    app = GUI(root)
    root.geometry("600x150")
    root.resizable(0,0)
    root.mainloop()

