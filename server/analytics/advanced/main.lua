require 'torch'
require 'nn'
require 'nngraph'
require 'lfs'

cmd = torch.CmdLine()
cmd:text()
cmd:text("Options:")
cmd:option("-data_path", "../../data/feature/", "pre-processed data directory")
cmd:option("-labels", "1,2,3,4,5,6,7,8,9,0,*,#", "list of labels separated with a comma")
cmd:option("-model", "lstm", "lstm | fnn | gru | rnn")
cmd:option("-layer_size", 128, "size of hidden internal state")
cmd:option("-layer_num", 2, "number of hidden layers")
cmd:option("-max_iteration", 100, "maximum number of training iteration")
cmd:option("-learning_rate", 2e-3, "learning rate")
cmd:option("-learning_rate_decay", 0.97, "learning rate decay")
cmd:option("-learning_rate_decay_after", 10, "in number of epochs, when to start decaying the learning rate")
cmd:option("-decay_rate", 0.95, "decay rate for rmsprop")
cmd:option("-dropout", 0, "dropout for regularization, used after each RNN hidden layer. 0 = no dropout")
cmd:option("-init_weight", 0.08, "value interval to init weights")
cmd:option("-seed", 123, "seed to pseudo-random number generator")
cmd:option("-gpu", 0, "use gpu (OpenCL)")
cmd:text()
opt = cmd:parse(arg)

GPU_ID = 1

if opt.gpu == 1 then
    local n, clnn = pcall(require, 'clnn')
    local t, cltorch = pcall(require, 'cltorch')

    if n and t then
    	print("Use OpenCL on GPU "..GPU_ID)
    	cltorch.setDevice(GPU_ID)
    end
else
	print("Use CPU")
end

require 'model.OneHot'

local dataLoader = require 'loader.DataLoader'
local lstm = require 'model.LSTM'

function cloneList(tensorList, toZero)
    local out = {}
    for k,v in pairs(tensorList) do
        out[k] = v:clone()
        if toZero then out[k]:zero() end
    end
    return out
end

function trainAutomatic()
	-- lossFunction = nn.ClassNLLCriterion()
	local lossFunction = nn.MSECriterion()

	trainer = nn.StochasticGradient(model, lossFunction)
	trainer.learningRate = opt.learning_rate
	trainer.learningRateDecay = opt.learning_rate_decay
	trainer.maxIteration = opt.max_iteration
	trainer.shuffleIndices = false
	trainer:train(dataset)
end

function train(model, dataset, criterion, initWeight)
	model:getParameters():uniform(-initWeight, initWeight)
	local states = {}
	local initialState = {}
	local predictions = {}
	local loss = 0

	for i = 1, opt.max_iteration do
		if i == 1 then
			for i = 1, opt.layer_num do
			    local emptyVector = torch.zeros(1, opt.layer_size)
			    table.insert(initialState, emptyVector:clone())
			    table.insert(initialState, emptyVector:clone())
			end

			states = {[0] = cloneList(initialState)}
		end

		local inputVector = dataset[i][1]
		local expectedOutputVector = dataset[i][2] 

		local out = model:forward({inputVector, unpack(states[i - 1])})

		states[i] = {}
		for i=1, #out - 1 do
			table.insert(states[i], out[i])
		end

		predictions[i] = out[#out]
		loss = loss + criterion:forward(predictions[i], expectedOutputVector)
	end

	loss = loss / opt.max_iteration

	local backwardStates = {[opt.max_iteration] = cloneList(initialState, true)}

	for i = opt.max_iteration, 1, -1 do
		local backpropagated = criterion:backward(predictions[i], expectedOutputVector)
		table.insert(backwardStates[i], backpropagated)

		local derivative = model:backward({inputVector, unpack(states[i - 1])}, backwardStates[i])
		backwardStates[t - 1] = {}

		for k, v in pairs(derivative) do
            if k > 1 then
            	backwardStates[t-1][k-1] = v
            end
        end
	end
end

dataLoader.load(opt.data_path, opt.labels:split(","))
local dataset = dataLoader.dataset
local model = lstm.get(dataLoader.metaData.inputSize, dataLoader.metaData.outputSize, opt.layer_size, opt.layer_num)
local lossFunction = nn.MSECriterion()

train(model, dataset, lossFunction, opt.init_weight)
-- os.exit()
