-- Author Tony Beltramelli www.tonybeltramelli.com - 10/11/2015

local FNN = {}

function FNN.get(inputSize, outputSize, layerSize, layerNum)
  	local input = nn.Identity()()

	local layerInputSize = inputSize
	local previous = input

	for i = 1, layerNum do
		local hidden = nn.Tanh()(nn.Linear(layerInputSize, layerSize)(previous))

		layerInputSize = layerSize
		previous = hidden
	end

	local output = nn.SoftMax()(nn.Linear(layerInputSize, outputSize)(previous))

	print("Create FNN neural net with "..inputSize.." input neurons, "..outputSize.." output neurons, and "..layerNum.." hidden layers with "..layerSize.." units")

	local model = nn.gModule({input}, {output})
	model.layerSize = layerSize
	model.layerNum = layerNum
	model.isRecurrent = false

	return model
end

return FNN
