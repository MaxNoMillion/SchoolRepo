############################################################################
## Name: Andrew Steen                                                     ##
## SWID: 102-68-080                                                       ##
## Date: Feb 28 2023                                                      ##
## Assignment #: 4                                                        ##
## Program Discription: Rending of non-polygonal objects such as speheres ##
##      and planes. The method of rendering is raytracing while using the ##
##      phong illumination model.                                         ##                                    
############################################################################

import copy
import math
from tkinter import *

CanvasWidth = 600
CanvasHeight = 400
d = 500
horizon = 3000
center_of_projection = [0,0,-d]
light_source = [500,500,0]
Ia = 0.2 # Ia = 0.1
Ip = 0.8 # Ip = 1
#L = computeUnitVector() # Lighting vector, 45 degree angle, light is behind viewer's right shoulder
#L = [1,1,-1]
V = [0,0,-1] # View vector, points towards viewer / center of projection [Left Hand Viewing System]
sky_color = [0.53, 0.81, 0.92]    # "87CEEB"

GLOBAL_BIGHTNESS = 1

DEPTH = 4

# Object class to make adding shapes easier
class Object:
  ## Contains All Objects in Scene
  all_objects = []

  def __init__(self, position, Kd, Ks, spec_index, local_weight, reflect, refract):
    self._position = position
    self._Kd = Kd
    self._Ks = Ks
    self._specIndex = spec_index
    self._local_weight = local_weight
    self._reflect = reflect
    self._refract = refract
    self._t = 999999
    self._intersection_point = []
    self._reflect_vector = []
    Sphere.all_objects.append(self)
  # Getter and Setter for t
  def get_t(self):
    return self._t
  def set_t(self, t):
    self._t = t
  # Getter and Setter for intersection_point
  def get_intersection_point(self):
    return self._intersection_point
  def set_intersection_point(self, intersection_point):
    self._intersection_point = intersection_point
  # Getter and Setter for reflect_vector
  def get_reflect_vector(self):
    return self._reflect_vector
  def set_reflect_vector(self, reflect_vector):
    self._reflect_vector = reflect_vector
  # Only getters for the rest of the intance vars
  def get_position(self):
    return self._position
  def get_Kd(self):
    return self._Kd
  def get_Ks(self):
    return self._Ks
  def get_specIndex(self):
    return self._specIndex
  def get_local_weight(self):
    return self._local_weight
  def get_reflect(self):
    return self._reflect
  def get_refract(self):
    return self._refract

  def getReflection(self, ray):
    T = normalize(ray)
    N = self.getNormal()
    demon = 2*(-N[0]*T[0] - N[1]*T[1] - N[2]*T[2])
    self.set_reflect_vector([N[0] + T[0]/demon, N[1] + T[1]/demon, N[2] + T[2]/demon])

  def getColor(self):
    if (type(self) != Plane):
      return self.get_local_color()
    else:
      int_point = self.get_intersection_point()
      X, Y, Z = int_point[0], int_point[1], int_point[2]
      if (X >= 0):
        color_flag = True
      else:
        color_flag = False
      
      if (abs(X)%200 > 100): color_flag = not color_flag

      if (abs(Z)%200 > 100): color_flag = not color_flag

      if (color_flag):
        return [1,0,0]
      else:
        return [1,1,1]

  def phongIntensity(self, ray):
    global Ia
    global Ip
    # if (type(self) == Sphere):
    #   print(self.intersection_point)
    L = computeUnitVector(self.get_intersection_point(), light_source)
    V = normalize(ray)    # Our ray is our view vector in this case
    # Calculating ambiant component
    ambient = Ia * self.get_Kd()
    N = self.getNormal()

    # if (type(self) == Sphere):
    #   print(N)

    # Taking the dot product of Normal and Light vectors
    NdotL = N[0]*L[0] + N[1]*L[1] + N[2]*L[2]
    if NdotL < 0: NdotL = 0     # If neg set to 0
    # Calculating diffuse component
    diffuse = Ip * self.get_Kd() * NdotL
    R = reflect(N,L) # return vector is normalized in "reflect" 
    # Taking dot product of Refect and View vectors
    RdotV = R[0]*V[0] + R[1]*V[1] + R[2]*V[2]
    if RdotV < 0: RdotV = 0     # If neg set to 0
    # Calculating specular component
    specular = Ip * self.get_Ks() * RdotV**self.get_specIndex()
    return ambient + diffuse + specular
    
  def getNormal(self):
    if (type(self) == Plane):
      return self.get_normal()
    else:
      int_point, pos = self.get_intersection_point(), self.get_position()
      return normalize([int_point[0] - pos[0], int_point[1] - pos[1], int_point[2] - pos[2]])

