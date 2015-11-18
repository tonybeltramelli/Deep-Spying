-- Author Tony Beltramelli www.tonybeltramelli.com - 10/11/2015

local LSTM = {}

function LSTM.get(inputSize, outputSize, layerSize, layerNum, dropout)
	local inputs = {}
	local outputs = {}

	table.insert(inputs, nn.Identity()())
	for i = 1, layerNum do
		table.insert(inputs, nn.Identity()())
		table.insert(inputs, nn.Identity()())
	end

	local x, layerInputSize
	local dropout = dropout or 0

	for i = 1, layerNum do
		if i == 1 then
			x = inputs[1]
			layerInputSize = inputSize
	    else
	    	x = outputs[(i - 1) * 2]
	    	layerInputSize = layerSize
	    	if dropout > 0 then x = nn.Dropout(dropout)(x) end
	    end

	    local prevC = inputs[i * 2]
	    local prevY = inputs[i * 2 + 1]

		local xInput = nn.Linear(layerInputSize, layerSize)(x):annotate{name = 'bias'}
		local prevYInput = nn.Linear(layerSize, layerSize)(prevY)
		local gateInput = nn.CAddTable()({xInput, prevYInput})

		local inputGate = nn.Sigmoid()(gateInput)
		local forgetGate = nn.Sigmoid()(gateInput)
		local outputGate = nn.Sigmoid()(gateInput)
		local cellInput = nn.Tanh()(gateInput)

		local nextC = nn.CAddTable()({
			nn.CMulTable()({forgetGate, prevC}),
			nn.CMulTable()({inputGate, cellInput})
		})
		local nextY = nn.CMulTable()({outputGate, nn.Tanh()(nextC)})

		table.insert(outputs, nextC)
		table.insert(outputs, nextY)
	end
	
	local topY = outputs[#outputs]
	if dropout > 0 then topY = nn.Dropout(dropout)(topY) end
	local prediction = nn.SoftMax()(nn.Linear(layerSize, outputSize)(topY))
	table.insert(outputs, prediction)

	print("Create LSTM neural net with "..inputSize.." input neurons, "..outputSize.." output neurons, and "..layerNum.." hidden layers with "..layerSize.." units")

	local model = nn.gModule(inputs, outputs)
	model.layerSize = layerSize
	model.layerNum = layerNum
	model.hiddenStateNum = 2
	model.isRecurrent = true

	return model
end

return LSTM
