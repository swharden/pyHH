"""
Hodgkin-Huxley Model Neuron Simulated Discretely with Python
Inspired by matlab code on "andy's brain blog" Oct 15 2013.
"""

import matplotlib.pyplot as plt
import numpy as np

# Simulation time (milliseconds)
simulationTime = 200
deltaT = .01
pointsPerMillisec = 1.0/deltaT
t = np.arange(simulationTime/deltaT) * deltaT

# Externally applied current across time (Suggested values: 3, 20, 50, 1000)
I = np.zeros(len(t))
indexPulseStart = int(100 * pointsPerMillisec)
indexPulseEnd = int(150 * pointsPerMillisec)
I[indexPulseStart:indexPulseEnd] = 50

# Kinetics (Table 3)
gK = 36
gNa = 120
g_L = .3
E_K = -12
E_Na = 115
E_L = 10.6
C = 1

# Initial States
V = 0  # Baseline voltage
alpha_n = .01 * ((10-V) / (np.exp((10-V)/10)-1))  # Equation 12
beta_n = .125*np.exp(-V/80)  # Equation 13
alpha_m = .1*((25-V) / (np.exp((25-V)/10)-1))  # Equation 20
beta_m = 4*np.exp(-V/18)  # Equation 21
alpha_h = .07*np.exp(-V/20)  # Equation 23
beta_h = 1/(np.exp((30-V)/10)+1)  # Equation 24

# Conductances over time
n = np.empty(len(t))
m = np.empty(len(t))
h = np.empty(len(t))
V = np.empty(len(t))

# Initial conductances
n[0] = alpha_n/(alpha_n+beta_n)  # Equation 9
m[0] = alpha_m/(alpha_m+beta_m)  # Equation 18
h[0] = alpha_h/(alpha_h+beta_h)  # Equation 18

# Simulate
for i in range(1, len(t)-1):

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

plt.figure()

ax1 = plt.subplot(211)
ax1.plot(t, V)

ax2 = plt.subplot(212, sharex=ax1)
ax2.plot(t, gK*np.power(n, 4), label='Potassium')
ax2.plot(t, gNa*np.power(m, 3)*h, label='Sodium')
ax2.set_ylabel("Conductance")
ax2.set_xlabel("Time (milliseconds)")
plt.legend()

plt.tight_layout()
plt.show()
