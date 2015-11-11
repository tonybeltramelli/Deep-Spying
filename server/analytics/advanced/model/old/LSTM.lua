local LSTM = {}

function LSTM.model(inputSize, outputSize, hiddenLayers, initWeight)
  local function lstmCell(input, prevY, prevC, layerSize)
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

  local x = nn.Identity()()
  local y = nn.Identity()()
  local prevY = nn.Identity()()
  local inputs = {[0] = nn.LookupTable(inputSize, hiddenLayers[0])(x)}
  local nextOutput = {}
  local splitted = {prevOutput:split(2 * #hiddenLayers)}

  for i = 1, #hiddenLayers do
    local prevC = splitted[2 * i - 1]
    local prevY = splitted[2 * i]
    local dropped = nn.Dropout()(inputs[i - 1])

    local nextY, nextC = lstmCell(dropped, prevY, prevC, hiddenLayers[i])

    table.insert(nextOutput, nextC)
    table.insert(nextOutput, nextY)

    inputs[i] = nextOutput
  end

  local nextYi = nn.Linear(hiddenLayers[#hiddenLayers], outputSize)
  local dropped = nn.Dropout()(inputs[#hiddenLayers])
  local prediction = nn.LogSoftMax()(h2y(dropped))
  local err = nn.ClassNLLCriterion()({prediction, nextYi})

  local m = nn.gModule({x, y, prevY}, {err, nn.Identity()(nextOutput)})
  m:getParameters():uniform(-initWeight, initWeight)
  return m
end

return LSTM

