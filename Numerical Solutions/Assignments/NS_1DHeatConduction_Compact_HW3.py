import math

import matplotlib.pyplot as plt
import numpy as np

# Lists
u1 = [None] * 1000000
u2 = [None] * 1000000
aa = [None] * 1000000
bb = [None] * 1000000
ex = [None] * 1000000
vv = [None] * 1000000
be = [None] * 1000000
ar = [None] * 1000000
err_w = [None] * 1000000
x = [None] * 1000000
cc = [None] * 1000000
dd = [None] * 1000000

# Parameters
dt = 0.00125
dx = 0.001
r = dt/(dx*dx)
mx = int(1/dx)
n_end = int(1/dt)
print(n_end)


# Initial Conditions
for i in range(0, mx + 1):
  x[i] = i*dx
  u1[i] = math.exp(x[i])

# Functions
def graph():
  x_np = np.array(x)
  y_np_u2 = np.array(u2)
  y_np_ex = np.array(ex)
  # Add a title
  plt.title('Compact Scheme - (t = 1.0)')
  # Add X and y Label
  plt.xlabel('x axis')
  plt.ylabel('U axis')
  plt.plot(x_np, y_np_u2, 'g.', label = "Numerical Solution")
  plt.plot(x_np, y_np_ex, label = "Exact Solution")
  plt.legend(loc = 'upper left')
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
    outputFile.write("i*dx = {0:5}\tu2[{1:}] = {4:10}\tex[{1:}] = {2:10}\t err_w[{1:}] = {3:10}\n". format(round(i*dx, 3), i, ex[i], abs(u2[i] - ex[i]), u2[i]))
  graph()

# Start Computation
nt = 1

while(True):
  u2[0] = math.exp(nt*dt)
  u2[mx] = math.exp(1 + nt*dt)

  # Setting up Tridiagonal System
  for i in range(1, mx):
    aa[i] = 10/12 + r
    bb[i] = r/2 - 1/12
    cc[i] = bb[i]
  for i in range(1, mx):
    dd[i] = (1/12 + r/2)*u1[i-1] + (10/12 - r)*u1[i] + (1/12 + r/2)*u1[i+1]
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

  # if (nt%10 == 0):
  # print(" n = {0:3}\t(x,t) = (0.5,{1:})\tUin = {2:18}\tu(xi,ti) = {3:18}\terr_w = {4:}". format(nt, nt/n_end, u2[int(0.5*mx)], ex[int(0.5*mx)], err_w[nt]))
  # print("{} {}". format(nt, err_w[nt]))
  # print("err = {}  ex[{}] = {}  u2[{}] = {}". format(err, i, ex[i], i, u2[i]))
  # print("i*dx = {0:5}\tu2[{1:}] = {4:10}\tex[{1:}] = {2:10}\t err_w[{1:}] = {3:10}". format(round(i*dx, 3), i, ex[i], err_w[nt], u2[i]))
  if (nt == n_end):
    findMaxError()
    break

  nt = nt + 1
  for i in range(0, mx + 1):
    u1[i] = u2[i]
