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
	torch.manualSeed(1234)

	local inputSize = metaData.inputSize
	local outputSize = metaData.outputSize

	model = nn.Sequential()
	local layerSize = inputSize

	for i = 1, #HIDDEN_LAYERS do
		local hiddenSize = HIDDEN_LAYERS[i]

		model:add(nn.Linear(layerSize, hiddenSize))
		model:add(nn.Tanh())
		model:add(nn.Dropout())

		layerSize = hiddenSize
	end

	model:add(nn.Linear(layerSize, outputSize))
	model:add(nn.LogSoftMax())
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

makeBinaryClasses(LABELS)
createDataset()
--buildNeuralNet()
local FNN = require 'model.FNN'
model = FNN.fnn(metaData.inputSize, metaData.outputSize, HIDDEN_LAYERS)
train()

-- os.exit()
