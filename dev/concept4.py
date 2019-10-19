import matplotlib.pyplot as plt
import numpy as np


class HHModel:
    """The HHModel tracks conductances of 3 channels to calculate Vm"""

    class Gate:
        """The Gate object manages a channel's open state"""
        alpha, beta, state = 0, 0, 0

        def update(self, deltaTms):
            alphaState = self.alpha * (1-self.state)
            betaState = self.beta * self.state
            self.state += deltaTms * (alphaState - betaState)

    ENa, EK, EKleak = 115, -12, 10.6
    gNa, gK, gKleak = 120, 36, 0.3
    m, n, h = Gate(), Gate(), Gate()
    Cm = 1

    def __init__(self, startingVoltage=0, deltaTms=0.05):
        self.Vm = startingVoltage
        self.deltaTms = deltaTms

    def Iterate(self, stimulusCurrent=0):
        # calculate alpha and beta for every gate using our latest Vm
        self.n.alpha = .01 * ((10-self.Vm) / (np.exp((10-self.Vm)/10)-1))
        self.n.beta = .125*np.exp(-self.Vm/80)
        self.m.alpha = .1*((25-self.Vm) / (np.exp((25-self.Vm)/10)-1))
        self.m.beta = 4*np.exp(-self.Vm/18)
        self.h.alpha = .07*np.exp(-self.Vm/20)
        self.h.beta = 1/(np.exp((30-self.Vm)/10)+1)

        # calculate channel currents using our new gate time constants
        INa = np.power(self.m.state, 3) * self.gNa * \
            self.h.state*(self.Vm-self.ENa)
        IK = np.power(self.n.state, 4) * self.gK * (self.Vm-self.EK)
        IKleak = self.gKleak * (self.Vm-self.EKleak)

        # calculate total membrane current
        Isum = stimulusCurrent - INa - IK - IKleak

        # calculate new Vm using membrane current for a step size and Cm
        self.Vm += self.deltaTms * Isum / self.Cm

        # calculate new channel states using latest Vm
        self.n.update(self.deltaTms)
        self.m.update(self.deltaTms)
        self.h.update(self.deltaTms)

        return self.Vm


if __name__ == "__main__":

    hh = HHModel()
    simulationLengthMsec = 200
    simulationPoints = int(simulationLengthMsec / hh.deltaTms)
    voltages = np.empty(simulationPoints)
    times = np.arange(simulationPoints) * hh.deltaTms

    for i in range(len(times)):
        hh.Iterate(stimulusCurrent=20)
        voltages[i] = hh.Vm
        # note: you can also plot hh's n, m, and k (channel open states)

    plt.figure(figsize=(10, 4))
    plt.plot(times, voltages)
    plt.ylabel("Membrane Potential (mV)")
    plt.xlabel("Simulation Time (milliseconds)")
    plt.title("Hodgkin-Huxley Spiking Neuron Model", fontSize=16)
    plt.tight_layout()
    plt.savefig("dev/concept4.png")
    plt.show()
