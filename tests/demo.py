import sys
import os
if not os.path.exists("./src/pyhh/__init__.py"):
    raise Exception("script must be run in project root folder")
sys.path.append("./src")

import numpy as np
import matplotlib.pyplot as plt
import pyhh

if __name__ == "__main__":

    # customize a neuron model if desired
    model = pyhh.HHModel()
    model.gNa = 100  # typically 120
    model.gK = 5  # typically 36
    model.EK = -35  # typically -12

    # customize a stimulus waveform
    stim = np.zeros(20000)
    stim[7000:13000] = 50  # add a square pulse

    # simulate the model cell using the custom waveform
    sim = pyhh.Simulation(model)
    sim.Run(stimulusWaveform=stim, stepSizeMs=0.01)

    # plot the results with MatPlotLib
    plt.figure(figsize=(10, 8))

    ax1 = plt.subplot(411)
    ax1.plot(sim.times, sim.Vm - 70, color='b')
    ax1.set_ylabel("Potential (mV)")
    ax1.set_title("Hodgkin-Huxley Spiking Neuron Model", fontSize=16)

    ax2 = plt.subplot(412)
    ax2.plot(sim.times, stim, color='r')
    ax2.set_ylabel("Stimulation (µA/cm²)")

    ax3 = plt.subplot(413, sharex=ax1)
    ax3.plot(sim.times, sim.StateH, label='h')
    ax3.plot(sim.times, sim.StateM, label='m')
    ax3.plot(sim.times, sim.StateN, label='n')
    ax3.set_ylabel("Activation (frac)")
    ax3.legend()

    ax4 = plt.subplot(414, sharex=ax1)
    ax4.plot(sim.times, sim.INa, label='VGSC')
    ax4.plot(sim.times, sim.IK, label='VGKC')
    ax4.plot(sim.times, sim.IKleak, label='KLeak')
    ax4.set_ylabel("Current (µA/cm²)")
    ax4.set_xlabel("Simulation Time (milliseconds)")
    ax4.legend()

    plt.tight_layout()
    plt.savefig("tests/demo.png")
    plt.show()
