local LSTM = {}

function LSTM.get(inputSize, outputSize, layerSize, layerNum)
	local inputs = {}
	local outputs = {}

	print("Create LSTM neural net with "..inputSize.." input neurons, "..outputSize.." output neurons, and "..layerNum.." hidden layers with "..layerSize.." units")

	table.insert(inputs, nn.Identity()())
	for i = 1, layerNum do
		table.insert(inputs, nn.Identity()())
		table.insert(inputs, nn.Identity()())
	end

	local x, layerInputSize

	for i = 1, layerNum do
		if i == 1 then
	      x = inputs[1]
	      layerInputSize = inputSize
	    else
	      x = outputs[(i - 1) * 2]
	      layerInputSize = layerSize
	    end

	    local prevC = inputs[i * 2]
	    local prevY = inputs[i * 2 + 1]

		local xInput = nn.Linear(layerInputSize, layerSize)(x)
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
	local prediction = nn.SoftMax()(nn.Linear(layerSize, outputSize)(topY))
	table.insert(outputs, prediction)

	return nn.gModule(inputs, outputs)
end

return LSTM
