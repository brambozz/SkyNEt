#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 15 16:32:25 2018
This script generates all binary assignments of N elements.
@author: hruiz and ualegre
"""
import numpy as np
from vc_dimension_test import VCDimensionTest


class CapacityTest():

    def __init__(self, configs):
        self.configs = configs
        self.current_dimension = configs.from_dimension
        self.threshold = self.__calculate_threshold()
        self.vcdimension_test = VCDimensionTest()

    def run_test(self):
        veredict = True
        while veredict is True:
            print('Generating inputs for VC Dimension %d: ' % self.current_dimension)
            inputs = self.generate_test_inputs(self.current_dimension)
            binary_labels = self.__generate_binary_target(self.current_dimension).tolist()
            for i in range(self.configs.max_opportunities):
                veredict, binary_labels = self.vcdimension_test.run_test(inputs, binary_labels, self.threshold)
                if veredict:
                    break
            if self.__next_vcdimension() is False:
                break

    def __calculate_threshold(self):
        return self.configs.threshold_numerator / self.current_dimension

    def __next_vcdimension(self):
        if self.current_dimension + 1 > self.configs.to_dimension:
            return False
        else:
            self.current_dimension = + 1
            self.__calculate_threshold()

    # @todo change generation of inputs to differetn vc dimensions
    def generate_test_inputs(self, vc_dim):
        #@todo create a function that automatically generates non-linear inputs
        try:
            if vc_dim == 4:
                return [[-0.7,-0.7,0.7,0.7],[0.7,-0.7,0.7,-0.7]]
            elif vc_dim == 5:
                return [[-0.7,-0.7,0.7,0.7,-0.35],[0.7,-0.7,0.7,-0.7,0.0]]
            elif vc_dim == 6:
                return [[-0.7,-0.7,0.7,0.7,-0.35,0.35],[0.7,-0.7,0.7,-0.7,0.0,0.0]]
            elif vc_dim == 7:
                return [[-0.7,-0.7,0.7,0.7,-0.35,0.35,0.0],[0.7,-0.7,0.7,-0.7,0.0,0.0,1.0]]
            elif vc_dim == 8:
                return [[-0.7,-0.7,0.7,0.7,-0.35,0.35,0.0,0.0],[0.7,-0.7,0.7,-0.7,0.0,0.0,1.0,-1.0]]
            else:
                raise VCDimensionException()
        except VCDimensionException:
            print('Dimension Exception occurred. The selected VC Dimension is %d Please insert a value between ' % vc_dim)

    def __generate_binary_target(self, target_dim):
        # length of list, i.e. number of binary targets
        binary_target_no = 2**target_dim
        assignments = []
        list_buf = []

        # construct assignments per element i
        print('===' * target_dim)
        print('ALL BINARY LABELS:')
        level = int((binary_target_no / 2))
        while level >= 1:
            list_buf = []
            buf0 = [0] * level
            buf1 = [1] * level
            while len(list_buf) < binary_target_no:
                list_buf += (buf0 + buf1)
            assignments.append(list_buf)
            level = int(level / 2)

        binary_targets = np.array(assignments).T
        print(binary_targets)
        print('===' * target_dim)
        return binary_targets


class CapacityTestConfigs():
    def __init__(self, from_dimension=1, to_dimension=4, voltage_false=-1.,
                voltage_true=0.4, threshold_numerator=1-0.5, max_opportunities=3):
        self.from_dimension = from_dimension
        self.to_dimension = to_dimension
        self.voltage_false = voltage_false
        self.voltage_true = voltage_true
        self.max_opportunities = max_opportunities # Maximum number of opportunities given to find all the gates
        # The threshold is calculated as: threshold_numerator/vc_dimension
        # Create binary labels for N samples
        # bad_gates = # for N=6 on model [51]
        self.threshold_numerator = threshold_numerator
        # self.threshold = (1-0.5/self.N)  # 1-(0.65/N)*(1+1.0/N)
        # print('Threshold for acceptance is set at: ', self.threshold)


class VCDimensionException(Exception):
    """Exception: It does not exist an implementation of such VC Dimension."""
    pass


if __name__ == '__main__':
    test = CapacityTest(CapacityTestConfigs(from_dimension=4))
    test.run_test()
