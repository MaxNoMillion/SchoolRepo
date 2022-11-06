# Import our modules that we are using
import matplotlib.pyplot as plt
import numpy as np

# # Create the vectors X and Y
# x = np.array(range(100))
# y = x ** 2

# # Create the plot
# plt.plot(x,y,label='y = x**2')

# # Add a title
# plt.title('My first Plot with Python')

# # Add X and y Label
# plt.xlabel('x axis')
# plt.ylabel('y axis')

# # Add a grid
# plt.grid(alpha=.4,linestyle='--')

# # Add a Legend
# plt.legend()

# # Show the plot
# plt.show()

# List
uold = [None] * 10000
unew = [None] * 10000
at = [None] * 10000
aa = [None] * 10000
ah = [None] * 10000
x = [None] * 10000
xh = [None] * 10000

# Parameters
dx = 0.01
dt = 0.01
mx = 200
CFL = dt/dx
n = 0
NT = 100

# Grid point x1, x(i+1/2)
for i in range(0,mx + 1):
  x[i] = i*dx
for i in range(1,mx + 1):
  xh[i] = (i - 0.5)*dx

# Initial condition
for i in range(0, mx + 1):
  if (i >= 20 and i <= 40):
    uold[i] = 1
  else:
    uold[i] = 0

# Boundary Condition
unew[0] = 0
unew[mx] = 0

def reset():
  pass

def graph():
  x_np = np.array(x)
  y_np = np.array(unew)

  # Add a title
  plt.title('Lax-Wendroff Scheme - (t = 1.0)')
  # Add X and y Label
  plt.xlabel('x axis')
  plt.ylabel('Unew axis')
  plt.plot(x_np, y_np)
  plt.show()
  

def outputFunction():
  graph();
  outputFile = open("outputFile.txt", "w")
  for i in range(0, mx + 1):
    print("x = {0:4}\tunew = {1:2}".format(round(x[i], 2), unew[i]))
    outputFile.write("x = {0:4}\tunew = {1:2}\n".format(round(x[i], 2), unew[i]))


# Define a(xi, tn), a(xi+1/2, tn), at(xi, tn)
time_req = [0, 0.1, 0.5, 1]

while(True):
  global tn
  tn = n*dt

  for i in range(1, mx):
    aa[i] = (1 + x[i]*x[i])/(1 + 2*x[i]*tn + 2*x[i]*x[i] + x[i]*x[i]*x[i]*x[i])
  
  for i in range(1, mx + 1):
    ah[i] = (1 + xh[i]*xh[i])/(1 + 2*xh[i]*tn + 2*xh[i]*xh[i] + xh[i]*xh[i]*xh[i]*xh[i])
  
  for i in range(1, mx):
    at[i] = -aa[i]*(2*x[i]/(1 + 2*x[i]*tn + 2*x[i]*x[i] + x[i]*x[i]*x[i]*x[i]))
  
  # Upwind Scheme
  for i in range(1, mx):
    unew[i] = uold[i] - CFL*aa[i]*(uold[i] - uold[i-1])

  # Lax-Wendroff Scheme
  # for i in range(1, mx):
  #   unew[i] = uold[i] - aa[i]*CFL*(uold[i+1]-uold[i-1])/2 - dt*CFL*at[i]*(uold[i+1]-uold[i-1])/4 + CFL**2*aa[i]*(ah[i+1]*(uold[i+1] - uold[i]) - ah[i]*(uold[i] - uold[i-1]))/2

  if(n == NT):
    outputFunction()
    break

  for i in range(1, mx):
    uold[i] = unew[i]
  print("n = {}".format(n))
  n = n + 1









