"""
Hodgkin-Huxley Model Neuron Simulated Discretely with Python
Inspired by matlab code on "andy's brain blog" Oct 15 2013.
"""

import matplotlib.pyplot as plt
import numpy as np

# Simulation time (all time units are milliseconds)
simulationTime = 200
deltaT = .01
pointsPerMillisec = 1.0/deltaT
t = np.arange(simulationTime/deltaT) * deltaT

# Create the stimulus waveform
I = np.zeros(len(t))

# Add some square pulses to the stimulus waveform
I[int(125 * pointsPerMillisec):int(175 * pointsPerMillisec)] = 50
I[int(25 * pointsPerMillisec):int(75 * pointsPerMillisec)] = 10

# channel conductances (mS/cm^2)
gK = 36
gNa = 120
g_L = .3

# ion reversal potentials (mV)
E_K = -12
E_Na = 115
E_L = 10.6

# membrane properties
C = 1.0  # capacitance (uF/cm^2)

# Open state over time (start at zero)
n = np.zeros(len(t))
m = np.zeros(len(t))
h = np.zeros(len(t))
V = np.zeros(len(t))

# Initial States
Vstart = -0  # Baseline voltage
alpha_n = .01 * ((10-Vstart) / (np.exp((10-Vstart)/10)-1))  # Equation 12
beta_n = .125*np.exp(-Vstart/80)  # Equation 13
alpha_m = .1*((25-Vstart) / (np.exp((25-Vstart)/10)-1))  # Equation 20
beta_m = 4*np.exp(-Vstart/18)  # Equation 21
alpha_h = .07*np.exp(-Vstart/20)  # Equation 23
beta_h = 1/(np.exp((30-Vstart)/10)+1)  # Equation 24

# Initial conductances
n[0] = alpha_n/(alpha_n+beta_n)  # Equation 9
m[0] = alpha_m/(alpha_m+beta_m)  # Equation 18
h[0] = alpha_h/(alpha_h+beta_h)  # Equation 18
V[0] = Vstart

# Simulate
for i in range(len(t)-1):

   # coefficients
    alpha_n = .01 * ((10-V[i]) / (np.exp((10-V[i])/10)-1))
    beta_n = .125*np.exp(-V[i]/80)
    alpha_m = .1*((25-V[i]) / (np.exp((25-V[i])/10)-1))
    beta_m = 4*np.exp(-V[i]/18)
    alpha_h = .07*np.exp(-V[i]/20)
    beta_h = 1/(np.exp((30-V[i])/10)+1)

    # currents
    I_Na = np.power(m[i], 3) * gNa * h[i] * (V[i]-E_Na)
    I_K = np.power(n[i], 4) * gK * (V[i]-E_K)
    I_L = g_L * (V[i]-E_L)
    I_ion = I[i] - I_K - I_Na - I_L

    # calculate derivatives using Euler first order approximation
    V[i+1] = V[i] + deltaT * I_ion / C
    n[i+1] = n[i] + deltaT * (alpha_n * (1-n[i]) - beta_n * n[i])
    m[i+1] = m[i] + deltaT * (alpha_m * (1-m[i]) - beta_m * m[i])
    h[i+1] = h[i] + deltaT * (alpha_h * (1-h[i]) - beta_h * h[i])

# Display Results
V = V-70  # Set resting potential to -70mv

plt.figure(figsize=(8, 8))

ax1 = plt.subplot(411)
ax1.plot(t, V, color='b')
ax1.set_ylabel("Potential (mV)")

ax2 = plt.subplot(412)
ax2.plot(t, I, color='r')
ax2.set_ylabel("Stimulus")

ax3 = plt.subplot(413, sharex=ax1)
ax3.plot(t, gK*np.power(n, 4), label='K')
ax3.plot(t, gNa*np.power(m, 3)*h, label='Na')
ax3.set_ylabel("Conductance")
plt.legend()

ax4 = plt.subplot(414, sharex=ax1)
ax4.plot(t, n, label='K')
ax4.plot(t, m, label='Na')
ax4.set_ylabel("Open State")
ax4.set_xlabel("Time (milliseconds)")
plt.legend()

plt.tight_layout()
plt.savefig("dev/concept3.png")
plt.show()
