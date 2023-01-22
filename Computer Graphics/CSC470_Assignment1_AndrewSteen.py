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

# Debug Toggle
DEBUG = False

# Object class to make adding shapes easier
class Object:
    ## Contains All Objects in Scene
    all_objects = []

    ## Constructor for Object Class
    def __init__(self, point_cloud, shape):
        self.point_cloud = point_cloud
        self.default_point_cloud = copy.deepcopy(point_cloud)       # Making deepCopy for resetting
        self.temp_visual_center = []                                # For inPlace rotation and scaling
        self.shape = shape
        self.isSelected = False
        Object.all_objects.append(self)                             # Adds objects to list

    # This class function draws all objects
    def drawAllObjects():
        # Calls drawObject function on each object in all_objects
        for object in Object.all_objects:
            object.drawObject()

    # This class function will draw an object by repeatedly callying drawPoly on each polygon in the object
    def drawObject(self):
        ## Draws each polygon of object
        for poly in self.shape:
            self.drawPoly(poly)

    # This class function will draw a polygon by repeatedly callying drawLine on each pair of points
    # making up the object.  Remember to draw a line between the last point and the first.
    def drawPoly(self, poly):
        ## Drawing Every Line in Poly
        for i in range(-1, len(poly) - 1, 1):
            self.drawLine(poly[i], poly[i+1])

    # Project the 3D endpoints to 2D point using a perspective projection implemented in 'project'
    # Convert the projected endpoints to display coordinates via a call to 'convertToDisplayCoordinates'
    # draw the actual line using the built-in create_line method
    def drawLine(self, start,end):
        # Initiallize coord vectors
        start_sp = []
        start_display = []
        end_sp = []
        end_display = []
        ## First We Must Convert Spacial Coords to Projected Coords ##
        ## And Then Convert From Prejected Coords to Display Coords ##
            # We must convert both start and end points
        start_sp = Object.project(start)
        start_display = Object.convertToDisplayCoordinates(start_sp)
        end_sp = Object.project(end)
        end_display = Object.convertToDisplayCoordinates(end_sp)
        # Tkinter function to draw line on window
        if (self.isSelected):
            w.create_line(start_display[0],start_display[1],end_display[0],end_display[1], fill='red')
        else:
            w.create_line(start_display[0],start_display[1],end_display[0],end_display[1])

    # This class function converts from 3D to 2D (+ depth) using the perspective projection technique.  Note that it
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
        displayXY.append(CanvasHeight/2 - point[1])
        ## Return coord of display point
        return displayXY

    # This class function resets object to its original position
    def resetObject(self):
        # Resets all points of object to original location
        for i in range (len(self.point_cloud)):
            for j in range(3):
                self.point_cloud[i][j] = self.default_point_cloud[i][j]

    # This class function resets entire scene
    def resetScene():
        # Calls resetObject function on each object in all_objects
        for object in Object.all_objects:
            object.resetObject()

    # This class functions calculates visual center of object
    def getVisualCenter(self):
        ## First We Must Find Visual Center ##
        # Initiallizing min and max values
        X_min, X_max, Y_min, Y_max, Z_min, Z_max = float('inf'), float('-inf'), float('inf'), float('-inf'), float('inf'), float('-inf')
        # Looping through points in the objects' point clouds
        for point in self.point_cloud:
            # Decoupling
            X, Y, Z = point[0], point[1], point[2]
            if X < X_min:       # Getting min X
                X_min = X
            if X > X_max:       # Getting max X
                X_max = X
            if Y < Y_min:       # Getting min Y
                Y_min = Y
            if Y > Y_max:       # Getting max Y
                Y_max = Y
            if Z < Z_min:       # Getting min Z
                Z_min = Z
            if Z > Z_max:       # Getting max Z
                Z_max = Z
        ## Using Max and Min Values to Calc Visual Center
        X_center = (X_max + X_min) / 2
        Y_center = (Y_max + Y_min) / 2
        Z_center = (Z_max + Z_min) / 2
        ## Returning Visual Center Coords
        return X_center, Y_center, Z_center

    # This functions translates object to origin with respect to its visual center.
    def translateToOrigin(self):
        # Saves current visual center into temp var
        self.temp_visual_center = self.getVisualCenter()
        ref = self.temp_visual_center   # Set to ref to ease the mind
        ## Then Translate All Points to New Center Location
        for point in self.point_cloud:
            X, Y, Z = point[0], point[1], point[2]
            point[0] = X - ref[0]
            point[1] = Y - ref[1]
            point[2] = Z - ref[2]

    # This function translates object back to original location
    def translateBack(self):
        # Setting ref to previous visual center
        ref = self.temp_visual_center
        ## Translate All Points to Original Location
        for point in self.point_cloud:
            X, Y, Z = point[0], point[1], point[2]
            point[0] = X + ref[0]
            point[1] = Y + ref[1]
            point[2] = Z + ref[2]

    # This class function translates an object by some displacement.  The displacement is a 3D
    # vector so the amount of displacement in each dimension can vary.
    def translate(self, displacement):
        ## Added displacement amounts per point of object cloud
        for point in self.point_cloud:
            X, Y, Z = point[0], point[1], point[2]
            point[0] = X + displacement[0]
            point[1] = Y + displacement[1]
            point[2] = Z - displacement[2]
        # DEBUG print object location
        if DEBUG:
            print(self.getVisualCenter())

    # This function performs a simple uniform scale of an object assuming the object is
    # centered at the origin.  The scalefactor is a scalar.
    def scale(self, scalefactor):
        ## Then We Must Translated to 0,0,0 For in Place Scaling
        self.translateToOrigin()
        #print(self.getVisualCenter())
        ## Multiplying scalefactor amount with points of object cloud
        for point in self.point_cloud:
            point[0] = point[0] * scalefactor
            point[1] = point[1] * scalefactor
            point[2] = point[2] * scalefactor
        ## Finally We Must Translate Back to Original Location
        self.translateBack()
        # DEBUG print object location
        if DEBUG:
            print(self.getVisualCenter())

    # This function performs a rotation of an object about the Z axis (from +X to +Y)
    # by 'degrees', assuming the object is centered at the origin.  The rotation is CCW
    # in a LHS when viewed from -Z [the location of the viewer in the standard postion]
    def rotateZ(self, degrees):
        rads = float(math.radians(float(degrees)))
        ## Then We Must Translated to 0,0,0 For in Place Scaling
        self.translateToOrigin()
        ## Then We Must Preform a Rotation on All Points
        for point in self.point_cloud:
            X, Y, Z = point[0], point[1], point[2]
            point[0] = X * math.cos(rads) - Y * math.sin(rads)
            point[1] = X * math.sin(rads) + Y * math.cos(rads)
            point[2] = Z
        ## Finally We Must Translate Back to Original Location
        self.translateBack()
        # DEBUG print object location
        if DEBUG:
            print(self.getVisualCenter())

    # This function performs a rotation of an object about the Y axis (from +Z to +X)
    # by 'degrees', assuming the object is centered at the origin.  The rotation is CW
    # in a LHS when viewed from +Y looking toward the origin.
    def rotateY(self, degrees):
        rads = float(math.radians(float(degrees)))
        ## Then We Must Translated to 0,0,0 For in Place Scaling
        self.translateToOrigin()
        ## Then We Must Preform a Rotation on All Points
        for point in self.point_cloud:
            X, Y, Z = point[0], point[1], point[2]
            point[0] = X * math.cos(rads) + Z * math.sin(rads)
            point[1] = Y
            point[2] = -X * math.sin(rads) + Z * math.cos(rads)
        ## Finally We Must Translate Back to Original Location
        self.translateBack()
        # DEBUG print object location
        if DEBUG:
            print(self.getVisualCenter())

    # This function performs a rotation of an object about the X axis (from +Y to +Z)
    # by 'degrees', assuming the object is centered at the origin.  The rotation is CW
    # in a LHS when viewed from +X looking toward the origin.
    def rotateX(self, degrees):
        rads = float(math.radians(float(degrees)))
        ## Then We Must Translated to 0,0,0 For in Place Scaling
        self.translateToOrigin()
        ## Then We Must Preform a Rotation on All Points
        for point in self.point_cloud:
            X, Y, Z = point[0], point[1], point[2]
            point[0] = X
            point[1] = Y * math.cos(rads) - Z * math.sin(rads)
            point[2] = Y * math.sin(rads) + Z * math.cos(rads)
        ## Finally We Must Translate Back to Original Location
        self.translateBack()
        # DEBUG print object location
        if DEBUG:
            print(self.getVisualCenter())


