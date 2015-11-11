require 'torch'
require 'nn'
require 'nngraph'
require 'lfs'
require 'optim'

cmd = torch.CmdLine()
cmd:text()
cmd:text("Options:")
cmd:option("-data_path", "../../data/feature/", "pre-processed data directory")
cmd:option("-labels", "1,2,3,4,5,6,7,8,9,0,*,#", "list of labels separated with a comma")
cmd:option("-model", "lstm", "lstm | fnn | gru | rnn")
cmd:option("-layer_size", 128, "size of hidden internal state")
cmd:option("-layer_num", 2, "number of hidden layers")
cmd:option("-max_epochs", 100, "maximum number of passes through the training dataset")
cmd:option("-learning_rate", 2e-3, "learning rate")
cmd:option("-learning_rate_decay", 0.97, "learning rate decay")
cmd:option("-learning_rate_decay_after", 10, "in number of epochs, when to start decaying the learning rate")
cmd:option("-decay_rate", 0.95, "decay rate for rmsprop")
cmd:option("-dropout", 0, "dropout for regularization, used after each RNN hidden layer. 0 = no dropout")
cmd:option("-init_weight", 0.08, "value interval to init weights")
cmd:option('-gradient_clip',5,'clip gradients at this value')
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

UClone = require 'utils.UClone'
local dataLoader = require 'loader.DataLoader'
local lstm = require 'model.LSTM'
local trainer = require 'Trainer'

dataLoader.load(opt.data_path, opt.labels:split(","))
local dataset = dataLoader.dataset
local model = lstm.get(dataLoader.metaData.inputSize, dataLoader.metaData.outputSize, opt.layer_size, opt.layer_num)
local criterion = nn.MSECriterion()

config = {
    sequenceLength = dataLoader.metaData.sequenceLength,
    initWeight = opt.init_weight,
    layerSize = opt.layer_size,
    layerNum = opt.layer_num,
    gradientClip = opt.gradient_clip,
    learningRate = opt.learning_rate,
    decayRate = opt.decay_rate,
    learningRateDecay = opt.learning_rate_decay,
    learningRateDecayAfter = opt.learning_rate_decay_after,
    maxEpochs = opt.max_epochs
}

trainer.trainRecurrent(model, criterion, dataset, config)
-- os.exit()
