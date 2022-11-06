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
t = np.arange(0, 3*T, T/20)
f = 0.5 * ( 1 + sig.square(2 * np.pi * freq * t))

# Plotting Original SquareWave
if Selector == 0:
  plt.plot(f)
  xticks = [i for i in range(0, 301, 50)]
  xticks_labels = [i for i in range(0, 61, 10)]
  plt.xticks(xticks_labels, xticks)
  plt.title('Square Wave - (10kHz)')
  plt.ylabel("Amplitude")
  plt.xlabel("Time(us)")

Fr64 = fft.fft(f, n = 64) # FFT of f at 64 samples

# Plotting DFT at 64 Samples
if Selector == 1:
  plt.plot(np.abs(Fr64))
  plt.title('FFT - 64 Samples')
  plt.ylabel("Magintude")

Fr256 = fft.fft(f, n = 256) # FFT of f at 256 samples

# Plotting DFT at 256 Samples
if Selector == 2:
  plt.plot(np.abs(Fr256))
  plt.title('FFT - 256 Samples')
  plt.ylabel("Magintude")

plt.show()
