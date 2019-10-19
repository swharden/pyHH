import numpy as np

class Gate:
    """The Gate object manages a channel's open state"""
    alpha, beta, state = 0, 0, 0

    def update(self, deltaTms):
        alphaState = self.alpha * (1-self.state)
        betaState = self.beta * self.state
        self.state += deltaTms * (alphaState - betaState)


class HHModel:
    """The HHModel tracks conductances of 3 channels to calculate Vm"""

    ENa, EK, EKleak = 115, -12, 10.6
    gNa, gK, gKleak = 120, 36, 0.3
    m, n, h = Gate(), Gate(), Gate()
    Cm, Vm = 1, 0

    def iterate(self, stimulusCurrent=0, deltaTms=0.05):
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
        self.Vm += deltaTms * Isum / self.Cm

        # calculate new channel states using latest Vm
        self.n.update(deltaTms)
        self.m.update(deltaTms)
        self.h.update(deltaTms)