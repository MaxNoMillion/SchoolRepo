##########################################################################
## Name: Andrew Steen                                                   ##
## SWID: 102-68-080                                                     ##
## Date: Jan 10 2023                                                    ##
## Assignment #: 1                                                      ##
## Program Discription: In-Place 3D Transiformations in a Multi-Object  ##
##    Environment with Perspective Projection.                          ##
##########################################################################


import copy
import math
from tkinter import *

CanvasWidth = 400
CanvasHeight = 400
d = 500

DEBUG = True

class Object:
    def __init__(self, shape, size, coord):
        self.shape = shape
        self.coord = coord

        if size >= 0:
            self.size = size
        else:
            self.size = 0

        if shape == "pyrimid":
            apex = [coord[0], coord[1] + size, coord[2]]
            base1 = [coord[0] + size, coord[1] - size, coord[2] - size]
            base2 = [coord[0] - size, coord[1] - size, coord[2] - size]
            base3 = [coord[0] - size, coord[1] - size, coord[2] + size]
            base4 = [coord[0] + size, coord[1] - size, coord[2] + size]

            self.point_cloud = [apex, base1, base2, base3, base4]

            frontpoly = [apex,base1,base4]
            rightpoly = [apex,base2,base1]
            backpoly = [apex,base3,base2]
            leftpoly = [apex,base4,base3]
            bottompoly = [base1,base2,base3,base4]

            self.polies = [bottompoly, frontpoly, rightpoly, backpoly, leftpoly]



        if shape == "square":
            top1 = [coord[0] + size, coord[1] + size, coord[2] - size]
            top2 = [coord[0] + size, coord[1] + size, coord[2] + size]
            top3 = [coord[0] - size, coord[1] + size, coord[2] + size]
            top4 = [coord[0] - size, coord[1] + size, coord[2] - size]
            base1 = [coord[0] + size, coord[1] - size, coord[2] - size]
            base2 = [coord[0] + size, coord[1] - size, coord[2] + size]
            base3 = [coord[0] - size, coord[1] - size, coord[2] + size]
            base4 = [coord[0] - size, coord[1] - size, coord[2] - size]

            self.point_cloud = [top1, top2, top3, top4, base1, base2, base3, base4]

            bottompoly = [base1,base2,base3,base4]
            toppoly = [top1, top2, top3, top4]
            frontpoly = [top1, base1, base4, top4]
            backpoly = [top2, base2, base3, top3]
            rightpoly = [top2, base2, base1, top1]
            leftpoly = [top4, base4, base3, top3]

            self.polies = [bottompoly, toppoly, frontpoly, backpoly, rightpoly, leftpoly]




# ***************************** Initialize Pyramid Object ***************************
# Definition  of the five underlying points
# apex = [0,50,100]
# base1 = [50,-50,50]
# base2 = [50,-50,150]
# base3 = [-50,-50,150]
# base4 = [-50,-50,50]
top1 = [50,50,50]
top2 = [50,50,150]
top3 = [-50,50,150]
top4 = [-50,50,50]
base1 = [50,-50,50]
base2 = [50,-50,150]
base3 = [-50,-50,150]
base4 = [-50,-50,50]

# Definition of the five polygon faces using the meaningful point names
# Polys are defined in clockwise order when viewed from the outside
# frontpoly = [apex,base1,base4]
# rightpoly = [apex,base2,base1]
# backpoly = [apex,base3,base2]
# leftpoly = [apex,base4,base3]
# bottompoly = [base1,base2,base3,base4]
bottompoly = [base1,base2,base3,base4]
toppoly = [top1, top2, top3, top4]
frontpoly = [top1, base1, base4, top4]
backpoly = [top2, base2, base3, top3]
rightpoly = [top2, base2, base1, top1]
leftpoly = [top4, base4, base3, top3]


