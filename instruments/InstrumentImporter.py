# This simple file is a wrapper for 
# importing all measurement equipment available in the lab.
# It also (importantly!) sets up a reset function that is executed
# at ctrl-C

from SkyNEt.instruments.ADwin import adwinIO
from SkyNEt.instruments.niDAQ import nidaqIO
from SkyNEt.instruments.DAC import IVVIrack
import signal
import sys

def reset(signum, frame):
        '''
        This functions performs the following reset tasks:
        - Set IVVI rack DACs to zero
        - Apply zero signal to the NI daq
        - Apply zero signal to the ADwin
        '''
        try:
            ivviReset = IVVIrack.initInstrument(name='ivviReset')
            ivviReset.set_dacs_zero()
            print('ivvi DACs set to zero')
        except:
            print('ivvi was not initialized, so also not reset')
			
        try:
            nidaqIO.reset_device()
            print('nidaq has been reset')
        except:
            print('nidaq not connected to PC, so also not reset')

        try:
            global adw
            reset_signal = np.zeros((2, 40003))
            adwinIO.IO_2D(adw, reset_signal, 1000)
        except:
            print('adwin was not initialized, so also not reset')

        # Finally stop the script execution
        sys.exit()
	
# Set up reset call at ctrl-C
signal.signal(signal.SIGINT, reset)