# ***************************** Initialize Objects ***************************
# Definition of the underlying points
## Pyramid
py_apex = [0,50,100]
py_base1 = [50,-50,50]
py_base2 = [50,-50,150]
py_base3 = [-50,-50,150]
py_base4 = [-50,-50,50]
# Square0
sq_top0_1 = [-100,50,50]
sq_top0_2 = [-100,50,150]
sq_top0_3 = [-200,50,150]
sq_top0_4 = [-200,50,50]
sq_base0_1 = [-100,-50,50]
sq_base0_2 = [-100,-50,150]
sq_base0_3 = [-200,-50,150]
sq_base0_4 = [-200,-50,50]
# Square1
sq_top1_1 = [200,50,50]
sq_top1_2 = [200,50,150]
sq_top1_3 = [100,50,150]
sq_top1_4 = [100,50,50]
sq_base1_1 = [200,-50,50]
sq_base1_2 = [200,-50,150]
sq_base1_3 = [100,-50,150]
sq_base1_4 = [100,-50,50]

# Definition of polygon faces using the meaningful point names
# Polys are defined in clockwise order when viewed from the outside
# Pyramid
py_frontpoly = [py_apex, py_base1, py_base4]
py_rightpoly = [py_apex, py_base2, py_base1]
py_backpoly = [py_apex, py_base3, py_base2]
py_leftpoly = [py_apex, py_base4, py_base3]
py_bottompoly = [py_base1, py_base2, py_base3, py_base4]
# Square0
sq_bottompoly0 = [sq_base0_1, sq_base0_2, sq_base0_3, sq_base0_4]
sq_toppoly0 = [sq_top0_1, sq_top0_2, sq_top0_3, sq_top0_4]
sq_frontpoly0 = [sq_top0_1, sq_base0_1, sq_base0_4, sq_top0_4]
sq_backpoly0 = [sq_top0_2, sq_base0_2, sq_base0_3, sq_top0_3]
sq_rightpoly0 = [sq_top0_2, sq_base0_2, sq_base0_1, sq_top0_1]
sq_leftpoly0 = [sq_top0_4, sq_base0_4, sq_base0_3, sq_top0_3]
# Square1
sq_bottompoly1 = [sq_base1_1, sq_base1_2, sq_base1_3, sq_base1_4]
sq_toppoly1 = [sq_top1_1, sq_top1_2, sq_top1_3, sq_top1_4]
sq_frontpoly1 = [sq_top1_1, sq_base1_1, sq_base1_4, sq_top1_4]
sq_backpoly1 = [sq_top1_2, sq_base1_2, sq_base1_3, sq_top1_3]
sq_rightpoly1 = [sq_top1_2, sq_base1_2, sq_base1_1, sq_top1_1]
sq_leftpoly1 = [sq_top1_4, sq_base1_4, sq_base1_3, sq_top1_3]