# Definition of the object
#Pyramid = [bottompoly, frontpoly, rightpoly, backpoly, leftpoly]
Square = [bottompoly, toppoly, frontpoly, backpoly, rightpoly, leftpoly]

# Definition of the Pyramid's underlying point cloud.  No structure, just the points.
# PyramidPointCloud = [apex, base1, base2, base3, base4]
# DefaultPyramidPointCloud = copy.deepcopy(PyramidPointCloud)
SquarePointCloud = [top1, top2, top3, top4, base1, base2, base3, base4]
DefaultSquarePointCloud = copy.deepcopy(SquarePointCloud)
#************************************************************************************

# This function resets the pyramid to its original size and location in 3D space
# Note that you have to be careful to update the values in the existing PyramidPointCloud
# structure rather than creating a new structure or just switching a pointer.  In other
# words, you'll need manually update the value of every x, y, and z of every point in
# point cloud (vertex list).
# def resetPyramid():
#     for i in range(len(PyramidPointCloud)):
#         for j in range(3):
#             PyramidPointCloud[i][j] = DefaultPyramidPointCloud[i][j]
def resetSquare():
    for i in range(len(SquarePointCloud)):
        for j in range(3):
            SquarePointCloud[i][j] = DefaultSquarePointCloud[i][j]

# This function translates an object by some displacement.  The displacement is a 3D
# vector so the amount of displacement in each dimension can vary.
def translate(object, displacement):
    ## Added displacement amounts per point of object cloud
    for point in object:
        point[0] = point[0] + displacement[0]
        point[1] = point[1] - displacement[1]
        point[2] = point[2] - displacement[2]
    
    if DEBUG:
        print(getVisualCenter(object))
    
# This function performs a simple uniform scale of an object assuming the object is
# centered at the origin.  The scalefactor is a scalar.
def scale(object, scalefactor):
    ## First We Must Record Original Location
    original_location = getVisualCenter(object)
    ## Then We Must Translated to 0,0,0 For in Place Scaling
    translateToOrigin(object, original_location)
    ## Multiplying scalefactor amount with points of object cloud
    for point in object:
        point[0] = point[0] * scalefactor
        point[1] = point[1] * scalefactor
        point[2] = point[2] * scalefactor
    ## Finally We Must Translate Back to Original Location
    translateBack(object, original_location)

    if DEBUG:
        print(getVisualCenter(object))

# This function performs a rotation of an object about the Z axis (from +X to +Y)
# by 'degrees', assuming the object is centered at the origin.  The rotation is CCW
# in a LHS when viewed from -Z [the location of the viewer in the standard postion]
def rotateZ(object,degrees):
    rads = math.radians(degrees)
    ## First We Must Record Original Location
    original_location = getVisualCenter(object)
    ## Then We Must Translated to 0,0,0 For in Place Scaling
    translateToOrigin(object, original_location)
    ## Then We Must Preform a Rotation on All Points
    for point in object:
        X, Y, Z = point[0], point[1], point[2]
        point[0] = X * math.cos(rads) - Y * math.sin(rads)
        point[1] = X * math.sin(rads) + Y * math.cos(rads)
        point[2] = Z
    ## Finally We Must Translate Back to Original Location
    translateBack(object, original_location)

    if DEBUG:
        print(getVisualCenter(object))
    
# This function performs a rotation of an object about the Y axis (from +Z to +X)
# by 'degrees', assuming the object is centered at the origin.  The rotation is CW
# in a LHS when viewed from +Y looking toward the origin.
def rotateY(object,degrees):
    rads = math.radians(degrees)
    ## First We Must Record Original Location
    original_location = getVisualCenter(object)
    ## Then We Must Translated to 0,0,0 For in Place Scaling
    translateToOrigin(object, original_location)
    ## Then We Must Preform a Rotation on All Points
    for point in object:
        X, Y, Z = point[0], point[1], point[2]
        point[0] = X * math.cos(rads) + Z * math.sin(rads)
        point[1] = Y
        point[2] = -X * math.sin(rads) + Z * math.cos(rads)
    ## Finally We Must Translate Back to Original Location
    translateBack(object, original_location)

    if DEBUG:
        print(getVisualCenter(object))

