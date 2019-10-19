import sys
import os
if not os.path.exists("./src/pyhh/__init__.py"):
    raise Exception("script must be run in project root folder")
sys.path.append("./src")

import numpy as np
import matplotlib.pyplot as plt
import pyhh

if __name__ == "__main__":

    # customize a neuron model
    model = pyhh.HHModel()
    model.gNa = 100 # typically 120
    model.gK = 5 # typically 36
    model.EK = -35 # typically -12

    # customize a stimulus waveform
    stim = np.zeros(2000)
    stim[700:1300] = 50 # add a square pulse

    # run a simulation on the model
    sim = pyhh.Simulation(model)
    sim.Run(stimulusCurrent=stim)

    # plot the results with MatPlotLib
    plt.figure(figsize=(10, 6))

    ax1 = plt.subplot(311)
    ax1.plot(sim.times, sim.Vm - 70, color='b')
    ax1.set_ylabel("Membrane Potential (mV)")
    ax1.set_title("Hodgkin-Huxley Spiking Neuron Model", fontSize=16)

    ax2 = plt.subplot(312)
    ax2.plot(sim.times, stim, color='r')
    ax2.set_ylabel("Stimulation")

    ax3 = plt.subplot(313, sharex=ax1)
    ax3.plot(sim.times, sim.StateH, label='h')
    ax3.plot(sim.times, sim.StateM, label='m')
    ax3.plot(sim.times, sim.StateN, label='n')
    ax3.set_ylabel("Open State")
    ax3.set_xlabel("Simulation Time (milliseconds)")
    ax3.legend()

    plt.tight_layout()
    plt.savefig("tests/demo.png")
    plt.show()
