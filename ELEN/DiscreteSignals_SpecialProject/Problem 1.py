
# imports
import matplotlib.pyplot as plt
import numpy as np
import numpy.fft as fft

# Setting up f and padding zeros
N = 16
f = np.zeros(N)
f[0], f[1], f[2] = 3.0, 2.0, 3.0
Fr = fft.fft(f, n=N)  # Taking FFT

r = np.zeros(N)
for i in range(N):
  r[i] = i

# Plotting f[k]
plt.subplot(3, 1, 1)
plt.stem(r, f)
plt.xlabel("k")
plt.ylabel("f[k]")
plt.grid(visible = True)

# Plotting magnitude of Fr
plt.subplot(3, 1, 2)
plt.stem(r, np.abs(Fr))
plt.xlabel("r")
plt.ylabel("Fr")
plt.grid(visible = True)

# Plotting phase of Fr
plt.subplot(3, 1, 3)
plt.stem(r, np.angle(Fr))
plt.xlabel("r")
plt.ylabel("angle Fr")
plt.grid(visible = True)

plt.show()