# This function performs a rotation of an object about the X axis (from +Y to +Z)
# by 'degrees', assuming the object is centered at the origin.  The rotation is CW
# in a LHS when viewed from +X looking toward the origin.
def rotateX(object,degrees):
    rads = math.radians(degrees)
    ## First We Must Record Original Location
    original_location = getVisualCenter(object)
    ## Then We Must Translated to 0,0,0 For in Place Scaling
    translateToOrigin(object, original_location)
    ## Then We Must Preform a Rotation on All Points
    for point in object:
        X, Y, Z = point[0], point[1], point[2]
        point[0] = X
        point[1] = Y * math.cos(rads) - Z * math.sin(rads)
        point[2] = Y * math.sin(rads) + Z * math.cos(rads)
    ## Finally We Must Translate Back to Original Location
    translateBack(object, original_location)

    if DEBUG:
        print(getVisualCenter(object))

# The function will draw an object by repeatedly callying drawPoly on each polygon in the object
def drawObject(object):
    ## Drawing Every Poly in Object
    for poly in object:
        drawPoly(poly)

# This function will draw a polygon by repeatedly callying drawLine on each pair of points
# making up the object.  Remember to draw a line between the last point and the first.
def drawPoly(poly):
    ## Drawing Every Line in Poly
    for i in range(-1, len(poly) - 1, 1):
        drawLine(poly[i], poly[i+1])

# Project the 3D endpoints to 2D point using a perspective projection implemented in 'project'
# Convert the projected endpoints to display coordinates via a call to 'convertToDisplayCoordinates'
# draw the actual line using the built-in create_line method
def drawLine(start,end):
    start_sp = []
    start_display = []
    end_sp = []
    end_display = []

    ## First We Must Convert Spacial Coords to Projected Coords ##
    ## And Then Convert From Prejected Coords to Display Coords ##
        # We must convert both start and end points
    start_sp = project(start)
    start_display = convertToDisplayCoordinates(start_sp)
    end_sp = project(end)
    end_display = convertToDisplayCoordinates(end_sp)
    w.create_line(start_display[0],start_display[1],end_display[0],end_display[1])

# This function converts from 3D to 2D (+ depth) using the perspective projection technique.  Note that it
# will return a NEW list of points.  We will not want to keep around the projected points in our object as
# they are only used in rendering
def project(point):
    ps = []
    ## Converting every deminsion of coord to projected point
    ps.append(d * (point[0] / (d + point[2])))
    ps.append(d * (point[1] / (d + point[2])))
    ps.append(d * (point[2] / (d + point[2])))
    ## Return coord of projected point
    return ps

# This function converts a 2D point to display coordinates in the tk system.  Note that it will return a
# NEW list of points.  We will not want to keep around the display coordinate points in our object as 
# they are only used in rendering.
def convertToDisplayCoordinates(point):
    displayXY = []
    ## Converting every deminsion of projected point coord into display coord
    displayXY.append(CanvasWidth/2 + point[0])
    displayXY.append(CanvasHeight/2 + point[1])
    ## Return coord of display point
    return displayXY


#### HELPER FUNCTIONS ####

# This functions translates object to origin with respect to its visual center.
def translateToOrigin(object, ori_pos):
    ## Then Translate All Points to New Center Location
    for point in object:
        X, Y, Z = point[0], point[1], point[2]
        point[0] = X - ori_pos[0]
        point[1] = Y - ori_pos[1]
        point[2] = Z - ori_pos[2]

# This function translates object back to original location
def translateBack(object, ori_pos):
    ## Translate All Points to Original Location
    for point in object:
        X, Y, Z = point[0], point[1], point[2]
        point[0] = X + ori_pos[0]
        point[1] = Y + ori_pos[1]
        point[2] = Z + ori_pos[2]

