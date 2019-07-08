from matplotlib import pyplot as plt
import ring_evolve as re
import numpy as np
import config_ring as config

steps = 3

with np.load('Class_data_0.20.npz') as data:
    inputs = data['inp_wvfrm'][::steps,:].T
    inputs[0,0:46]=inputs[0,0:46]*0.2
    inputs[1,0:46]=inputs[1,0:46]*0.2
    print('Input shape: ', inputs.shape)
    labels = data['target'][::steps]
    print('Target sgape ', labels.shape)

mask0 = labels==0
mask1 = labels==1
labels[mask0] = 1
labels[mask1] = 0
cf = config.experiment_config(inputs, labels)
target_wave = cf.TargetGen
t, inp_wave, weights = cf.InputGen
plt.figure()
plt.plot(t,inp_wave.T)
plt.plot(t,target_wave,'k')
plt.show()
#print(sys.path)
#_,_,_,_ = re.evolve(inputs,labels)

try:
    re.reset(0, 0)
except:
    pass