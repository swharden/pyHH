import sys
import os
if not os.path.exists("./src/pyhh/__init__.py"):
    raise Exception("script must be run in project root folder")
sys.path.append("./src")

import numpy as np
import matplotlib.pyplot as plt
import pyhh


class Simulation:

    def __init__(self, model=pyhh.HHModel()):
        self.model = model
        self.CreateArrays(0, 0)
        pass

    def CreateArrays(self, pointCount, deltaTms):
        self.times = np.arange(pointCount) * deltaTms
        self.Vm = np.empty(pointCount)
        self.INa = np.empty(pointCount)
        self.IK = np.empty(pointCount)
        self.IKleak = np.empty(pointCount)
        self.StateN = np.empty(pointCount)
        self.StateM = np.empty(pointCount)
        self.StateH = np.empty(pointCount)

    def Run(self, durationSec=0.1, deltaTms=0.05):
        iterations = int(durationSec * 1000 / deltaTms)
        self.CreateArrays(iterations, deltaTms)
        for i in range(iterations):
            if (i > 1 and i % 1000 == 0):
                percent = int(100*(i+1)/iterations)
                print(f"simulating... {percent}%")
            self.model.iterate(stimulusCurrent=10)
            self.Vm[i] = self.model.Vm
            self.StateH[i] = self.model.h.state
            self.StateM[i] = self.model.m.state
            self.StateN[i] = self.model.n.state
        print("simulation complete")


if __name__ == "__main__":

    sim = Simulation()
    sim.Run()

    plt.figure(figsize=(10, 6))

    ax1 = plt.subplot(211)
    ax1.plot(sim.times, sim.Vm - 70, color='b')
    ax1.set_ylabel("Membrane Potential (mV)")
    ax1.set_title("Hodgkin-Huxley Spiking Neuron Model", fontSize=16)

    ax2 = plt.subplot(212, sharex=ax1)
    ax2.plot(sim.times, sim.StateH, label='h')
    ax2.plot(sim.times, sim.StateM, label='m')
    ax2.plot(sim.times, sim.StateN, label='n')
    ax2.set_ylabel("Open State")
    ax2.legend()

    plt.tight_layout()
    plt.savefig("tests/demo.png")
    plt.show()
