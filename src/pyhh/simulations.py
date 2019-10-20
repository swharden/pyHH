import numpy as np
import warnings


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

    def Run(self, stimulusWaveform, stepSizeMs):
        if (stepSizeMs > 0.05):
            warnings.warn("step sizes < 0.05 ms are recommended")
        assert isinstance(stimulusWaveform, np.ndarray)
        self.CreateArrays(len(stimulusWaveform), stepSizeMs)
        print(f"simulating {len(stimulusWaveform)} time points...")
        for i in range(len(stimulusWaveform)):
            self.model.iterate(stimulusWaveform[i], stepSizeMs)
            self.Vm[i] = self.model.Vm
            self.INa[i] = self.model.INa
            self.IK[i] = self.model.IK
            self.IKleak[i] = self.model.IKleak
            self.StateH[i] = self.model.h.state
            self.StateM[i] = self.model.m.state
            self.StateN[i] = self.model.n.state
        print("simulation complete")


assert __name__ != "__main__", "do not execute this module (only import it)"
