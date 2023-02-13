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
Ia = 0.3 # intensity of the ambient light in the scene
Ip = 0.7 # inensity of the point light source in the scene
Kd = 0.5 # diffuse reflectivity of object
Ks = 0.5 # diffuse reflectivity of point light
specIndex = 16 # Spread of reflected light
L = [1,1,-1] # Lighting vector, 45 degree angle, light is behind viewer's right shoulder
V = [0,0,-1] # View vector, points towards viewer / center of projection [Left Hand Viewing System]

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
        polys = self.shape
        for i in range(len(polys)):
            if (Object.visual_mode == 1):                          # Draws wire frame
                self.drawPolyWire(polys[i])
            elif (Object.visual_mode == 2):                        # Draws filled polygons with wireframe
                self.polygonFill(polys, polys[i], i, self.color[i])
                self.drawPolyWire(polys[i])
            elif (Object.visual_mode > 2):                        # Draws filled polygons
                self.polygonFill(polys, polys[i], i, self.color[i])

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
    def polygonFill(self, polys, poly, poly_num, color):
        # Gets both current poly normal and list of vertex normals of intersecting polys
        poly_norm_list, poly_norm = getNormals(polys, poly_num)
        # Dont need to fill if ya cant see it
        if (not isFaceShowing(poly)):
            return
        # Convert polygon to display coords
        display_poly = projectAndConvertToDisplay(poly, poly_norm_list)

        # Precompute edge_table: Xstart, Ystart, Yend, dX, Zstart, dZ, Nstart, dN, dI
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
        # For Gaurand Shading
        edge_iI, edge_jI = getIntensity(edge_table[i][6]), getIntensity(edge_table[j][6])
        # For Phong Shading
        edge_iN, edge_jN = copy.deepcopy(edge_table[i][6]), copy.deepcopy(edge_table[j][6])

        # Looping through each y line of pixels
        for y in range(first_fill_line, last_fill_line):
            LeftX, RightX, LeftZ, RightZ = 0, 0, 0, 0       # Initiallzing and reseting right and left X and Z edge
            LeftI, RightI = 0, 0                            # For Gaurand Shading
            LeftN, RightN = [0,0,0], [0,0,0]                # For Phong Shading  
            # Insuring the left edge is left of the right edge for X and Z edges
            if (edge_iX < edge_jX):
                LeftX, RightX = edge_iX, edge_jX
                LeftZ, RightZ = edge_iZ, edge_jZ
                LeftI, RightI = edge_iI, edge_jI
                LeftN, RightN = copy.deepcopy(edge_iN), copy.deepcopy(edge_jN)
            else:   # Swap if not
                LeftX, RightX = edge_jX, edge_iX
                LeftZ, RightZ = edge_jZ, edge_iZ
                LeftI, RightI = edge_jI, edge_iI
                LeftN, RightN = copy.deepcopy(edge_jN), copy.deepcopy(edge_iN)
            # For debugging Right and Left X and Z edge coords
            if DEBUG_XZ_RL:
                print("LeftX: ", LeftX, "\tRightX: ", RightX, "LeftZ: ", LeftZ, "\tRightZ: ", RightZ, "LeftI: ", LeftI, "\tRightI: ", RightI, "LeftN: ", LeftN, "\tRightN: ", RightN)

            # Initallize z index
            z = LeftZ
            # Initallize intensity index
            intensity = copy.deepcopy(LeftZ)
            # Initallize n index
            n = copy.deepcopy(LeftN)

            # Getting dZ
            dZFillLine = 0
            if ((RightX - LeftX) != 0):
                dZFillLine = (RightZ - LeftZ)/(RightX - LeftX)
            else:
                dZFillLine = 0

            # Getting dI
            dIFillLine = 0
            if ((RightX - LeftX) != 0):
                dIFillLine = (RightI - LeftI)/(RightX - LeftX)
            else:
                dIFillLine = 0

            # Getting dN
            dNFillLine = [0,0,0]
            if ((RightX - LeftX) != 0):
                dNFillLine[0] = (RightN[0] - LeftN[0])/(RightX - LeftX)
                dNFillLine[1] = (RightN[1] - LeftN[1])/(RightX - LeftX)
                dNFillLine[2] = (RightN[2] - LeftN[2])/(RightX - LeftX)
            else:
                dNFillLine = [0,0,0]

            # Looping through each pixel of current y line
            for x in range(round(LeftX), round(RightX)):
                if (x < 400 and x > 0 and y < 400 and y > 0):   # offscreen Culling
                    # Checking if current z value should be displayed
                    if (z < Object.zBuffer[x][y]):
                        # Draw pixel
                        w.create_line(x, y, x+1, y, fill = getColor(poly_norm, intensity, n, color))
                        # Update value in zBuffer
                        Object.zBuffer[x][y] = z
                    # Index z by dZ
                    z += dZFillLine
                    intensity += dIFillLine
                    n[0] += dNFillLine[0]
                    n[1] += dNFillLine[1]
                    n[2] += dNFillLine[2]

            # Index edge points by dX and dZ
            edge_iX = edge_iX + edge_table[i][3]
            edge_jX = edge_jX + edge_table[j][3]
            edge_iZ = edge_iZ + edge_table[i][5]
            edge_jZ = edge_jZ + edge_table[j][5]
            edge_iI = edge_iI + edge_table[i][8]
            edge_jI = edge_jI + edge_table[j][8]
            edge_iN[0] = edge_iN[0] + edge_table[i][7][0]
            edge_iN[1] = edge_iN[1] + edge_table[i][7][1]
            edge_iN[2] = edge_iN[2] + edge_table[i][7][2]
            edge_jN[0] = edge_jN[0] + edge_table[j][7][0]
            edge_jN[1] = edge_jN[1] + edge_table[j][7][1]
            edge_jN[2] = edge_jN[2] + edge_table[j][7][2]

            # if at the end of active edge then switch to next edge
            if (y >= edge_table[i][2] and y < last_fill_line):
                i = next
                edge_iX = edge_table[i][0]
                edge_iZ = edge_table[i][4]
                edge_iI = getIntensity(edge_table[i][6])
                edge_iN[0] = edge_table[i][6][0]
                edge_iN[1] = edge_table[i][6][1]
                edge_iN[2] = edge_table[i][6][2]
                next += 1
            # if at the end of active edge then switch to next edge
            if (y >= edge_table[j][2] and y < last_fill_line):
                j = next
                edge_jX = edge_table[j][0]
                edge_jZ = edge_table[j][4]
                edge_jI = getIntensity(edge_table[j][6])
                edge_jN[0] = edge_table[j][6][0]
                edge_jN[1] = edge_table[j][6][1]
                edge_jN[2] = edge_table[j][6][2]
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
        try:
            displayXY.append(point[3])
        except:
            pass
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

