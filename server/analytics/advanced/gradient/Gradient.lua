-- Author Tony Beltramelli www.tonybeltramelli.com - 11/11/2015
-- Adapted from https://github.com/karpathy/char-rnn/ and https://github.com/oxford-cs-ml-2015/practical6/

local Gradient = {}

function Gradient.getInitialState(layerSize, layerNum, hiddenStateNum)
    local initialState = {}
    local emptyVector = torch.zeros(1, layerSize)

    for i = 1, layerNum * hiddenStateNum do
        table.insert(initialState, emptyVector:clone())
    end
    return initialState
end

-- Gradient.trainRecurrent
-- example config:
-- {
--   initWeight : 0.08
--   learningRate : 0.002
--   decayRate : 0.95
--   gradientClip : 5
--   learningRateDecay : 0.97
--   maxEpochs : 50
-- }
function Gradient.trainRecurrent(model, criterion, dataset, config)
    local config = config or {}
    local initWeight = config.initWeight
    local gradientClip = config.gradientClip
    local learningRate = config.learningRate
    local decayRate = config.decayRate
    local learningRateDecay = config.learningRateDecay
    local learningRateDecayAfter = config.learningRateDecayAfter
    local maxEpochs = config.maxEpochs

    local layerSize = model.layerSize
    local layerNum = model.layerNum
    local hiddenStateNum = model.hiddenStateNum

    local sequenceLength = dataset.metaData.sequenceLength
    local currentSequence = nil

    local params, gradParams = model:getParameters()
    params:uniform(-initWeight, initWeight)
    
    for key, node in ipairs(model.forwardnodes) do
        if node.data.annotations.name == "bias" then
            node.data.module.bias[{{layerNum + 1, 2 * layerNum}}]:fill(1.0)
        end
    end

    print("Parameters in the model: "..params:nElement())

    local models = UClone.cloneNetOverTime(model, sequenceLength, not model.parameters)
    local criterions = UClone.cloneNetOverTime(criterion, sequenceLength, not criterion.parameters)

    local initialState = Gradient.getInitialState(layerSize, layerNum, hiddenStateNum)

    function backpropagation(p)
        if p ~= params then
            params:copy(p)
        end
        gradParams:zero()

        local states = {[0] = initialState}
        local predictions = {}
        local loss = 0

        for t = 1, sequenceLength do
            local inputVector = currentSequence[t][1]
            local expectedOutputVector = currentSequence[t][2]

            models[t]:training()
            local output = models[t]:forward({inputVector, unpack(states[t - 1])})
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
            local derivative = models[t]:backward({inputVector, unpack(states[t - 1])}, finalState[t])
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
    local minLoss = 1.0
    local optimizationState = {learningRate = learningRate, alpha = decayRate}
    local iterations = maxEpochs * sequenceLength
    local j = 0

    for i = 1, iterations do
        j = j + 1
        if j == #dataset + 1 then
            j = 1
        end

        currentSequence = dataset[j]

        local epoch = i / sequenceLength
        local newParams, loss = optim.rmsprop(backpropagation, params, optimizationState)
        params = newParams

        local currentLoss = loss[1]

        if currentLoss < minLoss then
            print("----> min loss "..currentLoss)
            minLoss = currentLoss
            torch.save("neural_net", model)
        end

        losses[i] = currentLoss

        if i % sequenceLength == 0 and learningRateDecay < 1 and epoch >= learningRateDecayAfter then
            optimizationState.learningRate = optimizationState.learningRate * learningRateDecay
            print("Decayed learning rate by a factor "..learningRateDecay.." to "..optimizationState.learningRate)
        end

        print(i.."/"..iterations..", epoch: "..epoch..", loss: "..currentLoss)
        
        if i % 10 == 0 then collectgarbage() end
    end

    return losses
end

