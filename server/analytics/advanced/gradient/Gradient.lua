-- adapted from https://github.com/karpathy/char-rnn/ and https://github.com/oxford-cs-ml-2015/practical6/

local Gradient = {}

function Gradient.getInitialState(layerSize, layerNum)
    local initialState = {}
    for L=1,layerNum do
        local emptyVector = torch.zeros(1, layerSize)
        table.insert(initialState, emptyVector:clone())
        table.insert(initialState, emptyVector:clone())
    end
    return initialState
end

-- Gradient.trainRecurrent
-- example config:
-- {
--   initWeight : 0.08
--   learningRate : 0.002
--   layerSize : 128
--   decayRate : 0.95
--   layerNum : 2
--   gradientClip : 5
--   learningRateDecay : 0.97
--   maxEpochs : 50
-- }
function Gradient.trainRecurrent(model, criterion, dataset, config)
    local config = config or {}
    local initWeight = config.initWeight
    local layerSize = config.layerSize
    local layerNum = config.layerNum
    local gradientClip = config.gradientClip
    local learningRate = config.learningRate
    local decayRate = config.decayRate
    local learningRateDecay = config.learningRateDecay
    local learningRateDecayAfter = config.learningRateDecayAfter
    local maxEpochs = config.maxEpochs

    local sequenceLength = dataset.metaData.sequenceLength
    local currentSequence = nil

    local params, gradParams = model:getParameters()
    params:uniform(-initWeight, initWeight)

    print("Parameters in the model: "..params:nElement())

    local models = UClone.cloneNetOverTime(model, sequenceLength, not model.parameters)
    local criterions = UClone.cloneNetOverTime(criterion, sequenceLength, not criterion.parameters)

    local initialState = Gradient.getInitialState(layerSize, layerNum)

    function backpropagation(p)
        if p ~= params then
            params:copy(p)
        end
        gradParams:zero()

        local states = {[0] = UClone.cloneList(initialState)}
        local predictions = {}
        local loss = 0

        for t = 1, sequenceLength do
            local inputVector = currentSequence[t][1]
            local expectedOutputVector = currentSequence[t][2]

            models[t]:training()
            local output = models[t]:forward{inputVector, unpack(states[t - 1])}
            predictions[t] = output[#output]
            loss = loss + criterions[t]:forward(predictions[t], expectedOutputVector)

            states[t] = {}
            for i=1, #output - 1 do
                table.insert(states[t], output[i])
            end
        end

        loss = loss / sequenceLength
        
        local finalState = {[sequenceLength] = UClone.cloneList(initialState, true)}
        for t = sequenceLength, 1, -1 do
            local inputVector = currentSequence[t][1]
            local expectedOutputVector = currentSequence[t][2]

            local backpropagatedState = criterions[t]:backward(predictions[t], expectedOutputVector)
            table.insert(finalState[t], backpropagatedState)
            local derivative = models[t]:backward({inputVector, unpack(states[t-1])}, finalState[t])
            finalState[t-1] = {}

            for k,v in pairs(derivative) do
                if k > 1 then
                    finalState[t-1][k-1] = v
                end
            end
        end
        
        initialState = states[#states]
        gradParams:clamp(-gradientClip, gradientClip)
        return loss, gradParams
    end

    local losses = {}
    local optimization = {learningRate = learningRate, alpha = decayRate}
    local iterations = maxEpochs * sequenceLength
    local lossBug = nil
    local j = 0

    for i = 1, iterations do
        j = j + 1
        if j == #dataset + 1 then
            j = 1
        end

        currentSequence = dataset[j]

        local epoch = i / sequenceLength
        local newParams, loss = optim.rmsprop(backpropagation, params, optimization)

        local currentLoss = loss[1]
        losses[i] = currentLoss

        if i % sequenceLength == 0 and learningRateDecay < 1 then
            if epoch >= learningRateDecayAfter then
                local decay_factor = learningRateDecay
                optimization.learningRate = optimization.learningRate * decay_factor
                print("Decayed learning rate by a factor "..decay_factor.." to "..optimization.learningRate)
            end
        end

        print(i..'/'..iterations..", epoch: "..epoch..", loss: "..currentLoss)
        
        if i % 10 == 0 then collectgarbage() end
    end
end

-- Gradient.evaluate
-- example config:
-- {
--   layerSize : 128
--   layerNum : 2
-- }
function Gradient.evaluate(model, dataset, config)
    local config = config or {}
    local layerSize = config.layerSize
    local layerNum = config.layerNum

    local sequenceLength = dataset.metaData.sequenceLength

    local models = UClone.cloneNetOverTime(model, sequenceLength, not model.parameters)
    local states = {[0] = Gradient.getInitialState(layerSize, layerNum)}
    
    local results = {}
    for i = 1, dataset:size() do
        currentSequence = dataset[i]

        local expectedOutputVector = nil
        local accumulativePrediction = torch.zeros(dataset.metaData.outputSize)
        for t = 1, sequenceLength do
            local inputVector = currentSequence[t][1]
            expectedOutputVector = currentSequence[t][2]

            models[t]:evaluate()
            local output = models[t]:forward{inputVector, unpack(states[t - 1])}
            local prediction = output[#output]
            accumulativePrediction = torch.add(accumulativePrediction, prediction)

            states[t] = {}
            for i=1, #output - 1 do
                table.insert(states[t], output[i])
            end
        end

        states[0] = states[#states]
        
        print(i..'/'..dataset:size())

        local v, index = torch.max(expectedOutputVector, 1)
        indexExpected = torch.sum(index)
        v, index = torch.max(accumulativePrediction, 1)
        indexPredicted = torch.sum(index)

        results[i] = {expected = indexExpected, predicted = indexPredicted}
    end

    return results
end

return Gradient