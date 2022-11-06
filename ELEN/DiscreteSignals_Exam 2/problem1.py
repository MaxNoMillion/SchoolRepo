# imports
import cmath

import matplotlib.pyplot as plt
import numpy as np

# Part A
f = np.zeros([4])
for i in range(4):
  f[i] = ((0.6)**i)

print("Part A:")
print(f)

# Part B
f_k = np.zeros([8], dtype = np.complex128)
for i in range(4):
  f_k[i] = f[i]

print()
print("Part B:")
print(f"f_k = [", end = '')
for i in range(len(f_k)):
  if i != len(f_k) - 1:
    print(f"{round(f_k[i].real, 4)}, ", end = ' ')
  else:
    print(f"{round(f_k[i].real, 4)}]")

print()

N_0 = 8
Omega_0 = (2*cmath.pi) / N_0
F = np.zeros([8], dtype = np.complex128)

for r in range(N_0):
  i = 0
  for item in f_k:
    F[r] += item * cmath.exp(-1j * r * Omega_0 * i)
    i += 1

for r in range(len(F)):
  if F[r].imag >= 0j:
    print(f"F[{r}] = {round(F[r].real, 4)} +{round(F[r].imag, 4)}j")
  else:
    print(f"F[{r}] = {round(F[r].real, 4)} {round(F[r].imag, 4)}j")

print()

print("Part C:")
f = np.zeros([8])
for i in range(8):
  f[i] = ((0.6)**i)

Omegas = np.array([0, cmath.pi/4, cmath.pi/2, 3*cmath.pi/4, cmath.pi, 5*cmath.pi/4, 3*cmath.pi/2, 7*cmath.pi/4])
Omegas_formatting = ["0", "pi/4", "pi/2", "3pi/4", "pi", "5pi/4", "3pi/2", "7pi/4"]

F1 = np.zeros([8], dtype = np.complex128)

for r in range(len(F1)):
  i = 0
  for item in f:
    F1[r] += item * cmath.exp(-1j * Omegas[r] * i)
    i += 1

for r in range(len(F1)):
  if F1[r].imag >= 0j:
    print(f"F[{Omegas_formatting[r]}] = {round(F1[r].real, 4)} +{round(F1[r].imag, 4)}j")
  else:
    print(f"F[{Omegas_formatting[r]}] = {round(F1[r].real, 4)} {round(F1[r].imag, 4)}j")
