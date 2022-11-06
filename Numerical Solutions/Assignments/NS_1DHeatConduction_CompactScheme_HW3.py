import math

import matplotlib.pyplot as plt
import numpy as np

max_x = 1
max_t = 200

Mx = 100
dx = max_x / (Mx-1)

Nt = 1000
dt = max_t / (Nt-1)

x_grid = np.array([j*dx for j in range(Mx)])
t_grid = np.array([n*dt for n in  range(Nt)])

D_v = float(10.)/float(100.)
D_u = 0.01 * D_v

k0 = 0.067
f = lambda u, v: dt*(v*(k0 + float(u*u)/float(1. + u*u)) - u)
g = lambda u, v: -f(u,v)
 
sigma_u = float(D_u*dt)/float((2.*dx*dx))
sigma_v = float(D_v*dt)/float((2.*dx*dx))

total_protein = 2.26

no_high = 10
U = np.array([0.1 for i in range(no_high, Mx)] + [2. for i in range(0, no_high)])
V = np.array([float(total_protein - dx* sum(U))/float(Mx*dx) for i in range(0, Mx)])

# plt.ylim((0., 2.1))
# plt.xlabel('x'); plt.ylabel('concentration')
# plt.plot(x_grid, U)
# plt.plot(x_grid, V)
# plt.show()

A_u = np.diagflat([-sigma_u for i in range(Mx-1)], -1) +\
      np.diagflat([1.+sigma_u]+[1.+2.*sigma_u for i in range(Mx-2)]+[1.+sigma_u]) +\
      np.diagflat([-sigma_u for i in range(Mx-1)], 1)
        
B_u = np.diagflat([sigma_u for i in range(Mx-1)], -1) +\
      np.diagflat([1.-sigma_u]+[1.-2.*sigma_u for i in range(Mx-2)]+[1.-sigma_u]) +\
      np.diagflat([sigma_u for i in range(Mx-1)], 1)
        
A_v = np.diagflat([-sigma_v for i in range(Mx-1)], -1) +\
      np.diagflat([1.+sigma_v]+[1.+2.*sigma_v for i in range(Mx-2)]+[1.+sigma_v]) +\
      np.diagflat([-sigma_v for i in range(Mx-1)], 1)
        
B_v = np.diagflat([sigma_v for i in range(Mx-1)], -1) +\
      np.diagflat([1.-sigma_v]+[1.-2.*sigma_v for i in range(Mx-2)]+[1.-sigma_v]) +\
      np.diagflat([sigma_v for i in range(Mx-1)], 1)

f_vec = lambda U, V: np.multiply(dt, np.subtract(np.multiply(V, 
                     np.add(k0, np.divide(np.multiply(U,U), np.add(1., np.multiply(U,U))))), U))

# print(f_vec(U,V))

U_record = []
V_record = []

U_record.append(U)
V_record.append(V)

for ti in range(1,Nt):
    U_new = np.linalg.solve(A_u, B_u.dot(U) + f_vec(U,V))
    V_new = np.linalg.solve(A_v, B_v.dot(V) - f_vec(U,V))
    
    U = U_new
    V = V_new
    
    U_record.append(U)
    V_record.append(V)

# plt.ylim((0., 2.1))
# plt.xlabel('x'); plt.ylabel('concentration')
# plt.plot(x_grid, U)
# plt.plot(x_grid, V)
# plt.show()

U_record = np.array(U_record)
V_record = np.array(V_record)

fig, ax = plt.subplots()
plt.xlabel('x'); plt.ylabel('t')
heatmap = ax.pcolor(x_grid, t_grid, U_record, vmin=0., vmax=1.2)
