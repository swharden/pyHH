import matplotlib.pyplot as plt
import numpy as np

# adapted from https://www.bonaccorso.eu/2017/08/19/hodgkin-huxley-spiking-neuron-model-python/

# simulation time (millisecond units)
tmin = 0.0
tmax = 50.0
T = np.linspace(tmin, tmax, 10000)

# channel conductances (mS/cm^2)
gK = 36.0
gNa = 120.0
gL = 0.3  # leak

# ion reversal potentials (mV)
VK = -12.0
VNa = 115.0
Vl = 10.613  # Leak

# membrane properties
Cm = 1.0  # capacitance (uF/cm^2)

# Potassium ion-channel rate functions


def alpha_n(Vm):
    return (0.01 * (10.0 - Vm)) / (np.exp(1.0 - (0.1 * Vm)) - 1.0)


def beta_n(Vm):
    return 0.125 * np.exp(-Vm / 80.0)

# Sodium ion-channel rate functions


def alpha_m(Vm):
    return (0.1 * (25.0 - Vm)) / (np.exp(2.5 - (0.1 * Vm)) - 1.0)


def beta_m(Vm):
    return 4.0 * np.exp(-Vm / 18.0)


def alpha_h(Vm):
    return 0.07 * np.exp(-Vm / 20.0)


def beta_h(Vm):
    return 1.0 / (np.exp(3.0 - (0.1 * Vm)) + 1.0)

# n, m, and h steady-state values


def n_inf(Vm=0.0):
    return alpha_n(Vm) / (alpha_n(Vm) + beta_n(Vm))


def m_inf(Vm=0.0):
    return alpha_m(Vm) / (alpha_m(Vm) + beta_m(Vm))


def h_inf(Vm=0.0):
    return alpha_h(Vm) / (alpha_h(Vm) + beta_h(Vm))

# Input stimulus


def Id(t):
    if 0.0 < t < 1.0:
        return 150.0
    elif 10.0 < t < 11.0:
        return 50.0
    return 0.0

# Compute derivatives


def compute_derivatives(y, t0):
    dy = np.zeros((4,))

    Vm = y[0]
    n = y[1]
    m = y[2]
    h = y[3]

    # dVm/dt
    GK = (gK / Cm) * np.power(n, 4.0)
    GNa = (gNa / Cm) * np.power(m, 3.0) * h
    GL = gL / Cm

    dy[0] = (Id(t0) / Cm) - (GK * (Vm - VK)) - \
        (GNa * (Vm - VNa)) - (GL * (Vm - Vl))

    # dn/dt
    dy[1] = (alpha_n(Vm) * (1.0 - n)) - (beta_n(Vm) * n)

    # dm/dt
    dy[2] = (alpha_m(Vm) * (1.0 - m)) - (beta_m(Vm) * m)

    # dh/dt
    dy[3] = (alpha_h(Vm) * (1.0 - h)) - (beta_h(Vm) * h)

    return dy


# State (Vm, n, m, h)
Y = np.array([0.0, n_inf(), m_inf(), h_inf()])

# Solve ODE system
from scipy.integrate import odeint
Vy = odeint(compute_derivatives, Y, T)

voltage = Vy[:, 0]
dndt = Vy[:, 1]
dmdt = Vy[:, 2]
dhdt = Vy[:, 3]

plt.figure()

ax1 = plt.subplot(211)
ax1.plot(voltage)

ax2 = plt.subplot(212, sharex = ax1)
ax2.plot(dndt, label="dn/dt")
ax2.plot(dmdt, label="dm/dt")
ax2.plot(dhdt, label="dh/dt")
ax2.legend()

plt.tight_layout()
plt.show()
