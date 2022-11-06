import math

import matplotlib.pyplot as plt
import numpy as np

# Lists
u1 = [None] * 10000
u2 = [None] * 10000
aa = [None] * 10000
bb = [None] * 10000
ex = [None] * 10000
vv = [None] * 10000
be = [None] * 10000
ar = [None] * 10000
err_w = [None] * 10000
x = [None] * 10000
cc = [None] * 10000
dd = [None] * 10000

# Parameters
dt = 0.05
dx = 0.001
r = dt/(dx*dx)
mx = 1000
n_end = 20

# Initial Conditions
for i in range(0, mx + 1):
  x[i] = i*dx
  u1[i] = math.exp(x[i])

# Functions
def graph():
  x_np = np.array(x)
  y_np_u2 = np.array(u2)
  y_np_ex = np.array(ex)
  plt.plot(x_np, y_np_u2)
  plt.plot(x_np, y_np_ex)
  plt.show()

def findMaxError():
  
  errmax = 0
  for n in range(1, n_end + 1):
    if (err_w[n] > errmax):
      errmax = err_w[n]
  print("max error = {}". format(errmax))
  # Output the solution
  outputFile = open("outputFile.txt", "w")
  outputFile.write("max error = {}\n". format(errmax))
  
  for i in range(0, mx + 1):
    outputFile.write("i*dx = {0:5}\tu2[{1:}] = {4:10}\tex[{3:}] = {2:2}\n". format(round(i*dx, 3), i, ex[i], i, u2[i]))
  graph()

# Start Computation
nt = 1

while(True):
  u2[0] = math.exp(nt*dt)
  u2[mx] = math.exp(1 + nt*dt)

  # Setting up Tridiagonal System
  for i in range(1, mx):
    aa[i] = 1 + r
    bb[i] = r/2
    cc[i] = bb[i]
  for i in range(1, mx):
    dd[i] = r*u1[i-1]/2 + (1 - r)*u1[i] + r*u1[i+1]/2
  dd[1] = dd[1] + bb[1]*u2[0]
  dd[mx-1] = dd[mx-1] + cc[mx-1]*u2[mx]
  bb[1] = 0
  cc[mx-1] = 0

  # Thomas Algorithm
  be[0] = 0
  ar[0] = 0
  for k in range(1, mx):
    be[k] = cc[k]/(aa[k] - bb[k]*be[k-1])
    ar[k] = (dd[k] + bb[k]*ar[k-1])/(aa[k] - bb[k]*be[k-1])
  
  vv[mx] = 0
  for j in range(1, mx):
    jj = mx - j
    vv[jj] = be[jj]*vv[jj+1] + ar[jj]

  for i in range(1, mx):
    u2[i] = vv[i]

  # Exact Solution and Error
  for i in range(0, mx+1):
    ex[i] = math.exp(nt*dt + x[i])
  err = 0
  for i in range(1, mx):
    err = err + (u2[i] - ex[i])*(u2[i] - ex[i]) 

  err_w[nt] = math.sqrt(dx*err)
  print("{} {}". format(nt, err_w[nt]))
  #print("err = {}  ex[{}] = {}  u2[{}] = {}". format(err, i, ex[i], i, u2[i]))

  if (nt == n_end):
    findMaxError()
    break

  nt = nt + 1
  for i in range(0, mx + 1):
    u1[i] = u2[i]