# Object class to make adding shapes easier
class Sphere(Object):
  def __init__(self, position, radius, local_color, Kd, Ks, spec_index, local_weight, reflect, refract):
    Object.__init__(self, position, Kd, Ks, spec_index, local_weight, reflect, refract)
    self._radius = radius
    self._local_color = local_color
  # Getters
  def get_radius(self):
    return self._radius
  def get_local_color(self):
    return self._local_color

  def intersect(self, ray_origin, ray):
    # Trace ray components
    i, j, k = ray[0], ray[1], ray[2]
    # Starting Point
    X1, Y1, Z1 = ray_origin[0], ray_origin[1], ray_origin[2]
    # Center Point
    position = self.get_position()
    l, m, n = position[0], position[1], position[2]
    # Sphere Radius
    r = self.get_radius()

    # Calculate a, b, and c
    a = i*i + j*j + k*k
    b = 2*i*(X1-l) + 2*j*(Y1-m) + 2*k*(Z1-n)
    c = l*l + m*m + n*n + X1*X1 + Y1*Y1 + Z1*Z1 + 2*(-l*X1 - m*Y1 - n*Z1) - r*r

    # Calcualte t
    discriminant = b*b - (4*a*c)
    if discriminant < 0:    # No Roots
      self.set_t(999999)
      self.set_intersection_point([]) 

    elif discriminant == 0: # One Root
      self.set_t(-b/(2*a))
      X, Y, Z = X1 + i*self.get_t(), Y1 + j*self.get_t(), Z1 + k*self.get_t()
      self.set_intersection_point([X,Y,Z])
      self.getReflection(ray)

      if self.get_intersection_point()[2] > horizon or self.get_intersection_point()[2] < 0 or self.get_t() < 0.001: 
        #print(self.intersection_point)
        self.set_intersection_point([])

    elif discriminant > 0:  # Two Roots (take nearest)
      # print("Two")
      # print("Trace ray:", i, j, k)
      # print("Starting Point:", X1, Y1, Z1)
      # print("Center Point:", l, m, n)

      self.set_t((-b - math.sqrt(discriminant))/(2*a))

      X, Y, Z = X1 + i*self.get_t(), Y1 + j*self.get_t(), Z1 + k*self.get_t()
      self.set_intersection_point([X,Y,Z])

      self.getReflection(ray)

      if self.get_intersection_point()[2] > horizon or self.get_intersection_point()[2] < 0 or self.get_t() < 0.001: 
        self.set_intersection_point([])

    return self.get_intersection_point()

class Plane(Object):
  def __init__(self, position, normal, Kd, Ks, spec_index, local_weight, reflect, refract):
    Object.__init__(self, position, Kd, Ks, spec_index, local_weight, reflect, refract)
    self._normal = normal
  # Getter
  def get_normal(self):
    return self._normal
  
  def intersect(self, ray_origin, ray):
    # Surface normals of plane
    normal = self.get_normal()
    A, B, C = normal[0], normal[1], normal[2]
    # Trace ray components
    i, j, k = ray[0], ray[1], ray[2]
    # Starting Point
    #print(ray_origin)
    X1, Y1, Z1 = ray_origin[0], ray_origin[1], ray_origin[2]
    # Calculating D
    position = self.get_position()
    D = A*position[0] + B*position[1] + C*position[2]
    # Calculating t and determining intersection point, if any
    if (A*i + B*j + C*k != 0):
      self.set_t(-(A*X1 + B*Y1 + C*Z1 - D)/(A*i + B*j + C*k))
      X, Y, Z = X1 + i*self.get_t(), Y1 + j*self.get_t(), Z1 + k*self.get_t()
      self.set_intersection_point([X,Y,Z])
      self.getReflection(ray)
      # Z cut-off plane/ -Z catch/ -t catch
      if self.get_intersection_point()[2] > horizon or self.get_intersection_point()[2] < 0 or self.get_t() < 0.001: 
        #print(self.intersection_point)
        self.set_intersection_point([])
    else:
      self.set_t(999999)
      self.set_intersection_point([])
    return self.get_intersection_point()

