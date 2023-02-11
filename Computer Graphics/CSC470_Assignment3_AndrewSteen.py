############################################################################
## Name: Andrew Steen                                                     ##
## SWID: 102-68-080                                                       ##
## Date: Feb 16 2023                                                      ##
## Assignment #: 3                                                        ##
## Program Discription: In-Place 3D Transiformations in a Multi-Object    ##
##   Environment with Perspective Projection, backface culling,           ##
##   polygon filling, and z buffering. Now including flat shading,        ##
##   Gouraud shading, and Phong shading.                                  ##
##                                                                        ##
## Controls:                                                              ##
## <Left, Right> - Arrow Keys To Cycle Selected Object.                   ##
## <1> - Wireframe                                                        ##
## <2> - Polygon Fill w/ Wireframe                                        ##
## <3> - Polygon Fill                                                     ##
## <4> - Flat Shading         (All Shaing Inherintly Imcorperates         ##
## <5> - Gourand Shading       Polygon Filling and Z-Buffering)           ##
## <6> - Phong Shading                                                    ##                                        
############################################################################


import copy
import math
from tkinter import *

CanvasWidth = 400
CanvasHeight = 400
d = 500

# Debug Toggle
DEBUG_POS = False
DEBUG_EDGE = False
DEBUG_EDGE_BUILD = False
DEBUG_XZ_RL = False

# Object class to make adding shapes easier
class Object:
    ## Contains All Objects in Scene
    all_objects = []
    # Selector for Display Mode
    visual_mode = 1
    # Initiallizing the zBuffer as a class variable for ease of access
    zBuffer = [[d for i in range(CanvasWidth)] for j in range(CanvasHeight)]

    ## Constructor for Object Class
    def __init__(self, point_cloud, shape, color):
        self.point_cloud = point_cloud                              # List of vertices coords
        self.default_point_cloud = copy.deepcopy(point_cloud)       # Making deepCopy for resetting
        self.temp_visual_center = []                                # For inPlace rotation and scaling
        self.shape = shape                                          # List of polygons
        self.color = color                                          # List of polygon colors     
        self.isSelected = False                                     # Toggle for object selection
        Object.all_objects.append(self)                             # Adds objects to list

    # This class function draws all objects
    def drawAllObjects():
        # Reseting zBuffer everytime screen is redrawn
        Object.zBuffer = [[d for i in range(CanvasWidth)] for j in range(CanvasHeight)]

        # Calls drawObject function on each object in all_objects
        for object in Object.all_objects:
            object.drawObject()

    # This class function will draw an object by repeatedly callying drawPoly on each polygon in the object
    def drawObject(self):
        poly = self.shape
        for i in range(len(poly)):
            if (Object.visual_mode == 1):                          # Draws wire frame
                self.drawPolyWire(poly[i])
            elif (Object.visual_mode == 2):                        # Draws filled polygons with wireframe
                self.polygonFill(poly[i], self.color[i])
                self.drawPolyWire(poly[i])
            elif (Object.visual_mode == 3):                        # Draws filled polygons
                self.polygonFill(poly[i], self.color[i])
            elif (Object.visual_mode == 4):                        # Draws flat shaded polygons
                self.flatShade(poly[i])
            elif (Object.visual_mode == 5):                        # Draws Gourand shaded polygons
                self.gouraudShade(poly[i])
            elif (Object.visual_mode == 6):                        # Draws Phong shaded polygonss
                self.phongShade(poly[i])

    # This class function will draw a polygon by repeatedly callying drawLine on each pair of points
    # making up the object.  Remember to draw a line between the last point and the first.
    def drawPolyWire(self, poly):
        ## Drawing Every Line in Poly
        for i in range(-1, len(poly) - 1, 1):
            if (Object.visual_mode != 1):               # For Backface Culling
                if (isFaceShowing(poly)):
                    self.drawLine(poly[i], poly[i+1])
            else:
                self.drawLine(poly[i], poly[i+1])       # For Wireframe

    # This class fuction will fill each polygon pixel by pixel taking in account z values to fix z fighting   
    def polygonFill(self, poly, color):
        # Dont need to fill if ya cant see it
        if (not isFaceShowing(poly)):
            return
        
        # Convert polygon to display coords
        display_poly = projectAndConvertToDisplay(poly)

        # Precompute edge_table: Xstart, Ystart, Yend, dX, Zstart, dZ
        edge_table = computeEdgeTable(display_poly)

        # For debuging
        if DEBUG_EDGE:
            print(edge_table)

        # If too small to draw
        if edge_table == []:
            return

        first_fill_line = edge_table[0][1] # lowest Y value
        last_fill_line = max(edge_table, key=lambda x: x[2])[2] # Single line maximum fn (find max based on sub-list index)

        # Initiallizing Indices
        i, j, next = 0, 1, 2

        # Initiallizing start and stop edge for X and Z
        edge_iX, edge_jX = edge_table[i][0], edge_table[j][0]
        edge_iZ, edge_jZ = edge_table[i][4], edge_table[j][4]

        # Looping through each y line of pixels
        for y in range(first_fill_line, last_fill_line):
            LeftX, RightX, LeftZ, RightZ = 0, 0, 0, 0       # Initiallzing and reseting right and left X and Z edge
            # Insuring the left edge is left of the right edge for X and Z edges
            if (edge_iX < edge_jX):
                LeftX, RightX = edge_iX, edge_jX
                LeftZ, RightZ = edge_iZ, edge_jZ
            else:   # Swap if not
                LeftX, RightX = edge_jX, edge_iX
                LeftZ, RightZ = edge_jZ, edge_iZ

            # For debugging Right and Left X and Z edge coords
            if DEBUG_XZ_RL:
                print("LeftX: ", LeftX, "\tRightX: ", RightX, "LeftZ: ", LeftZ, "\tRightZ: ", RightZ)

            # Initallize z index
            z = LeftZ

            # Getting dZ
            dZFillLine = 0
            if ((RightX - LeftX) != 0):
                dZFillLine = (RightZ - LeftZ)/(RightX - LeftX)
            else:
                dZFillLine = 0

            # Looping through each pixel of current y line
            for x in range(round(LeftX), round(RightX)):
                if (x < 400 and x > 0 and y < 400 and y > 0):   # offscreen Culling
                    # Checking if current z value should be displayed
                    if (z < Object.zBuffer[x][y]):
                        # Draw pixel
                        w.create_line(x, y, x+1, y, fill=color)
                        # Update value in zBuffer
                        Object.zBuffer[x][y] = z
                    # Index z by dZ
                    z += dZFillLine

            # Index edge points by dX and dZ
            edge_iX = edge_iX + edge_table[i][3]
            edge_jX = edge_jX + edge_table[j][3]
            edge_iZ = edge_iZ + edge_table[i][5]
            edge_jZ = edge_jZ + edge_table[j][5]

            # if at the end of active edge then switch to next edge
            if (y >= edge_table[i][2] and y < last_fill_line):
                i = next
                edge_iX = edge_table[i][0]
                edge_iZ = edge_table[i][4]
                next += 1
            # if at the end of active edge then switch to next edge
            if (y >= edge_table[j][2] and y < last_fill_line):
                j = next
                edge_jX = edge_table[j][0]
                edge_jZ = edge_table[j][4]
                next += 1
            
    # Project the 3D endpoints to 2D point using a perspective projection implemented in 'project'
    # Convert the projected endpoints to display coordinates via a call to 'convertToDisplayCoordinates'
    # draw the actual line using the built-in create_line method
    def drawLine(self, start, end):
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
        displayXY.append(point[2])
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
        if DEBUG_POS:
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
        if DEBUG_POS:
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
        if DEBUG_POS:
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
        if DEBUG_POS:
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
        if DEBUG_POS:
            print(self.getVisualCenter())

