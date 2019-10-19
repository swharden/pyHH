import numpy as np


class Simulation:

    def __init__(self, model):
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

    def Run(self, stimulusCurrent=0, durationSec=0.1, deltaTms=0.05):
        if isinstance(stimulusCurrent, np.ndarray):
            iterations = len(stimulusCurrent)
        else:
            iterations = int(durationSec * 1000 / deltaTms)
        self.CreateArrays(iterations, deltaTms)
        for i in range(iterations):
            if (i > 1 and i % 1000 == 0):
                percent = int(100*(i+1)/iterations)
                print(f"simulating... {percent}%")
            if isinstance(stimulusCurrent, np.ndarray):
                self.model.iterate(stimulusCurrent=stimulusCurrent[i])
            else:
                self.model.iterate(stimulusCurrent=float(stimulusCurrent))
            self.Vm[i] = self.model.Vm
            self.StateH[i] = self.model.h.state
            self.StateM[i] = self.model.m.state
            self.StateN[i] = self.model.n.state
        print("simulation complete")