def traceRay(start_point, ray, depth):
  # Return "black" on Final Recusive Call
  if depth == 0: return [0,0,0]
  # Intersect the ray with all objects to determine nearest_object (if any)
  tMin = 999999 # initializing t to large value
  # Check intersection for every object in scene
  for object in Object.all_objects:
    if object.intersect(start_point, ray) != []:   # Does Ray Intersect Object?
      if object.get_t() < tMin:                         # Determines Closest Object
          tMin = object.get_t()
          nearest_object = object                  # Sets Current Object as Nearest Object
  if tMin == 999999: return sky_color                # No Intersect = Sky 
  # Get local object color
  color = nearest_object.getColor()
  # Get intesity of current
  intensity = nearest_object.phongIntensity(ray)
  #if inShadow(nearest_object, nearest_object.intersection_point): intensity *= 0.25
  local_color = [color[0]*intensity*GLOBAL_BIGHTNESS, color[1]*intensity*GLOBAL_BIGHTNESS, color[2]*intensity*GLOBAL_BIGHTNESS]
  local_weight = nearest_object.get_local_weight()
  # Compute the Color Returned from the Reflected Ray
  reflect_weight = nearest_object.get_reflect()
  reflect_color = traceRay(nearest_object.get_intersection_point(), nearest_object.get_reflect_vector(), depth-1)
  # Combine local and reflect colors using weights
  final_color = [0,0,0]
  # print(local_color, local_weight, reflect_color, reflect_weight)
  for i in range(3):
    final_color[i] = local_color[i]*local_weight + reflect_color[i]*reflect_weight
  return final_color

def renderImage():
  top = round(CanvasHeight/2)
  bottom = round(-CanvasHeight/2)
  left = round(-CanvasWidth/2)
  right = round(CanvasWidth/2)

  for y in range(top, bottom, -1):
    if (y%10 == 0): print("Pixel:", [0,y])
    for x in range(left, right):
      ray = computeUnitVector(center_of_projection, [x, y, 0])
      color = traceRay(center_of_projection, ray, DEPTH)
      w.create_line(right+x, top-y, right+x+1, top-y, fill=RGBColorHexCode(color))

def RGBColorHexCode(color_components):
  full_hex_code = "#"
  for i in range(3):
    if color_components[i] > 1: color_components[i] = 1
    hexString = str(hex(round(255 * color_components[i])))
    if hexString[0] == "-": # illumination intensity should not be negative
      print("illumination intensity is Negative. Setting to 00. Did you check for negative NdotL?")
      trimmedHexString = "00"
    else:
      trimmedHexString = hexString[2:] # get rid of "0x" at the beginning of hex strings
      if len(trimmedHexString) == 1: trimmedHexString = "0" + trimmedHexString
      # we will use the green color component to display our monochrome illunmination results
    full_hex_code += trimmedHexString
  return full_hex_code
    
def computeUnitVector(start, end):
  return normalize([end[0]-start[0], end[1]-start[1], end[2]-start[2]])
  
# This function normalizes desired vector
def normalize(vector):
    sumOfSquares = 0
    # Summs the square of each component
    for i in range(len(vector)):
        sumOfSquares += vector[i]**2
    # Gets mag
    magnitude = math.sqrt(sumOfSquares)
    vect = []
    # Divides each component by mag
    for i in range(len(vector)):
        vect.append(vector[i]/magnitude)
    return vect  

def inShadow(start_object, start_point):
  ray = computeUnitVector(start_point, light_source)
  for object in Object.all_objects:
    if start_object != object and object.intersect(start_point, ray) != []: return True
  return False

# This function returns the reflection vector of the light vector
def reflect(N, L):
  R = []
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

# Instantiate Board Object
# Args: position, normal, Kd, Ks, spec_index, local_weight, reflect, refract
#board = Plane([0,-300,0], [0,1,0], 0.9, 0.1, 8, 0.8, 0.25, 0)

# Instantiate Sphere Objects
# Args: position, radius, local_color, Kd, Ks, spec_index, local_weight, reflect, refract
redSphere = Sphere([300, -100, 700], 200, [1,0.5,0.5], 0.5, 0.5, 8, 0.2, 0, 0)

# Define a drawing canvas and render the 20 spheres on it
root = Tk()
outerframe = Frame(root)
outerframe.pack()
w = Canvas(outerframe, width = CanvasWidth, height = CanvasHeight)
renderImage()
w.pack()
root.mainloop() 
