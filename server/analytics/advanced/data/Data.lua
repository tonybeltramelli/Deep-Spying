-- Author Tony Beltramelli www.tonybeltramelli.com - 10/11/2015

local Data = {}

function Data.makeBinaryClasses(labelSet)
	Data.classes = {}
	local len = #labelSet

	for i = 1, len do
		local t = torch.zeros(1, len)
		local binClasses = t:storage()

		binClasses[i] = 1
		Data.classes[labelSet[i]] = torch.Tensor(binClasses)
	end
end

function Data.load(path, labelSet)
	Data.makeBinaryClasses(labelSet)

	Data.dataset = {}
	Data.dataset.metaData = nil

	for file in lfs.dir(path) do
	    if string.match(file, ".data") then
	    	local data = io.open(path..file, "r")
	    	local sequence = nil

	    	if data then
	    		local outputVect = nil

	    		for line in data:lines() do
	    			if string.match(line, ":") then
	    				local s, e = string.find(line, ":")
		                local label = string.sub(line, s + 1)

		                if sequence then
		                	table.insert(Data.dataset, sequence)

		                	if not Data.dataset.metaData.sequenceLength then
		                		Data.dataset.metaData['sequenceLength'] = #sequence
		                	end
		                end

		                sequence = {}
		                outputVect = Data.classes[label]
		            elseif string.match(line, ".") then
		            	dataPoints = line:split(",")
		            	
		            	local len = #dataPoints
		            	local t = torch.Tensor(1, len)
		            	local inputVect = t:storage()

		            	for j = 1, len do
		            		inputVect[j] = dataPoints[j]
		            	end

		            	table.insert(sequence, {torch.Tensor(inputVect), outputVect})

		            	if Data.dataset.metaData == nil then
		            		Data.dataset.metaData = {inputSize = len, outputSize = #labelSet}
		            	end
		            end
				end
			end

	    	data.close()
	    end
	end
	function Data.dataset:size() return #Data.dataset end
end

function Data.shuffle()
	local indices = torch.randperm(Data.dataset:size())
	
end

return Data
