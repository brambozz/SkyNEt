''''
Main handler of the SkyNEt platform
'''
# Import packages
import modules.ReservoirSparse as Reservoir
import modules.PlotBuilder as PlotBuilder
import modules.GenerateInput as GenerateInput
import math
# temporary imports
import numpy as np

# Read config.txt file
exec(open("config.txt").read())

# Init software reservoir
print("Initializing the reservoir...")
res = Reservoir.Network(nodes, inputscaling, spectralradius, weightdensity)

# Obtain benchmark input
[t, inp] = GenerateInput.softwareInput(benchmark, SampleFreq, WavePeriods, WaveFrequency)
# Obtain benchmark output
[t, outp] = GenerateInput.targetOutput(benchmark, SampleFreq, WavePeriods, WaveFrequency)

print("Feeding the input signal...")
printcounter = 0
for i in range(len(inp)):
    if (printcounter == math.floor(len(inp) / 10)):
        print('%d%% completed' % ((i / len(inp)) * 100), end='\r')
        printcounter = 0
    else:
        printcounter += 1
    res.update_reservoir(inp[i])

trained_output = res.train_reservoir_ridgereg(outp, rralpha, skipstates)
# trained_output = res.train_reservoir_pseudoinv(outp, skipstates)
trainplusideal = np.c_[trained_output, outp[skipstates:]]

# temporary plot
y = np.empty((len(t), 5))
for i in range(5):
    y[:,i] = res.collect_state[:, i]

PlotBuilder.genericPlot(t, y, 'Time (A.U.)', 'Output (A.U.)', 'Example reservoir states')
PlotBuilder.genericPlot(t[skipstates:], trainplusideal, 'Time (A.U.)', 'Output (A.U.)', 'trained_output')