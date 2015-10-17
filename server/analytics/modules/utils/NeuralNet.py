__author__ = 'Tony Beltramelli www.tonybeltramelli.com - 17/10/2015'

from pybrain.structure import *


class NeuralNet:

    @staticmethod
    def get_neural_net(input_number, output_number, NetworkType, HiddenLayerType, neurons_per_layer=[9]):
        input = LinearLayer(input_number)
        output = SoftmaxLayer(output_number)

        neural_net = NetworkType()
        neural_net.addInputModule(input)
        neural_net.addOutputModule(output)

        prev = input
        for i in range(0, len(neurons_per_layer)):
            hidden = HiddenLayerType(neurons_per_layer[i])

            neural_net.addModule(hidden)
            neural_net.addConnection(FullConnection(prev, hidden))

            prev = hidden

        neural_net.addConnection(FullConnection(prev, output))
        neural_net.sortModules()

        fast_net = neural_net.convertToFastNetwork()

        if fast_net is not None:
            neural_net = fast_net
            print "Use fast C++ implementation"
        else:
            print "Use standard Python implementation"

        return neural_net