# This functions calculates visual center of object
def getVisualCenter(object):
    ## First We Must Find Visual Center ##
    # Getting bounds
    X_min, X_max, Y_min, Y_max, Z_min, Z_max = 0, 0, 0, 0, 0, 0
    for point in object:
        X, Y, Z = point[0], point[1], point[2]
        if X < X_min:
            X_min = X
        if X > X_max:
            X_max = X
        if Y < Y_min:
            Y_min = Y
        if Y > Y_max:
            Y_max = Y
        if Z < Z_min:
            Z_min = Z
        if Z > Z_max:
            Z_max = Z
    ## Using Max and Min Values to Calc Visual Center
    X_center = (X_max + X_min) / 2
    Y_center = (Y_max + Y_min) / 2
    Z_center = (Z_max + Z_min) / 2
    ## Returning Visual Center Coords
    return X_center, Y_center, Z_center


# **************************************************************************
# Everything below this point implements the interface
# def reset():
#     w.delete(ALL)
#     resetPyramid()
#     drawObject(Pyramid)

# def larger():
#     w.delete(ALL)
#     scale(PyramidPointCloud,1.1)
#     drawObject(Pyramid)

# def smaller():
#     w.delete(ALL)
#     scale(PyramidPointCloud,.9)
#     drawObject(Pyramid)

# def forward():
#     w.delete(ALL)
#     translate(PyramidPointCloud,[0,0,5])
#     drawObject(Pyramid)

# def backward():
#     w.delete(ALL)
#     translate(PyramidPointCloud,[0,0,-5])
#     drawObject(Pyramid)

# def left():
#     w.delete(ALL)
#     translate(PyramidPointCloud,[-5,0,0])
#     drawObject(Pyramid)

# def right():
#     w.delete(ALL)
#     translate(PyramidPointCloud,[5,0,0])
#     drawObject(Pyramid)

# def up():
#     w.delete(ALL)
#     translate(PyramidPointCloud,[0,5,0])
#     drawObject(Pyramid)

# def down():
#     w.delete(ALL)
#     translate(PyramidPointCloud,[0,-5,0])
#     drawObject(Pyramid)

# def xPlus():
#     w.delete(ALL)
#     rotateX(PyramidPointCloud,5)
#     drawObject(Pyramid)

# def xMinus():
#     w.delete(ALL)
#     rotateX(PyramidPointCloud,-5)
#     drawObject(Pyramid)

# def yPlus():
#     w.delete(ALL)
#     rotateY(PyramidPointCloud,5)
#     drawObject(Pyramid)

# def yMinus():
#     w.delete(ALL)
#     rotateY(PyramidPointCloud,-5)
#     drawObject(Pyramid)

# def zPlus():
#     w.delete(ALL)
#     rotateZ(PyramidPointCloud,5)
#     drawObject(Pyramid)

# def zMinus():
#     w.delete(ALL)
#     rotateZ(PyramidPointCloud,-5)
#     drawObject(Pyramid)

def reset():
    w.delete(ALL)
    resetSquare()
    drawObject(Square)

def larger():
    w.delete(ALL)
    scale(SquarePointCloud,1.1)
    drawObject(Square)

def smaller():
    w.delete(ALL)
    scale(SquarePointCloud,.9)
    drawObject(Square)

def forward():
    w.delete(ALL)
    translate(SquarePointCloud,[0,0,5])
    drawObject(Square)

def backward():
    w.delete(ALL)
    translate(SquarePointCloud,[0,0,-5])
    drawObject(Square)

def left():
    w.delete(ALL)
    translate(SquarePointCloud,[-5,0,0])
    drawObject(Square)

def right():
    w.delete(ALL)
    translate(SquarePointCloud,[5,0,0])
    drawObject(Square)

