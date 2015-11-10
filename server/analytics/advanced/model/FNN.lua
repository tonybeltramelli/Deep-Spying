local FNN = {}

function FNN.model(inputSize, outputSize, hiddenLayers, initWeight)
  	local input = nn.Identity()()

	local layerSize = inputSize
	local previous = input

	for i = 1, #hiddenLayers do
		local hiddenSize = hiddenLayers[i]
		local hidden = nn.Tanh()(nn.Linear(layerSize, hiddenSize)(previous))

		layerSize = hiddenSize
		previous = hidden
	end

	local output = nn.LogSoftMax()(nn.Linear(layerSize, outputSize)(previous))

	local m = nn.gModule({input}, {output})
	m:getParameters():uniform(-initWeight, initWeight)
	return m
end

return FNN


