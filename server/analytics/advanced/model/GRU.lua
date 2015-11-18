-- Author Tony Beltramelli www.tonybeltramelli.com - 16/11/2015
-- Adapted from https://github.com/karpathy/char-rnn/

local GRU = {}

function GRU.get(inputSize, outputSize, layerSize, layerNum)
	local inputs = {}
	local outputs = {}

	table.insert(inputs, nn.Identity()())
	for i = 1, layerNum do
		table.insert(inputs, nn.Identity()())
	end

	local x, layerInputSize
	local dropout = dropout or 0

	for i = 1, layerNum do
		if i == 1 then
    		x = inputs[1]
    		layerInputSize = inputSize
    	else
    		x = outputs[i - 1]
    		layerInputSize = layerSize
    		if dropout > 0 then x = nn.Dropout(dropout)(x) end
    	end

		local prevY = inputs[i + 1]

		local xInput = nn.Linear(layerInputSize, layerSize)(x)
		local prevYInput = nn.Linear(layerSize, layerSize)(prevY)
		local gateInput = nn.CAddTable()({xInput, prevYInput})

		local updateGate = nn.Sigmoid()(gateInput)
		local resetGate = nn.Sigmoid()(gateInput)
    
    	local gatedHidden = nn.CMulTable()({resetGate, prevY})
    	local p2 = nn.Linear(layerSize, layerSize)(gatedHidden)
    	local p1 = nn.Linear(layerInputSize, layerSize)(x)
    	local hiddenCandidate = nn.Tanh()(nn.CAddTable()({p1, p2}))
    
	    local zh = nn.CMulTable()({updateGate, hiddenCandidate})
	    local zhm1 = nn.CMulTable()({nn.AddConstant(1, false)(nn.MulConstant(-1, false)(updateGate)), prevY})
	    local nextY = nn.CAddTable()({zh, zhm1})

    	table.insert(outputs, nextY)
    end

    local topY = outputs[#outputs]
    if dropout > 0 then topY = nn.Dropout(dropout)(topY) end
	local prediction = nn.SoftMax()(nn.Linear(layerSize, outputSize)(topY))
	table.insert(outputs, prediction)

	print("Create GRU neural net with "..inputSize.." input neurons, "..outputSize.." output neurons, and "..layerNum.." hidden layers with "..layerSize.." units")

	local model = nn.gModule(inputs, outputs)
	model.layerSize = layerSize
	model.layerNum = layerNum
	model.hiddenStateNum = 1
	model.isRecurrent = true

	return model
end

return GRU
	