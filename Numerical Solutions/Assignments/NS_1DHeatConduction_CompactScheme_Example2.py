import math
import os
import sys

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

matplotlib.rc('font', size=18)
matplotlib.rc('font', family='Arial')

#definition of numerical parameters
N = 51 #number of grid points
dt = 5.e-4 #time step
L = float(1) #size of grid
nsteps = 620 #number of time steps
dx = L/(N-1) #grid spacing
nplot = 20 #number of timesteps before plotting

r = dt/dx**2 #assuming heat diffusion coefficient == 1

#initialize matrices A, B and b array
A = np.zeros((N-2,N-2))
B = np.zeros((N-2,N-2))
b = np.zeros((N-2))
#define matrices A, B and b array
for i in range(N-2):
    if i==0:
        A[i,:] = [2+2*r if j==0 else (-r) if j==1 else 0 for j in range(N-2)]
        B[i,:] = [2-2*r if j==0 else r if j==1 else 0 for j in range(N-2)]
        b[i] = 0. #boundary condition at i=1
    elif i==N-3:
        A[i,:] = [-r if j==N-4 else 2+2*r if j==N-3 else 0 for j in range(N-2)]
        B[i,:] = [r if j==N-4 else 2-2*r if j==N-3 else 0 for j in range(N-2)]
        b[i] = 0. #boundary condition at i=N
    else:
        A[i,:] = [-r if j==i-1 or j==i+1 else 2+2*r if j==i else 0 for j in range(N-2)]
        B[i,:] = [r if j==i-1 or j==i+1 else 2-2*r if j==i else 0 for j in range(N-2)]

#initialize grid
x = np.linspace(0,1,N)
#initial condition
# u = np.asarray([2*xx if xx<=0.5 else 2*(1-xx) for xx in x])
u = np.asarray([math.exp(xx) for xx in x])
#evaluate right hand side at t=0
bb = B.dot(u[1:-1]) + b

x_np = np.array(x)
y_np_u2 = np.array(u)
# y_np_ex = np.array(ex)
plt.plot(x_np, y_np_u2)
# plt.plot(x_np, y_np_ex)
plt.show()


# fig = plt.figure()
# plt.plot(x,u,linewidth=2)
# filename = 'foo000.jpg';
# fig.set_tight_layout(True);
# plt.xlabel("x")
# plt.ylabel("u")
# plt.title("t = 0")
# plt.savefig(filename)
# plt.clf()

# c = 0
# for j in range(nsteps):
#     print(j)
#     #find solution inside domain
#     u[1:-1] = np.linalg.solve(A,bb)
#     #update right hand side
#     bb = B.dot(u[1:-1]) + b
#     if(j%nplot==0): #plot results every nplot timesteps
#         plt.plot(x,u,linewidth=2)
#         plt.ylim([0,1])
#         filename = 'foo' + str(c+1).zfill(3) + '.jpg';
#         plt.xlabel("x")
#         plt.ylabel("u")
#         plt.title("t = %2.2f"%(dt*(j+1)))
#         plt.savefig(filename)
#         plt.clf()
#         c += 1

# os.system("ffmpeg -y -i 'foo%03d.jpg' heat_equation.m4v")
# os.system("rm -f *.jpg")
