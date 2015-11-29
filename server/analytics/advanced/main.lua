-- Author Tony Beltramelli www.tonybeltramelli.com - 10/11/2015

require 'torch'
require 'nn'
require 'nngraph'
require 'lfs'
require 'optim'

cmd = torch.CmdLine()
cmd:text()
cmd:text("Options:")
cmd:option("-data_path", "../../data/feature/", "pre-processed data directory")
cmd:option("-output_report", "report", "filename to save the validation report")
cmd:option("-mode", "train", "train | evaluate | validate")
cmd:option("-labels", "1,2,3,4,5,6,7,8,9,0,*,#", "list of labels separated with a comma")
cmd:option("-k", 5, "number of dataset splits to perform k-fold cross-validation")
cmd:option("-model", "lstm", "lstm | fnn | gru | rnn")
cmd:option("-layer_size", 128, "size of hidden internal state")
cmd:option("-layer_num", 2, "number of hidden layers")
cmd:option("-max_epochs", 100, "maximum number of passes through the training dataset")
cmd:option("-learning_rate", 0.01, "learning rate")
cmd:option("-learning_rate_decay", 0.97, "learning rate decay")
cmd:option("-learning_rate_decay_after", 10, "in number of epochs, when to start decaying the learning rate")
cmd:option("-decay_rate", 0.95, "decay rate for rmsprop")
cmd:option("-init_weight", 0.08, "value interval to init weights")
cmd:option("-gradient_clip", 5, "clip gradients at this value")
cmd:option("-dropout", 0.1, "dropout for regularization and avoid overfitting")
cmd:option("-seed", 123, "seed to pseudo-random number generator")
cmd:option("-gpu", 0, "use gpu (OpenCL)")
cmd:text()
opt = cmd:parse(arg)

GPU_ID = 1
USE_GPU = false

if opt.gpu == 1 then
    local n, clnn = pcall(require, 'clnn')
    local t, cltorch = pcall(require, 'cltorch')
    if n and t then
    	print("Use OpenCL on GPU "..GPU_ID)
    	cltorch.setDevice(GPU_ID)
    end
    USE_GPU = true
else
	print("Use CPU")
end

torch.manualSeed(opt.seed)

UClone = require 'utils.UClone'
UMath = require 'utils.UMath'

local data = require 'data.Data'
local gradient = require 'gradient.Gradient'

local labels = opt.labels:split(",")
local referenceDataset = data.load(opt.data_path, labels)

function train(dataset)
    local model = nil
    
    if opt.model == "lstm" then
        local lstm = require 'model.LSTM'
        model = lstm.get(dataset.metaData.inputSize, dataset.metaData.outputSize, opt.layer_size, opt.layer_num, opt.dropout)
    elseif opt.model == "fnn" then
        local fnn = require 'model.FNN'
        model = fnn.get(dataset.metaData.inputSize, dataset.metaData.outputSize, opt.layer_size, opt.layer_num)
    elseif opt.model == "gru" then
        local gru = require 'model.GRU'
        model = gru.get(dataset.metaData.inputSize, dataset.metaData.outputSize, opt.layer_size, opt.layer_num)
    elseif opt.model == "rnn" then
        local rnn = require 'model.RNN'
        model = rnn.get(dataset.metaData.inputSize, dataset.metaData.outputSize, opt.layer_size, opt.layer_num)
    end

    local criterion = nn.MSECriterion()

    config = {
        initWeight = opt.init_weight,
        gradientClip = opt.gradient_clip,
        learningRate = opt.learning_rate,
        decayRate = opt.decay_rate,
        learningRateDecay = opt.learning_rate_decay,
        learningRateDecayAfter = opt.learning_rate_decay_after,
        maxEpochs = opt.max_epochs
    }

    local losses = nil
    if model.isRecurrent then
        losses = gradient.trainRecurrent(model, criterion, dataset, config)
    else
        losses = gradient.trainFeedforward(model, criterion, dataset, config)
    end

    return losses
end

function evaluate(dataset)
    local model = torch.load("neural_net")

    local results = nil
    if model.isRecurrent then
        results = gradient.evaluate(model, dataset)
    else
        results = gradient.evaluateFeedforward(model, dataset)
    end

    local confusion = optim.ConfusionMatrix(#labels)

    for i = 1, #results do
        print(labels[results[i].predicted].." - "..labels[results[i].expected])
        confusion:add(results[i].predicted, results[i].expected)
    end
    
    print(confusion)
    return results
end

function crossValidation(dataset)
    local report = require 'data.Report'
    local datasets = data.shuffleAndSplit(dataset, opt.k)

    function joinMyTables(t1, t2)
       for k,v in ipairs(t2) do
          table.insert(t1, v)
       end 
     
       return t1
    end

    for i = 1, opt.k do
        print(opt.k.."-fold cross-validation: "..i.."/"..opt.k)

        local evaluationSet = datasets[i]
        local trainingSet = data.excludeAndMerge(datasets, i)

        local losses = train(trainingSet)
        local results = evaluate(joinMyTables(trainingSet, evaluationSet))

        report.store(losses, results, labels, evaluationSet:size())
    end
    report.save(opt.output_report)
end

if opt.mode == "train" then
    print("Train")
    train(referenceDataset)
elseif opt.mode == "evaluate" then
    print("Evaluate")
    evaluate(referenceDataset)
elseif opt.mode == "validate" then
    print("Validate")
    crossValidation(referenceDataset)
end
