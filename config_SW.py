import numpy as np 

class experiment_config(object):

    def __init__(self):

        #define where you want to save the data.
        self.filepath = r'D:\Aernout\test'
        self.name = test

        #define the constants
        self.v_low = 0
        self.v_high = 0.1
        self.n_points = 10000
        self.position = 'high'

        #define the input and output amplification
        self.amplification = 1
        self.source_gain = 1

        #measurement tool settings.
        self.device = 'nidaq'
        self.fs = 8000

        def SquareWave(self, v_high, v_low, n_points):
            i = 0
            if position == 'high':
                for i in range(0, int((n_points/2)-1)):
                    input = v_high
                    i = i+1
                for i in range (int(n_points/2), int(n_points-1)):
                    input = 'v_low'
                    i = i+1
            else:
                input = 'v_low'