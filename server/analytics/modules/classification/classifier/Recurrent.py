__author__ = 'Tony Beltramelli www.tonybeltramelli.com - 13/09/2015'

from pybrain.datasets import SequentialDataSet
from pybrain.supervised.trainers import RPropMinusTrainer
from pybrain.structure import *
from Classifier import *


class Recurrent(Classifier):
    def __init__(self, neurons_per_layer=[9]):
        Classifier.__init__(self)

        self.neurons_per_layer = neurons_per_layer

    def build_neural_net(self):
        input_number, output_number = self.meta_data

        input = LinearLayer(input_number)
        output = SoftmaxLayer(len(self.LABELS))
        #bias = BiasUnit(name='bias')

        self.neural_net = RecurrentNetwork()
        self.neural_net.addInputModule(input)
        self.neural_net.addOutputModule(output)
        #self.neural_net.addModule(bias)

        prev = input
        for i in range(0, len(self.neurons_per_layer)):
            lstm = LSTMLayer(self.neurons_per_layer[i], peepholes=False)

            self.neural_net.addModule(lstm)
            self.neural_net.addConnection(FullConnection(prev, lstm))
            #self.neural_net.addConnection(FullConnection(bias, lstm))

            prev = lstm

        self.neural_net.addConnection(FullConnection(prev, output))
        self.neural_net.sortModules()

        fast_net = self.neural_net.convertToFastNetwork()

        if fast_net is not None:
            self.neural_net = fast_net
            print "Use fast C++ implementation"
        else:
            print "Use standard Python implementation"

    def get_new_data_set(self):
        input_number, output_number = self.meta_data

        return SequentialDataSet(input_number, output_number)

    def get_new_trainer(self, data_set):
        if not self.neural_net:
            self.build_neural_net()

        return RPropMinusTrainer(self.neural_net, dataset=data_set)

    def get_predictions(self, input_values):
        predictions = np.zeros(len(self.LABELS))
        for values in input_values:
            prediction = self.neural_net.activate(values)
            predictions = [sum(x) for x in zip(predictions, prediction)]

        return UMath.normalize_array(predictions)

    def get_name(self):
        return "LSTM recurrent network (RProp- training)"