function Gradient.evaluate(model, dataset)
    local layerSize = model.layerSize
    local layerNum = model.layerNum
    local hiddenStateNum = model.hiddenStateNum

    local sequenceLength = dataset.metaData.sequenceLength

    local models = UClone.cloneNetOverTime(model, sequenceLength, not model.parameters)
    local states = {[0] = Gradient.getInitialState(layerSize, layerNum, hiddenStateNum)}
    
    local results = {}
    for i = 1, dataset:size() do
        currentSequence = dataset[i]

        local expectedOutputVector = nil
        local accumulativePrediction = torch.zeros(dataset.metaData.outputSize)
        for t = 1, sequenceLength do
            local inputVector = currentSequence[t][1]
            expectedOutputVector = currentSequence[t][2]

            models[t]:evaluate()
            local output = models[t]:forward({inputVector, unpack(states[t - 1])})
            
            states[t] = {}
            for i=1, #output - 1 do
                table.insert(states[t], output[i])
            end

            if t > sequenceLength / 4 then
                local prediction = output[#output]
                accumulativePrediction = torch.add(accumulativePrediction, prediction)
            end
        end

        states[0] = states[#states]
        
        print(i.."/"..dataset:size())

        if i % 10 == 0 then collectgarbage() end

        local v, index = torch.max(expectedOutputVector, 1)
        indexExpected = torch.sum(index)
        v, index = torch.max(accumulativePrediction, 1)
        indexPredicted = torch.sum(index)

        results[i] = {expected = indexExpected, predicted = indexPredicted, output = UMath.normalizeTensor(accumulativePrediction)}
    end

    return results
end

function Gradient.trainFeedforward(model, criterion, dataset, config)
    local config = config or {}
    local initWeight = config.initWeight
    local gradientClip = config.gradientClip
    local learningRate = config.learningRate
    local decayRate = config.decayRate
    local learningRateDecay = config.learningRateDecay
    local learningRateDecayAfter = config.learningRateDecayAfter
    local maxEpochs = config.maxEpochs

    local layerSize = model.layerSize
    local layerNum = model.layerNum

    local sequenceLength = dataset.metaData.sequenceLength
    local currentSequence = nil

    local params, gradParams = model:getParameters()
    params:uniform(-initWeight, initWeight)

    print("Parameters in the model: "..params:nElement())

    function backpropagation(p)
        if p ~= params then
            params:copy(p)
        end
        gradParams:zero()

        local predictions = {}
        local loss = 0

        for t = 1, sequenceLength do
            local inputVector = currentSequence[t][1]
            local expectedOutputVector = currentSequence[t][2]

            model:training()
            local output = model:forward(inputVector)
            predictions[t] = output
            loss = loss + criterion:forward(predictions[t], expectedOutputVector)
        end

        loss = loss / sequenceLength
        
        for t = sequenceLength, 1, -1 do
            local inputVector = currentSequence[t][1]
            local expectedOutputVector = currentSequence[t][2]

            local backpropagatedState = criterion:backward(predictions[t], expectedOutputVector)
            local derivative = model:backward(inputVector, backpropagatedState)
        end
        
        gradParams:clamp(-gradientClip, gradientClip)
        return loss, gradParams
    end

    local losses = {}
    local minLoss = 1.0
    local optimizationState = {learningRate = learningRate, alpha = decayRate}
    local iterations = maxEpochs * sequenceLength
    local j = 0

    for i = 1, iterations do
        j = j + 1
        if j == #dataset + 1 then
            j = 1
        end

        currentSequence = dataset[j]

        local epoch = i / sequenceLength
        local newParams, loss = optim.rmsprop(backpropagation, params, optimizationState)

        local currentLoss = loss[1]
        losses[i] = currentLoss

        if currentLoss < minLoss then
            print("----> min loss "..currentLoss)
            minLoss = currentLoss
            torch.save("neural_net", model)
        end

        if i % sequenceLength == 0 and learningRateDecay < 1 and epoch >= learningRateDecayAfter then
            optimizationState.learningRate = optimizationState.learningRate * learningRateDecay
            print("Decayed learning rate by a factor "..learningRateDecay.." to "..optimizationState.learningRate)
        end

        print(i.."/"..iterations..", epoch: "..epoch..", loss: "..currentLoss)
        
        if i % 10 == 0 then collectgarbage() end
    end

    return losses
end

function Gradient.evaluateFeedforward(model, dataset)
    local layerSize = model.layerSize
    local layerNum = model.layerNum
    
    local sequenceLength = dataset.metaData.sequenceLength

    local results = {}
    for i = 1, dataset:size() do
        currentSequence = dataset[i]

        local expectedOutputVector = nil
        local accumulativePrediction = torch.zeros(dataset.metaData.outputSize)
        for t = 1, sequenceLength do
            local inputVector = currentSequence[t][1]
            expectedOutputVector = currentSequence[t][2]

            model:evaluate()
            local output = model:forward(inputVector)
            local prediction = output
            accumulativePrediction = torch.add(accumulativePrediction, prediction)
        end

        print(i.."/"..dataset:size())

        if i % 10 == 0 then collectgarbage() end

        local v, index = torch.max(expectedOutputVector, 1)
        indexExpected = torch.sum(index)
        v, index = torch.max(accumulativePrediction, 1)
        indexPredicted = torch.sum(index)

        results[i] = {expected = indexExpected, predicted = indexPredicted, output = UMath.normalizeTensor(accumulativePrediction)}
    end

    return results
end

return Gradient