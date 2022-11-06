# imports
import matplotlib.pyplot as plt
import numpy as np
import numpy.fft as fft

subGraphNum = 2

##### Part A #####
# Orginal Equation
steps_ori = 1000
T = 1000
N = 8
f_ori = np.zeros(steps_ori)
w = T/steps_ori
for k in range(steps_ori):
  f_ori[k] = 0.8**(k*w)

#Plotting Orginal Equation (Continuous)
plt.subplot(subGraphNum, 1, 1)
plt.plot(np.array([i for i in range(0, steps_ori, int(steps_ori/(N)))]), f_ori[0:8], 'c--', label = 'f(t)')
xticks = [i for i in range(0, steps_ori + int(steps_ori/(N)), int(steps_ori/(N)))]
xticks_labels = [i for i in range(9)]
plt.xticks(xticks, xticks_labels)
plt.grid(visible = True)
plt.title('Original Function')
plt.legend()

# DTFT of orginal
Fr_ori = fft.fft(f_ori, n = 1000)

# Plotting DTFT (Non-Truncated)
plt.subplot(subGraphNum, 1, 2)
plt.plot(np.abs(Fr_ori), 'c--', label = 'DTFT')
xticks = [i for i in range(0, steps_ori + int(steps_ori/(N)), int(steps_ori/(N)))]
xticks_labels = [i for i in range(9)]
plt.xticks(xticks, xticks_labels)
plt.grid(visible = True)
plt.title('Discrete Fourier Transform')
plt.legend()


##### Part B #####
# 8-Point: Original Equation
steps = 200
N = 8
f = np.zeros(steps)
for k in range(N):
  f[k] = 0.8**k

# 8-Point: DTFT of orginal
Fr = fft.fft(f)

# Plotting DTFT (Truncated)
plt.subplot(subGraphNum, 1, 2)
plt.plot(np.array([i for i in range(0, steps_ori, int(steps_ori/steps))]), np.abs(Fr), 'r', label = 'Truncated - DTFT')
plt.ylabel("Fr")
plt.grid(visible = True)
plt.legend()

##### Part C #####
# 8-Point Original Equation
steps_ = 8
N = 8
f = np.zeros(steps_)
for k in range(N):
  f[k] = 0.8**k

# Plotting Original Equation (Discrete)
plt.subplot(subGraphNum, 1, 1)
plt.stem(np.array([i for i in range(0, steps_ori, int(steps_ori/(N)))]), f[0:8], label = 'f[k]')
plt.ylabel("f[k]")
plt.grid(visible = True)
plt.legend()

# 8-Point: DFT of orginal
Fr = fft.fft(f)
print(Fr)  # Print DFT Results

# Plotting DFT
plt.subplot(subGraphNum, 1, 2)
plt.stem(np.array([i for i in range(0, steps_ori, int(steps_ori/(steps_)))]), np.abs(Fr), label = 'DFT')
plt.ylabel("Fr")
plt.grid(visible = True)
plt.legend()

plt.show()
