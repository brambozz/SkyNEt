# -*- coding: utf-8 -*-
"""
Created on Mon Dec 17 16:51:29 2018

Script to characterize a device using partially a grid and partially sine wave 
functions
@author: Mark
"""
# Import packages
import SkyNEt.modules.SaveLib as SaveLib
from SkyNEt.instruments import InstrumentImporter
import time
from SkyNEt.experiments.wave_search import transient_test
import SkyNEt.experiments.wave_search.config_wave_search as config
# temporary imports
import numpy as np

#%% Initialization of saving config file
configSrc = config.__file__

# Initialize config object
cf = config.experiment_config()

# initialize save directory
saveDirectory = SaveLib.createSaveDirectory(cf.filepath, cf.name)

# Initialize output data set
data = np.zeros((1, int(cf.sampleTime * cf.fs)))

batches = int(cf.fs * cf.sampleTime / cf.samplePoints)

for i in range(0, batches):
    start_wave = time.time()
    
    t = np.linspace(i * cf.samplePoints, (i + 1) * cf.samplePoints - 1, cf.samplePoints)
    waves = cf.generateSineWave(cf.freq, t, cf.Vmax, cf.fs)
    # Use 0.05 second to ramp up to the value where data aqcuisition stopped previous iteration
    # and 0.05 second to ramp down after the batch is done
    wavesRamped = np.zeros((waves.shape[0], waves.shape[1] + int(0.1*cf.fs))) 
    dataRamped = np.zeros((1,wavesRamped.shape[1]))
    for j in range(wavesRamped.shape[0]):
        wavesRamped[j,0:int(0.05*cf.fs)] = np.linspace(0,waves[j,0], int(0.05*cf.fs))
        wavesRamped[j,int(0.05*cf.fs): int(0.05*cf.fs) + waves.shape[1]] = waves[j,:]
        wavesRamped[j,int(0.05*cf.fs) + waves.shape[1]:] = np.linspace(waves[j,-1], 0, int(0.05*cf.fs))
        
    dataRamped = InstrumentImporter.nidaqIO.IO_cDAQ(wavesRamped, cf.fs)      
    data[0, i*cf.samplePoints: (i+1)*cf.samplePoints] = dataRamped[:, int(0.05*cf.fs):int(0.05*cf.fs) + waves.shape[1]]
    end_wave = time.time()
    print('Data collection for part ' + str(i+1) + ' of ' + str(batches) + ' took '+str(end_wave-start_wave)+' sec.')


if cf.transientTest:
    print("Testing for transients...")
    print("Only for the last loaded data transients are tested for convenience")
    ytestdata, difference, xtestdata = transient_test.transient_test(waves, data[0, (batches-1)*cf.samplePoints:(batches)*cf.samplePoints], cf.fs, cf.sampleTime, cf.n)
    SaveLib.saveExperiment(cf.configSrc, saveDirectory, 
    						xtestdata = xtestdata, 
    						ytestdata = ytestdata*cf.amplification/cf.postgain, \
                            diff = difference*cf.amplification/cf.postgain, \
                            output = data*cf.amplification/cf.postgain, 
                            freq = cf.freq,
    						sampleTime = cf.sampleTime,
    						fs = cf.fs,
    						phase = cf.phase,
    						Vmax = cf.Vmax,
                            filename = 'training_NN_data')
else:
    SaveLib.saveExperiment(cf.configSrc, saveDirectory, 
    						output = data*cf.amplification/cf.postgain,
    						freq = cf.freq,
    						sampleTime = cf.sampleTime,
    						fs = cf.fs,
    						phase = cf.phase,
    						Vmax = cf.Vmax,
    						filename = 'training_NN_data')
  

InstrumentImporter.reset(0,0)