# This function determines color of pixel determined by which visual mode
def getColor(poly_norm, pixel_intensity, pixel_normal, color):
    if Object.visual_mode == 2 or Object.visual_mode == 3:
        return color
    elif Object.visual_mode == 4:
        return getFlatPixel(poly_norm)
    elif Object.visual_mode == 5:
        return getGaurandPixel(pixel_intensity)
    else:
        return getPhongPixel(pixel_normal)

def determineColor(poly_norm):
    int_comps = getIntensityComponents(poly_norm)
    color = triColorHexCode(int_comps[0], int_comps[1], int_comps[2])
    return color

def getIntensityComponents(poly_norm):
    global L
    global V
    global Ip
    global Ia
    global Ks
    global Kd
    global specIndex
    L = normalize(L)
    V = normalize(V)
    # ambient diffuse component of illumination model
    ambient = Ia * Kd
    N = normalize(poly_norm)
    NdotL = N[0]*L[0] + N[1]*L[1] + N[2]*L[2]
    if NdotL < 0: NdotL = 0
    diffuse = Ip * Kd * NdotL
    R = reflect (N,L) # return vector is normalized in "reflect" 
    RdotV = R[0]*V[0] + R[1]*V[1] + R[2]*V[2]
    if RdotV < 0: RdotV = 0
    specular = Ip * Ks * RdotV**specIndex

    return [ambient, diffuse, specular]

def getIntensity(poly_norm):
    int_comps = getIntensityComponents(poly_norm)
    return int_comps[0] + int_comps[1] + int_comps[2]