# ***************************** NON-Class Functions ***************************

# This function normalizes desired vector
def normalize(vec):
    Nx, Ny, Nz = vec[0], vec[1], vec[2]
    return [Nx / math.sqrt(Nx*Nx + Ny*Ny + Nz*Nz), Ny / math.sqrt(Nx*Nx + Ny*Ny + Nz*Nz), Nz / math.sqrt(Nx*Nx + Ny*Ny + Nz*Nz),]

# This function is to determine whether or not a polygon should be back face culled
def isFaceShowing(poly):
    P0, P1, P2 = poly[0], poly[1], poly[2]
    P = getVector(P0, P1) 
    Q = getVector(P0, P2) 
    # To make code more clear.
    Px, Py, Pz = P[0], P[1], P[2]
    Qx, Qy, Qz = Q[0], Q[1], Q[2]
    # Getting normal vector (No Normalization)
    N = [Py*Qz - Pz*Qy, Pz*Qx - Px*Qz, Px*Qy - Py*Qx]
    # Normalizing normal vector
    N_norm = normalize(N);

    # Now we must compute offset plane
    D = N_norm[0]*P0[0] + N_norm[1]*P0[1] + N_norm[2]*P0[2]

    # Now, finally, we determine if the polygon is visable from view point
    V = [0, 0, -d]
    if ((N_norm[0]*V[0] + N_norm[1]*V[1] + N_norm[2]*V[2] - D) > 0):
        return True
    else:
        return False

# This function returns vector from given final and initial points
def getVector(int, fin):
    return [fin[0] - int[0], fin[1] - int[1], fin[2] - int[2]]

# This function converts all vertices of polygon into display X and Y values as well as Zps values
def projectAndConvertToDisplay(poly):
    pro_point = []
    display_points = []
    # Projecting each vertex
    for i in range(len(poly)):
        pro_point.append(Object.project(poly[i]))
    # Converting X and Y into display coords
    for i in range(len(pro_point)):
        display_points.append(Object.convertToDisplayCoordinates(pro_point[i]))
        display_points[i][0] = round(display_points[i][0])  # Rounding X and Y coords
        display_points[i][1] = round(display_points[i][1])
    return display_points

