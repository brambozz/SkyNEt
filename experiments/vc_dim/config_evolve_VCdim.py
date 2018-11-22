import numpy as np
from SkyNEt.config.config_class import config_class
from SkyNEt.modules.GenWaveform import GenWaveform
from SkyNEt.modules.Classifiers import perceptron

class experiment_config(config_class):
    '''This is the experiment configuration file to measure VC dim.
    This experiment_config class inherits from config_class default values that are known to work well with boolean logic.
    You can define user-specific parameters in the construction of the object in __init__() or define
    methods that you might need after, e.g. a new fitness function or input and output generators.
    Remember if you define a new fitness function or generator, you have to redefine the self.Fitness,
    self.Target_gen and self.Input_gen in __init__()

    ----------------------------------------------------------------------------
    Description of general parameters
    ----------------------------------------------------------------------------
    amplification; specify the amount of nA/V. E.g. if you set the IVVI to 100M,
        then amplification = 10
    generations; the amount of generations for the GA
    generange; the range that each gene ([0, 1]) is mapped to. E.g. in the Boolean
        experiment the genes for the control voltages are mapped to the desired
        control voltage range.
    partition; this tells the GA how it will evolve the next generation.
        In order, this will make the GA evolve the specified number with
        - promoting fittest partition[0] genomes unchanged
        - adding Gaussian noise to the fittest partition[1] genomes
        - crossover between fittest partition[2] genomes
        - crossover between fittest partition[3] and randomly selected genes
        - randomly adding parition[4] genomes
    genomes; the amount of genomes in the genepool, speficy this parameter instead
        of partition if you don't care about the specific partition.
    genes; the amount of genes per genome
    mutationrate; the probability of mutation for each gene (between 0 and 1)
    fitnessavg; the amount of times the same genome is tested to obtain the fitness
        value.
    fitnessparameters; the parameters for FitnessEvolution (see its doc for
        specifics)
    filepath; the path used for saving your experiment data
    name; name used for experiment data file (date/time will be appended)

    ----------------------------------------------------------------------------
    Description of method parameters
    ----------------------------------------------------------------------------
    signallength; the length in s of the Boolean P and Q signals
    edgelength; the length in s of the edge between 0 and 1 in P and Q
    fs; sample frequency for niDAQ or ADwin

    ----------------------------------------------------------------------------
    Description of methods
    ----------------------------------------------------------------------------
    TargetGen; specify the target function you wish to evolve, examples for N=4 are:
        - OR
        - AND
        - NOR
        - NAND
        - XOR
        - XNOR
    Fitness; specify the fitness function, as the accuracy of a perceptron separating the data
    '''

    def __init__(self, inputs, labels):
        super().__init__() #DO NOT REMOVE!
        ################################################
        ######### SPECIFY PARAMETERS ###################
        ################################################

        # Define experiment
        self.lengths, self.slopes = [125], [10] # in 1/fs
        self.InputGen = self.input_waveform(inputs)
        self.amplification = 1
        self.TargetGen = np.asarray(GenWaveform(labels, self.lengths, slopes=self.slopes))
        self.generations = 100
        self.generange = [[-900,900], [-900, 900], [-900, 900], [-900, 900], [-900, 900]]
        self.input_scaling = 0.9
        self.Fitness = self.accuracy_fit
#        self.fitnessparameters = [1, 0, 0, 1]

        # Specify either partition or genomes
        self.partition = [2, 6, 6, 6, 5]

        # Documentation
        self.genelabels = ['CV1','CV2','CV3','CV4','CV5']

        # Save settings
        self.filepath = r'../../test/evolution_test/VCdim_testing/'
        buf_str = str(labels)
        self.name = 'VCdim-'+''.join(buf_str.lstrip('[').strip(']').split())

        ################################################
        ################# OFF-LIMITS ###################
        ################################################
        # Check if genomes parameter has been changed
        if(self.genomes != sum(self.default_partition)):
            if(self.genomes%5 == 0):
                self.partition = [self.genomes%5]*5  # Construct equally partitioned genomes
            else:
                print('WARNING: The specified number of genomes is not divisible by 5.'
                      + ' The remaining genomes are generated randomly each generation. '
                      + ' Specify partition in the config instead of genomes if you do not want this.')
                self.partition = [self.genomes//5]*5  # Construct equally partitioned genomes
                self.partition[-1] += self.genomes%5  # Add remainder to last entry of partition

        self.genomes = sum(self.partition)  # Make sure genomes parameter is correct
        self.genes = len(self.generange)  # Make sure genes parameter is correct

    #####################################################
    ############# USER-SPECIFIC METHODS #################
    #####################################################
    # Optionally define new methods here that you wish to use in your experiment.
    # These can be e.g. new fitness functions or input/output generators.
    
    def input_waveform(self, inputs):
        assert len(inputs) == 2, 'Input must be 2 dimensional!'
        inp_wvfrm0 = GenWaveform(inputs[0], self.lengths, slopes=self.slopes)
        inp_wvfrm1 = GenWaveform(inputs[1], self.lengths, slopes=self.slopes)
        samples = len(inp_wvfrm0)
        time_arr = np.linspace(0, samples/self.fs, samples)
        inputs_wvfrm = np.asarray([inp_wvfrm0,inp_wvfrm1])
        
#        print('Size of input', inputs_wvfrm.shape)
        w_ampl = [1,0]*len(inputs[0])
        w_lengths = [self.lengths[0],self.slopes[0]]*len(inputs[0])
        
        weight_wvfrm = GenWaveform(w_ampl, w_lengths)
        bool_weights = [x==1 for x in weight_wvfrm[:samples]]
        
        return time_arr, inputs_wvfrm, bool_weights
    
    def accuracy_fit(self, output, target, w):
#        print(w)
#        print('shape of target = ', target.shape)
        x = output[w][:,np.newaxis]
        y = target[w][:,np.newaxis]
#        print('shape of x,y: ', x.shape,y.shape)
#        acc, _, _ = perceptron(x,y)
        acc = 1.
        print('Perceptron is OFF!')
        X = np.stack((x, y), axis=0)[:,:,0]
        corr = np.corrcoef(X)[0,1]
        return acc*corr