# This function flat shades current pixels
def getFlatPixel(norm):
    return determineColor(norm)
        
# This function gaurand shades current pixels
def getGaurandPixel(intensity):
    pass

# This function phonge shades current pixels
def getPhongPixel(pixel_norm):
    int_comps = getIntensityComponents(pixel_norm)
    color = triColorHexCode(int_comps[0], int_comps[1], int_comps[2])
    return color

# This function normalizes desired vector
def normalize(vector):
    sumOfSquares = 0
    for i in range(len(vector)):
        sumOfSquares += vector[i]**2
    magnitude = math.sqrt(sumOfSquares)
    vect = []
    for i in range(len(vector)):
        vect.append(vector[i]/magnitude)
    return vect

# This function returns the reflection vector of the light vector
def reflect(N, L):
  R = []
  # Normalize the Normal vector and Light vector
  N = normalize(N)
  L = normalize(L)
  # Taking the cross product of the Normal and Light vector
  twoCosPhi = 2 * (N[0]*L[0] + N[1]*L[1] + N[2]*L[2])
  # Determining the direction of reflection vector
  if twoCosPhi > 0:
    for i in range(3):
      R.append(N[i] - (L[i] / twoCosPhi))
  elif twoCosPhi == 0:
    for i in range(3):
      R.append(-L[i])
  else: # twoCosPhi < 0
    for i in range(3):
      R.append(-N[i] + (L[i] / twoCosPhi))
  return normalize(R)

# This function converts ambient, diffuse, and spectular to a hex code
def triColorHexCode(ambient, diffuse, specular):
  combinedColorCode = colorHexCode(ambient + diffuse + specular)
  specularColorCode = colorHexCode(specular)
  colorString = "#" + specularColorCode + combinedColorCode + specularColorCode
  return colorString

# This function formats hex code
def colorHexCode(intensity):
  hexString = str(hex(round(255 * intensity)))
  if hexString[0] == "-": # illumination intensity should not be negative
    print("illumination intensity is Negative. Setting to 00. Did you check for negative NdotL?")
    trimmedHexString = "00"
  else:
    trimmedHexString = hexString[2:] # get rid of "0x" at the beginning of hex strings
    if len(trimmedHexString) == 1: trimmedHexString = "0" + trimmedHexString
    # we will use the green color component to display our monochrome illunmination results
  return trimmedHexString

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
def projectAndConvertToDisplay(poly, poly_norm_list):
    pro_point = []
    display_points = []
    # Projecting each vertex
    for i in range(len(poly)):
        pro_point.append(Object.project(poly[i]))
    # Converting X and Y into display coords
    for i in range(len(pro_point)):
        #print(poly_norm_list[i])
        pro_point[i].append(poly_norm_list[i])
        #print(pro_point[i])
        display_points.append(Object.convertToDisplayCoordinates(pro_point[i]))
        #print(display_points)
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
        Nstart, Nend = edges[i][0][3], edges[i][1][3]       # Normals
        Istart, Iend = getIntensity(Nstart), getIntensity(Nend)
        # Try/Except needed to catch divide by zero errors
        try:
            # Tries to build edge table
            edge_table.append([Xstart, Ystart, Yend, (Xend - Xstart)/(Yend - Ystart), Zstart, (Zend - Zstart)/(Yend - Ystart),
                              Nstart, [(Nend[0] - Nstart[0])/(Yend - Ystart), (Nend[1] - Nstart[1])/(Yend - Ystart), 
                              (Nend[2] - Nstart[2])/(Yend - Ystart)], (Iend - Istart)/(Yend - Ystart)])
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

# Gets normal of passed in poly
def getNormal(poly):
    # First Normal
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
    return N_norm

