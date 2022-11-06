import math

import matplotlib.pyplot as plt
import numpy as np

# parameters
dx = 0.01
dy = 0.01
LX = 2
LY = 1
Nx = int(LX/dx)
Ny = int(LY/dy)
# for E(2h)
dx2 = 2*dx
dy2 = 2*dy
Nx2 = int(LX/dx2)
Ny2 = int(LY/dy2)
nx = Nx + 1
ny = Ny + 1
nx2 = Nx2 + 1
ny2 = Ny2 + 1
x = np.linspace(0, LX, nx)
y = np.linspace(0, LY, ny)
x2 = np.linspace(0, LX, nx2)
y2 = np.linspace(0, LY, ny2)

# Iteration Parameters
tol = 10**-10
U = np.zeros((ny, nx))
pi = 3.141592653589793

# boundary conditions
# y_end = np.zero(ny)
U[0,:] = 0
U[Ny,:] = 0;
U[:,0] = np.sin(pi*y)
U[:,Nx] = math.exp(2)*np.sin(pi*y)


U2 = np.copy(U)
exact = np.copy(U)
exact2 = np.copy(U2)

U_old = np.copy(U)
U2_old = np.copy(U2)

U2h = np.zeros((ny2, nx2))
U2h[0,:] = 0
U2h[Ny2,:] = 0;
U2h[:,0] = np.sin(pi*y2)
U2h[:,Nx2] = math.exp(2)*np.sin(pi*y2)
U2h_old = np.copy(U2h)
exact2h = np.copy(U2h)
error = 1
ncount = 0
n2count = 0
outputFile3 = open("outputFile3.txt","w")
outputFile3.close()



# Jacobi Iteration

# Exact Value
for j in range(1, Ny):
    for i in range(1, Nx):
      exact[j,i] = math.exp((i)*dx)*np.sin(pi*(j)*dy)

while(error > tol):
  ncount = ncount + 1
  for j in range(1, Ny):
    for i in range(1, Nx):
      U[j,i] = 0.25*(U_old[j,i+1]+U_old[j,i-1]+U_old[j+1,i]+U_old[j-1,i]) + ((dx**2)/4)*(pi**2 - 1)*math.exp(dx*(i))*np.sin(pi*dy*(j))
  # Check Convergence
  error = np.amax(abs(U-U_old))
  U_old = np.copy(U)
  print("it = {}\terror = {}".format(ncount, error))

errmax = np.amax(abs(U-exact))
print("it = {}\terrmax1 = {}".format(ncount, errmax))
# outputting to file
outputFile3 = open("outputFile3.txt", "a")
outputFile3.write("Jacobi:\n")
outputFile3.write("it = {}\terrmax = {}\n\n".format(ncount, errmax))
outputFile3.close()

error = 1



# Gauss-Seidel Iteration

# Exact 2 Value
for j in range(1, Ny):
  for i in range(1, Nx):
    exact2[j,i] = math.exp((i)*dx)*np.sin(pi*(j)*dy)

while(error > tol):
  n2count = n2count + 1
  for j in range(1, Ny):
    for i in range(1, Nx):
      U2[j,i] = 0.25*(U2_old[j,i+1]+U2[j,i-1]+U2_old[j+1,i]+U2[j-1,i]) + ((dx**2)/4)*(pi**2 - 1)*math.exp(dx*(i))*np.sin(pi*dy*(j))
  # Check Convergence
  error = np.amax(abs(U2-U2_old))
  U2_old = np.copy(U2)
  print("it = {}\terror2 = {}".format(n2count, error))

errmax2 = np.amax(abs(U2-exact2))
print("it = {}\terrmax2 = {}".format(n2count, errmax2))
# outputting to file
outputFile3 = open("outputFile3.txt", "a")
outputFile3.write("G-S:\n")
outputFile3.write("it = {}\terrmax2 = {}\n\n".format(n2count, errmax2))
outputFile3.close()

# error=1;
# ncount=0;


# Error convergence

# # Exact 2h Value
# for j in range(1, Ny2):
#   for i in range(1, Nx2):
#     exact2h[j,i] = math.exp((i)*dx2)*np.sin(pi*(j)*dy2)

# while(error > tol):
#   ncount = ncount + 1
#   for j in range(1, Ny2):
#     for i in range(1, Nx2):
#       U2h[j,i] = 0.25*(U2h_old[j,i+1]+U2h[j,i-1]+U2h_old[j+1,i]+U2h[j-1,i]) + ((dx2**2)/4)*(pi**2 - 1)*math.exp(dx2*(i))*np.sin(pi*dy2*(j))

#   # Check Convergence
#   error = np.amax(abs(U2h-U2h_old))
#   U2h_old = np.copy(U2h)
#   print("it = {}\terror = {}".format(ncount, error))

# errmax2h = np.amax(abs(U2h-exact2h))
# print("it = {}\terrmax = {}".format(ncount, errmax2h))
# print(errmax2h)
# print(errmax2)
# print(math.log(errmax2h/errmax2, 2))
# # outputting to file
# outputFile3 = open("outputFile3.txt", "a")
# outputFile3.write("G-S Error:\n")
# outputFile3.write("E(h) = {}\tConvergence Rate = {}\n\n".format(errmax2, math.log(errmax2h/errmax2, 2)))
# outputFile3.close()


# Plotting
fig = plt.figure()
ax = fig.add_subplot(111, projection = '3d')

X,Y = np.meshgrid(x,y)
# ax.plot_surface(X,Y,U2)
ax.plot_surface(X,Y,exact2)
plt.show()
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')