# This function creates an ordered edge table with polygon display points as input
def computeEdgeTable(display_points):
    edge_table = []

    # We need a list of edges sorted from lowest starting Y to highest
    if DEBUG_EDGE_BUILD:
        edges = getEdges(display_points)
        print(edges)
        edges = orientEdges(edges)
        print(edges)
        edges = sortEdges(edges)
        print(edges)
    else:
        edges = sortEdges(orientEdges(getEdges(display_points)))

    # Now we build edge table from ordered edges
    for i in range(len(edges)):
        # Relabeling to making code clearer
        Xstart, Ystart, Xend, Yend = edges[i][0][0], edges[i][0][1], edges[i][1][0], edges[i][1][1]
        Zstart, Zend = edges[i][0][2], edges[i][1][2]
        # Try/Except needed to catch divide by zero errors
        try:
            # Tries to build edge table
            edge_table.append([Xstart, Ystart, Yend, (Xend - Xstart)/(Yend - Ystart), Zstart, (Zend - Zstart)/(Yend - Ystart)])
        except ZeroDivisionError:
            # If dX or dZ is Undifined then pass (Edge not added to edge table)
            pass
    return edge_table

# This function finds edges using polygon display points
def getEdges(poly):
    edges = []
    # Finding edges (Not ordered or oriented)
    for i in range(-1, len(poly) - 1, 1):
        edges.append([poly[i], poly[i+1]])
    return edges

# This function reorients edges that are 180 deg out of phase
def orientEdges(edges):
    # Flipping edges with Ystart values that are greater than Yend
    for i in range(len(edges)):
        if edges[i][0][1] > edges[i][1][1]:     # If Ystart is greater that Yend
            temp = edges[i][0]                  # Then flip points
            edges[i][0] = edges[i][1]
            edges[i][1] = temp
    return edges

# This function sorts edges from lowest Y start to highest
def sortEdges(edges):
    # Single line sort function that sorts list based of specific sub-list index
    return (sorted(edges, key = lambda x: x[0][1]))

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
sq_toppoly0 = [sq_top0_2, sq_top0_1, sq_top0_4, sq_top0_3]
sq_frontpoly0 = [sq_top0_1, sq_base0_1, sq_base0_4, sq_top0_4]
sq_backpoly0 = [sq_top0_3, sq_base0_3, sq_base0_2, sq_top0_2]
sq_rightpoly0 = [sq_top0_2, sq_base0_2, sq_base0_1, sq_top0_1]
sq_leftpoly0 = [sq_top0_4, sq_base0_4, sq_base0_3, sq_top0_3]
# Square1
sq_bottompoly1 = [sq_base1_1, sq_base1_2, sq_base1_3, sq_base1_4]
sq_toppoly1 = [sq_top1_2, sq_top1_1, sq_top1_4, sq_top1_3]
sq_frontpoly1 = [sq_top1_1, sq_base1_1, sq_base1_4, sq_top1_4]
sq_backpoly1 = [sq_top1_3, sq_base1_3, sq_base1_2, sq_top1_2]
sq_rightpoly1 = [sq_top1_2, sq_base1_2, sq_base1_1, sq_top1_1]
sq_leftpoly1 = [sq_top1_4, sq_base1_4, sq_base1_3, sq_top1_3]


# Definition of the objects
pyramid = [py_bottompoly, py_frontpoly, py_rightpoly, py_backpoly, py_leftpoly]
square0 = [sq_bottompoly0, sq_toppoly0, sq_frontpoly0, sq_backpoly0, sq_rightpoly0, sq_leftpoly0]
square1 = [sq_bottompoly1, sq_toppoly1, sq_frontpoly1, sq_backpoly1, sq_rightpoly1, sq_leftpoly1]

# Polygon Colors
pyramid_colors = ["black", "red", "green", "blue", "yellow"]
square_colors0 = ["white", "#cccccc", "#999999", "#666666","#333333", "black"]
square_colors1 = ["white", "#cccccc", "#999999", "#666666","#333333", "black"]

# Definition of the objects' underlying point cloud.  No structure, just the points.
pyramid_point_cloud = [py_apex, py_base1, py_base2, py_base3, py_base4]
square0_point_cloud = [sq_top0_1, sq_top0_2, sq_top0_3, sq_top0_4, sq_base0_1, sq_base0_2, sq_base0_3, sq_base0_4]
square1_point_cloud = [sq_top1_1, sq_top1_2, sq_top1_3, sq_top1_4, sq_base1_1, sq_base1_2, sq_base1_3, sq_base1_4]

# Creating Object object
Pyramid = Object(pyramid_point_cloud, pyramid, pyramid_colors)
Square0 = Object(square0_point_cloud, square0, square_colors0)
Square1 = Object(square1_point_cloud, square1, square_colors1)

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

# Visual mode selection.
#visual_mode = 1
def num_1(event):
    w.delete(ALL)
    Object.visual_mode = 1
    # Redraw objects
    Object.drawAllObjects()
def num_2(event):
    w.delete(ALL)
    Object.visual_mode = 2
    # Redraw objects
    Object.drawAllObjects()
def num_3(event):
    w.delete(ALL)
    Object.visual_mode = 3
    # Redraw objects
    Object.drawAllObjects()

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
root.bind("1", num_1)
root.bind("2", num_2)
root.bind("3", num_3)
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