# Gets list of normals of polygon vertices
def getNormals(poly_list, poly_num):
    # # Slicing of end polygons
    # poly_list = poly_list[:8]
    # Getting normal of current poly
    curr_poly_norm = getNormal(poly_list[poly_num])
    norm_list = []
    if poly_num < 8:
        # Get Normals of adjacent polys                             # if current poly == poly_list[3]
        pre_poly_norm = getNormal(poly_list[(poly_num - 1)&7])           # getting normal of poly_list[2] 
        post_poly_norm = getNormal(poly_list[(poly_num + 1)%8])             # and poly_list[4]
        # Getting Normal Vectors on Intersections of Polys 
        NV1 = normalize(addVector(pre_poly_norm, curr_poly_norm))
        NV2 = normalize(addVector(pre_poly_norm, curr_poly_norm))
        NV3 = normalize(addVector(post_poly_norm, curr_poly_norm))
        NV4 = normalize(addVector(post_poly_norm, curr_poly_norm))
        # Creates List of Vertex Normals on Intersections of Polys
        norm_list = [NV1, NV2, NV3, NV4]
    else:
        for i in range(8):
            norm_list.append(curr_poly_norm)
    # Returns both List of Normals and Current Poly Normal
    return norm_list, curr_poly_norm
        
# This function adds vectors
def addVector(P, Q):
    return [P[0] + Q[0], P[1] + Q[1], P[2] + Q[2]]

# ***************************** Initialize Objects ***************************
# # Defining Pyramid
# # Coords of Vertices
# py_apex = [0,50,100]
# py_base1 = [50,-50,50]
# py_base2 = [50,-50,150]
# py_base3 = [-50,-50,150]
# py_base4 = [-50,-50,50]
# # Polys defined from points in clockwise order viewed from the outside
# py_frontpoly = [py_apex, py_base1, py_base4]
# py_rightpoly = [py_apex, py_base2, py_base1]
# py_backpoly = [py_apex, py_base3, py_base2]
# py_leftpoly = [py_apex, py_base4, py_base3]
# py_bottompoly = [py_base1, py_base2, py_base3, py_base4]
# # Defining object from group of polys
# pyramid = [py_bottompoly, py_frontpoly, py_rightpoly, py_backpoly, py_leftpoly]
# # Creating point cloud of objects vertices
# pyramid_point_cloud = [py_apex, py_base1, py_base2, py_base3, py_base4]
# # Setting colors of each poly
# pyramid_colors = ["black", "red", "green", "blue", "yellow"]
# # Defining object
# Pyramid = Object(pyramid_point_cloud, pyramid, pyramid_colors)

# # Defining Square0 (Cube)
# # Coords of Vertices
# sq_top0_1 = [-100,50,50]
# sq_top0_2 = [-100,50,150]
# sq_top0_3 = [-200,50,150]
# sq_top0_4 = [-200,50,50]
# sq_base0_1 = [-100,-50,50]
# sq_base0_2 = [-100,-50,150]
# sq_base0_3 = [-200,-50,150]
# sq_base0_4 = [-200,-50,50]
# # Polys defined from points in clockwise order viewed from the outside
# sq_bottompoly0 = [sq_base0_1, sq_base0_2, sq_base0_3, sq_base0_4]
# sq_toppoly0 = [sq_top0_2, sq_top0_1, sq_top0_4, sq_top0_3]
# sq_frontpoly0 = [sq_top0_1, sq_base0_1, sq_base0_4, sq_top0_4]
# sq_backpoly0 = [sq_top0_3, sq_base0_3, sq_base0_2, sq_top0_2]
# sq_rightpoly0 = [sq_top0_2, sq_base0_2, sq_base0_1, sq_top0_1]
# sq_leftpoly0 = [sq_top0_4, sq_base0_4, sq_base0_3, sq_top0_3]
# # Defining object from group of polys
# square0 = [sq_bottompoly0, sq_toppoly0, sq_frontpoly0, sq_backpoly0, sq_rightpoly0, sq_leftpoly0]
# # Creating point cloud of objects vertices
# square0_point_cloud = [sq_top0_1, sq_top0_2, sq_top0_3, sq_top0_4, sq_base0_1, sq_base0_2, sq_base0_3, sq_base0_4]
# # Setting colors of each poly
# square_colors0 = ["white", "#cccccc", "#999999", "#666666","#333333", "black"]
# # Defining object
# Square0 = Object(square0_point_cloud, square0, square_colors0)

