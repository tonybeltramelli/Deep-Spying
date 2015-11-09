local FNN = {}

function FNN.fnn(inputSize, outputSize, hiddenLayers)
  	local input = nn.Identity()()

	local layerSize = inputSize
	local previous = input

	for i = 1, #hiddenLayers do
		local hiddenSize = hiddenLayers[i]

		hidden = nn.Tanh()(nn.Linear(layerSize, hiddenSize)(previous))

		layerSize = hiddenSize
		previous = hidden
	end

	output = nn.LogSoftMax()(nn.Linear(layerSize, outputSize)(previous))

	return nn.gModule({input}, {output})
end

return FNN


