# imports
import math

import matplotlib.pyplot as plt
import numpy as np

# Givens
T = 1
N = 101
A = 0
B = T
h = (T/4 + T/4)/N
a = [0.0] * N
b = [0.0] * N
terms = 10  # Number of terms

# Exact Values
a_e = [0.3183098861837907, 0.5, 0.2122065907891938,
       0, -0.04244131815783876, 0, 0.01818913635335947,
       0, -0.01010507575186637, 0, 0.00643050275118769] * int(terms/10)
b_e = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] * int(terms/10)

# Calculating a0 term
for t in range(0, N+1):
  d = -T/4 + t*h
  if (t == 0 or t == N):
    a[0] += math.cos(2*math.pi*d/T)
  elif ( t%2 == 0 and t != 0):
    a[0] += 2*math.cos(2*math.pi*d/T)
  else:
    a[0] += 4*math.cos(2*math.pi*d/T)
a[0] *= (1/T)*(h/3)

# Calculating a1 - a10 terms
for n in range(1, terms+1):
  for t in range( 0, N+1 ):
    d = -T/4 + t*h
    if (t == 0 or t == N):
      a[n] += math.cos(2*math.pi*d/T)*math.cos(n*2*math.pi*d/T)
    elif ( t%2 == 0 and t != 0):
      a[n] += 2*math.cos(2*math.pi*d/T)*math.cos(n*2*math.pi*d/T)
    else:
      a[n] += 4*math.cos(2*math.pi*d/T)*math.cos(n*2*math.pi*d/T)
  a[n] *= (2/T)*(h/3)

# Calculating b1 - b10 terms
for n in range(1, terms+1):
  for t in range( 0, N+1 ):
    d = -T/4 + t*h
    if (t == 0 or t == N):
      b[n] += math.cos(2*math.pi*d/T)*math.sin(n*2*math.pi*d/T)
    elif ( t%2 == 0 and t != 0):
      b[n] += 2*math.cos(2*math.pi*d/T)*math.sin(n*2*math.pi*d/T)
    else:
      b[n] += 4*math.cos(2*math.pi*d/T)*math.sin(n*2*math.pi*d/T)
  b[n] *= (2/T)*(h/3)
print("╔═══════════════╦══════════════════════════╦════════════════════════╦═══════════════════════════╗")
print("║ Coefficients: ║    Numerical Values:     ║      Exact Values:     ║     Difference Error:     ║")
print("╠═══════════════╬══════════════════════════╬════════════════════════╬═══════════════════════════╣")
for i in range(0,terms+1):
  print("║      a{0:<8}║ {1:< 25}║ {2:^23}║   {3:<24}║". format(i, a[i], a_e[i], abs(a[i]-a_e[i])))
for i in range(1,terms+1):
  print("║      b{0:<8}║ {1:< 25}║ {2:^23}║   {3:<24}║". format(i, b[i], b_e[i], abs(b[i]-b_e[i])))
print("╚═══════════════╩══════════════════════════╩════════════════════════╩═══════════════════════════╝")
# number of timesteps
steps = 2000
f = [a[0]] * steps
# width of timestep
w = (T + B - A)/steps
for t in range(steps):
  d = 0 + t*w
  for i in range(1, terms+1):
    f[t] += a[i]*math.cos(i*2*math.pi*d/T) + b[i]*math.sin(i*2*math.pi*d/T)

f_np = np.array(f)

# Add a title
plt.title('Fourier Series Waveform')
# Add X and Y Label
plt.xlabel('t (ms)')
plt.ylabel('f(t)')
plt.plot(f_np)
plt.show()