# Definition of the objects
pyramid = [py_bottompoly, py_frontpoly, py_rightpoly, py_backpoly, py_leftpoly]
square0 = [sq_bottompoly0, sq_toppoly0, sq_frontpoly0, sq_backpoly0, sq_rightpoly0, sq_leftpoly0]
square1 = [sq_bottompoly1, sq_toppoly1, sq_frontpoly1, sq_backpoly1, sq_rightpoly1, sq_leftpoly1]

# Definition of the objects' underlying point cloud.  No structure, just the points.
pyramid_point_cloud = [py_apex, py_base1, py_base2, py_base3, py_base4]
square0_point_cloud = [sq_top0_1, sq_top0_2, sq_top0_3, sq_top0_4, sq_base0_1, sq_base0_2, sq_base0_3, sq_base0_4]
square1_point_cloud = [sq_top1_1, sq_top1_2, sq_top1_3, sq_top1_4, sq_base1_1, sq_base1_2, sq_base1_3, sq_base1_4]

# Creating Object object
Pyramid = Object(pyramid_point_cloud, pyramid)
Square0 = Object(square0_point_cloud, square0)
Square1 = Object(square1_point_cloud, square1)

#************************************************************************************

#### OBJECT SELECTOR ####
# Starting Object
object = Square0
curr = 1    # curr object index
# This function is used to select an object with the arrow keys.
def selector(direction):
    # Calling Global Vars
    global object
    global curr
    # For selection detection (Color)
    object.isSelected = False
    # Adding or Subtracting from Index Depending on Arrow Direction
    curr += direction
    # Modulo to Allow Object Selection Cycling
    curr %= len(Object.all_objects)
    # Sets "object" to selector object in object list
    object = Object.all_objects[curr]
    # For selection detection (Color)
    object.isSelected = True
    # Redraw objects
    Object.drawAllObjects()

# Detects Keys and Changes Selector
def left_key(event):
    selector(1)
def right_key(event):
    selector(-1)

# **************************************************************************
# Everything below this point implements the interface
def reset():
    w.delete(ALL)
    Object.resetScene()
    Object.drawAllObjects()

def larger():
    w.delete(ALL)
    object.scale(1.1)
    Object.drawAllObjects()

def smaller():
    w.delete(ALL)
    object.scale(0.9)
    Object.drawAllObjects()

def forward():
    w.delete(ALL)
    object.translate([0,0,5])
    Object.drawAllObjects()

def backward():
    w.delete(ALL)
    object.translate([0,0,-5])
    Object.drawAllObjects()

def left():
    w.delete(ALL)
    object.translate([-5,0,0])
    Object.drawAllObjects()

def right():
    w.delete(ALL)
    object.translate([5,0,0])
    Object.drawAllObjects()

def up():
    w.delete(ALL)
    object.translate([0,5,0])
    Object.drawAllObjects()

def down():
    w.delete(ALL)
    object.translate([0,-5,0])
    Object.drawAllObjects()

def xPlus():
    w.delete(ALL)
    object.rotateX(5)
    Object.drawAllObjects()

def xMinus():
    w.delete(ALL)
    object.rotateX(-5)
    Object.drawAllObjects()

def yPlus():
    w.delete(ALL)
    object.rotateY(5)
    Object.drawAllObjects()

def yMinus():
    w.delete(ALL)
    object.rotateY(-5)
    Object.drawAllObjects()

def zPlus():
    w.delete(ALL)
    object.rotateZ(5)
    Object.drawAllObjects()

def zMinus():
    w.delete(ALL)
    object.rotateZ(-5)
    Object.drawAllObjects()

#*******************************************************************************#
object.isSelected = True
root = Tk()
outerframe = Frame(root)
outerframe.pack()

root.bind("<Right>", right_key)
root.bind("<Left>", left_key)
w = Canvas(outerframe, width=CanvasWidth, height=CanvasHeight)
Object.drawAllObjects()
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