def up():
    w.delete(ALL)
    translate(SquarePointCloud,[0,5,0])
    drawObject(Square)

def down():
    w.delete(ALL)
    translate(SquarePointCloud,[0,-5,0])
    drawObject(Square)

def xPlus():
    w.delete(ALL)
    rotateX(SquarePointCloud,5)
    drawObject(Square)

def xMinus():
    w.delete(ALL)
    rotateX(SquarePointCloud,-5)
    drawObject(Square)

def yPlus():
    w.delete(ALL)
    rotateY(SquarePointCloud,5)
    drawObject(Square)

def yMinus():
    w.delete(ALL)
    rotateY(SquarePointCloud,-5)
    drawObject(Square)

def zPlus():
    w.delete(ALL)
    rotateZ(SquarePointCloud,5)
    drawObject(Square)

def zMinus():
    w.delete(ALL)
    rotateZ(SquarePointCloud,-5)
    drawObject(Square)


root = Tk()
outerframe = Frame(root)
outerframe.pack()

w = Canvas(outerframe, width=CanvasWidth, height=CanvasHeight)
# drawObject(Pyramid)
drawObject(Square)
w.pack()

controlpanel = Frame(outerframe)
controlpanel.pack()

resetcontrols = Frame(controlpanel, height=100, borderwidth=2, relief=RIDGE)
resetcontrols.pack(side=LEFT)

resetcontrolslabel = Label(resetcontrols, text="Reset")
resetcontrolslabel.pack()

resetButton = Button(resetcontrols, text="Reset", fg="green", command=reset)
resetButton.pack(side=LEFT)

scalecontrols = Frame(controlpanel, borderwidth=2, relief=RIDGE)
scalecontrols.pack(side=LEFT)

scalecontrolslabel = Label(scalecontrols, text="Scale")
scalecontrolslabel.pack()

largerButton = Button(scalecontrols, text="Larger", command=larger)
largerButton.pack(side=LEFT)

smallerButton = Button(scalecontrols, text="Smaller", command=smaller)
smallerButton.pack(side=LEFT)

translatecontrols = Frame(controlpanel, borderwidth=2, relief=RIDGE)
translatecontrols.pack(side=LEFT)

translatecontrolslabel = Label(translatecontrols, text="Translation")
translatecontrolslabel.pack()

forwardButton = Button(translatecontrols, text="FW", command=forward)
forwardButton.pack(side=LEFT)

backwardButton = Button(translatecontrols, text="BK", command=backward)
backwardButton.pack(side=LEFT)

leftButton = Button(translatecontrols, text="LF", command=left)
leftButton.pack(side=LEFT)

rightButton = Button(translatecontrols, text="RT", command=right)
rightButton.pack(side=LEFT)

upButton = Button(translatecontrols, text="UP", command=up)
upButton.pack(side=LEFT)

downButton = Button(translatecontrols, text="DN", command=down)
downButton.pack(side=LEFT)

rotationcontrols = Frame(controlpanel, borderwidth=2, relief=RIDGE)
rotationcontrols.pack(side=LEFT)

rotationcontrolslabel = Label(rotationcontrols, text="Rotation")
rotationcontrolslabel.pack()

xPlusButton = Button(rotationcontrols, text="X+", command=xPlus)
xPlusButton.pack(side=LEFT)

xMinusButton = Button(rotationcontrols, text="X-", command=xMinus)
xMinusButton.pack(side=LEFT)

yPlusButton = Button(rotationcontrols, text="Y+", command=yPlus)
yPlusButton.pack(side=LEFT)

yMinusButton = Button(rotationcontrols, text="Y-", command=yMinus)
yMinusButton.pack(side=LEFT)

zPlusButton = Button(rotationcontrols, text="Z+", command=zPlus)
zPlusButton.pack(side=LEFT)

zMinusButton = Button(rotationcontrols, text="Z-", command=zMinus)
zMinusButton.pack(side=LEFT)

root.mainloop()