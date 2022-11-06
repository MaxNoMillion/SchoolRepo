# imports
import matplotlib.pyplot as plt
import numpy as np
import numpy.fft as fft
from scipy import signal as sig

# Selector:
  # 0 - Orginal Wave
  # 1 - FFT at 64 Samples
  # 2 - FFT at 256 Samples

Selector = 0

# Setting up f
freq = 10**3
T = 1/freq
t = np.arange(0, T*3, T/20)
f = 0.5 * ( 1 + sig.square(2 * np.pi * freq * t))

hf = f * np.hamming(len(f)) # Multiplying f by hamming window function

# PLotting hf
if Selector == 0:
  plt.plot(hf)
  xticks = [i for i in range(0, 301, 50)]
  xticks_labels = [i for i in range(0, 61, 10)]
  plt.xticks(xticks_labels, xticks)
  plt.title('Square Wave with Hamming Window - (10kHz)')
  plt.ylabel("Amplitude")
  plt.xlabel("Time(us)")

hFr64 = fft.fft(hf, n = 64) # FFT of hf at 64 samples

# Plotting hFr at 64 Samples
if Selector == 1:
  plt.plot(np.abs(hFr64))
  plt.title('FFT - 64 Samples')
  plt.ylabel("Magintude")

hFr256 = fft.fft(hf, n = 256) # FFT of hf at 64 samples

# Plotting hFr at 256 Samples
if Selector == 2:
  plt.plot(np.abs(hFr256))
  plt.title('FFT - 256 Samples')
  plt.ylabel("Magintude")


plt.show()
