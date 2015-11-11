-- adapted from https://github.com/karpathy/char-rnn/ and https://github.com/oxford-cs-ml-2015/practical6/

local Trainer = {}

-- example config:
-- {
--   initWeight : 0.08
--   learningRate : 0.002
--   sequenceLength : 50
--   layerSize : 128
--   decayRate : 0.95
--   layerNum : 2
--   gradientClip : 5
--   learningRateDecay : 0.97
--   maxEpochs : 50
-- }

function Trainer.trainRecurrent(model, criterion, dataset, config)
    local config = config or {}
    
    local sequenceLength = config.sequenceLength
    local initWeight = config.initWeight
    local layerSize = config.layerSize
    local layerNum = config.layerNum
    local gradientClip = config.gradientClip
    local learningRate = config.learningRate
    local decayRate = config.decayRate
    local learningRateDecay = config.learningRateDecay
    local learningRateDecayAfter = config.learningRateDecayAfter
    local maxEpochs = config.maxEpochs

    local currentSequence = nil

    local params, gradParams = model:getParameters()
    params:uniform(-initWeight, initWeight)

    print('Parameters in the model: ' .. params:nElement())

    local models = UClone.cloneNetOverTime(model, sequenceLength, not model.parameters)
    local criterions = UClone.cloneNetOverTime(criterion, sequenceLength, not criterion.parameters)

    local initialState = {}
    for L=1,layerNum do
        local emptyVector = torch.zeros(1, layerSize)
        table.insert(initialState, emptyVector:clone())
        table.insert(initialState, emptyVector:clone())
    end

    function backpropagation(p)
        if p ~= params then
            params:copy(p)
        end
        gradParams:zero()

        local state = {[0] = UClone.cloneList(initialState)}
        local predictions = {}
        local loss = 0

        for t = 1, sequenceLength do
            local inputVector = currentSequence[t][1]
            local expectedOutputVector = currentSequence[t][2]

            models[t]:training()
            local output = models[t]:forward{inputVector, unpack(state[t - 1])}
            predictions[t] = output[#output]
            loss = loss + criterions[t]:forward(predictions[t], expectedOutputVector)

            state[t] = {}
            for i=1, #output - 1 do
                table.insert(state[t], output[i])
            end
        end

        loss = loss / sequenceLength
        
        local finalState = {[sequenceLength] = UClone.cloneList(initialState, true)}
        for t = sequenceLength, 1, -1 do
            local inputVector = currentSequence[t][1]
            local expectedOutputVector = currentSequence[t][2]

            local backpropagatedState = criterions[t]:backward(predictions[t], expectedOutputVector)
            table.insert(finalState[t], backpropagatedState)
            local derivative = models[t]:backward({inputVector, unpack(state[t-1])}, finalState[t])
            finalState[t-1] = {}

            for k,v in pairs(derivative) do
                if k > 1 then
                    finalState[t-1][k-1] = v
                end
            end
        end
        
        initialState = state[#state]
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
                print('decayed learning rate by a factor ' .. decay_factor .. ' to ' .. optimization.learningRate)
            end
        end

        print(string.format("%d/%d (epoch %.3f), train_loss = %6.8f, grad/param norm = %6.4e", i, iterations, epoch, currentLoss, gradParams:norm() / params:norm()))
        
        if i % 10 == 0 then collectgarbage() end

        if loss[1] ~= loss[1] then
            print('loss is NaN.  This usually indicates a bug.  Please check the issues page for existing issues, or create a new issue, if none exist.  Ideally, please state: your operating system, 32-bit/64-bit, your blas version, cpu/cuda/cl?')
            break
        end
        if lossBug == nil then lossBug = loss[1] end
        if loss[1] > lossBug * 3 then
            print('loss is exploding, aborting.')
            break
        end
    end
end

return Trainer