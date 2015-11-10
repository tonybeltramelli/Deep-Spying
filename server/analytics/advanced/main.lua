require 'torch'
require 'nn'
require 'nngraph'
require 'lfs'

GPU_ID = 1
USE_OPENCL = 0

if GPU_ID >= 0 and USE_OPENCL == 1 then
    local n, clnn = pcall(require, 'clnn')
    local t, cltorch = pcall(require, 'cltorch')

    if n and t then
    	print("Use OpenCL on GPU "..GPU_ID)
    	cltorch.setDevice(GPU_ID)
    end
else
	print("Use CPU")
end

LABELS = {"1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "*", "#"}
HIDDEN_LAYERS = {256, 256}
DATA_PATH = "../../data/feature/"
INIT_WEIGHT=0.08

metaData = nil

function makeBinaryClasses(labelSet)
	classes = {}
	local len = #labelSet

	for i = 1, len do
		local t = torch.Tensor(1, len)
		local binClasses = t:storage()

		binClasses[i] = 1
		classes[labelSet[i]] = torch.Tensor(binClasses)
	end
end

function createDataset()
	dataset = {}
	local i = 0

	for file in lfs.dir(DATA_PATH) do
	    if string.match(file, ".data") then
	    	local data = io.open(DATA_PATH..file, "r")

	    	if data then
	    		local outputVect = nil

	    		for line in data:lines() do
	    			if string.match(line, ":") then
	    				local s, e = string.find(line, ":")
		                local label = string.sub(line, s + 1)
		                outputVect = classes[label]
		            elseif string.match(line, ".") then
		            	dataPoints = line:split(",")
		            	
		            	local len = #dataPoints
		            	local t = torch.Tensor(1, len)
		            	local inputVect = t:storage()

		            	for j = 1, len do
		            		inputVect[j] = dataPoints[j]
		            	end

		            	i = i + 1
		               	dataset[i] = {torch.Tensor(inputVect), outputVect}

		            	if metaData == nil then
		            		metaData = {inputSize = len, outputSize = #LABELS}
		            	end
		            end
				end
			end

	    	data.close()
	    end
	end
	function dataset:size() return #dataset end
end

function buildNeuralNet()
	-- torch.manualSeed(1234)

	-- local LSTM = require 'model.LSTM'
	-- model = LSTM.model(metaData.inputSize, metaData.outputSize, HIDDEN_LAYERS, INIT_WEIGHT)

	inputSize = 2
	outputSize = 4
	layerSize = 10
	initWeight = 0.08
	layers = 1

	local inputs = {}
	local outputs = {}

	table.insert(inputs, nn.Identity()())
	for i = 1, layers do
		table.insert(inputs, nn.Identity()())
		table.insert(inputs, nn.Identity()())
	end

	local input = inputs[1]

	for i = 1, layers do
		local prevC = inputs[i * 2]
		local prevY = inputs[i * 2 + 1]

		local function lstmCell(input, prevY, prevC)
	    	local xi = nn.Linear(inputSize, layerSize)(input)
		    local prevYi = nn.Linear(layerSize, layerSize)(prevY)
		    local gateInput = nn.CAddTable()({xi, prevYi})
		    
		    local inputGate = nn.Sigmoid()(gateInput)
		    local forgetGate = nn.Sigmoid()(gateInput)
		    local cellInput = nn.Tanh()(gateInput)
		    local nextC = nn.CAddTable()({
		      nn.CMulTable()({forgetGate, prevC}),
		      nn.CMulTable()({inputGate, cellInput})
		    })
		    local outputGate = nn.Sigmoid()(gateInput)
		    local nextY = nn.CMulTable()({outputGate, nn.Tanh()(nextC)})
		    return nextY, nextC
		end

		local nextY, nextC = lstmCell(input, prevY, prevC)
		table.insert(outputs, nextC)
		table.insert(outputs, nextY)
	end
	
	local topY = outputs[#outputs]
	local prediction = nn.LogSoftMax()(nn.Linear(layerSize, outputSize)(topY))
	table.insert(outputs, prediction)

	model = nn.gModule(inputs, outputs)
	model:getParameters():uniform(-initWeight, initWeight)
end

function train()
	-- lossFunction = nn.ClassNLLCriterion()
	local lossFunction = nn.MSECriterion()

	trainer = nn.StochasticGradient(model, lossFunction)
	trainer.learningRate = 0.001
	trainer.learningRateDecay = 0.9
	trainer.maxIteration = 100
	trainer.shuffleIndices = false
	trainer:train(dataset)
end

--makeBinaryClasses(LABELS)
--createDataset()
--buildNeuralNet()
--train()

-- os.exit()







buildNeuralNet()
out = model:forward({torch.randn(1,2), torch.randn(1, 10), torch.randn(1, 10)})
print(out[3])
