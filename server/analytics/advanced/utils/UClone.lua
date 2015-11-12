-- Author Tony Beltramelli www.tonybeltramelli.com - 11/11/2015
-- Adapted from https://github.com/wojciechz/learning_to_execute and https://github.com/karpathy/char-rnn/

local UClone = {}

function UClone.cloneNetOverTime(net, time)
	local clones = {}

    local params, gradParams
    if net.parameters then
        params, gradParams = net:parameters()
        if params == nil then
            params = {}
        end
    end

    local paramsNoGrad
    if net.parametersNoGrad then
        paramsNoGrad = net:parametersNoGrad()
    end

    local mem = torch.MemoryFile("w"):binary()
    mem:writeObject(net)

    for t = 1, time do
        local reader = torch.MemoryFile(mem:storage(), "r"):binary()
        local clone = reader:readObject()
        reader:close()

        if net.parameters then
            local cloneParams, cloneGradParams = clone:parameters()
            local cloneParamsNoGrad
            for i = 1, #params do
                cloneParams[i]:set(params[i])
                cloneGradParams[i]:set(gradParams[i])
            end
            if paramsNoGrad then
                cloneParamsNoGrad = clone:parametersNoGrad()
                for i =1,#paramsNoGrad do
                    cloneParamsNoGrad[i]:set(paramsNoGrad[i])
                end
            end
        end

        clones[t] = clone
        collectgarbage()
    end

    mem:close()
    return clones
end

function UClone.cloneList(list, toZero)
    local out = {}
    for k,v in pairs(list) do
        out[k] = v:clone()
        if toZero then out[k]:zero() end
    end
    return out
end

return UClone