# # Defining Square1 (Cube)
# # Coords of Vertices
# sq_top1_1 = [200,50,50]
# sq_top1_2 = [200,50,150]
# sq_top1_3 = [100,50,150]
# sq_top1_4 = [100,50,50]
# sq_base1_1 = [200,-50,50]
# sq_base1_2 = [200,-50,150]
# sq_base1_3 = [100,-50,150]
# sq_base1_4 = [100,-50,50]
# # Polys defined from points in clockwise order viewed from the outside
# sq_bottompoly1 = [sq_base1_1, sq_base1_2, sq_base1_3, sq_base1_4]
# sq_toppoly1 = [sq_top1_2, sq_top1_1, sq_top1_4, sq_top1_3]
# sq_frontpoly1 = [sq_top1_1, sq_base1_1, sq_base1_4, sq_top1_4]
# sq_backpoly1 = [sq_top1_3, sq_base1_3, sq_base1_2, sq_top1_2]
# sq_rightpoly1 = [sq_top1_2, sq_base1_2, sq_base1_1, sq_top1_1]
# sq_leftpoly1 = [sq_top1_4, sq_base1_4, sq_base1_3, sq_top1_3]
# # Defining object from group of polys
# square1 = [sq_bottompoly1, sq_toppoly1, sq_frontpoly1, sq_backpoly1, sq_rightpoly1, sq_leftpoly1]
# # Creating point cloud of objects vertices
# square1_point_cloud = [sq_top1_1, sq_top1_2, sq_top1_3, sq_top1_4, sq_base1_1, sq_base1_2, sq_base1_3, sq_base1_4]
# # Setting colors of each poly
# square_colors1 = ["white", "#cccccc", "#999999", "#666666","#333333", "black"]
# # Defining object
# Square1 = Object(square1_point_cloud, square1, square_colors1)

# Defining Cylinder
# Coords of Vertices
front1 = [-50,120.7107,50]
front2 = [50,120.7107,50]
front3 = [120.7107,50,50]
front4 = [120.7107,-50,50]
front5 = [50,-120.7107,50]
front6 = [-50,-120.7107,50]
front7 = [-120.7107,-50,50]
front8 = [-120.7107,50,50]
back1 = [-50,120.7107,450]
back2 = [50,120.7107,450]
back3 = [120.7107,50,450]
back4 = [120.7107,-50,450]
back5 = [50,-120.7107,450]
back6 = [-50,-120.7107,450]
back7 = [-120.7107,-50,450]
back8 = [-120.7107,50,450]
# Polys defined from points in clockwise order viewed from the outside
northPoly = [front1, back1, back2, front2]
northEastPoly = [front2, back2, back3, front3]
eastPoly = [front3, back3, back4, front4]
southEastPoly = [front4, back4, back5, front5]
southPoly = [front5, back5, back6, front6]
southWestPoly = [front6, back6, back7, front7]
westPoly = [front7, back7, back8, front8]
northWestPoly = [front8, back8, back1, front1]
frontPoly = [front1, front2, front3, front4, front5, front6, front7, front8]
backPoly = [back1, back8, back7, back6, back5, back4, back3, back2]
# Defining object from group of polys
cylinder = [northPoly, northEastPoly, eastPoly, southEastPoly, southPoly, southWestPoly, westPoly, northWestPoly, frontPoly, backPoly]
# Creating point cloud of objects vertices
cylinder_point_cloud = [front1, front2, front3, front4, front5, front6, front7, front8, back1, back2, back3, back4, back5, back6, back7, back8]
# Setting colors of each poly
cylinder_colors = ["black", "red", "green", "blue", "yellow", "black", "red", "green", "#666666", "#333333"]

# Defining object
cylinder = Object(cylinder_point_cloud, cylinder, cylinder_colors)

#************************************************************************************

#### OBJECT SELECTOR ####
# Starting Object
object = Object.all_objects[0]
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
def num_4(event):
    w.delete(ALL)
    Object.visual_mode = 4
    # Redraw objects
    Object.drawAllObjects()
def num_5(event):
    w.delete(ALL)
    Object.visual_mode = 5
    # Redraw objects
    Object.drawAllObjects()
def num_6(event):
    w.delete(ALL)
    Object.visual_mode = 6
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
root.bind("4", num_4)
root.bind("5", num_5)
root.bind("6", num_6)
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