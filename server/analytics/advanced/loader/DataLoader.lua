local DataLoader = {}

function DataLoader.makeBinaryClasses(labelSet)
	DataLoader.classes = {}
	local len = #labelSet

	for i = 1, len do
		local t = torch.zeros(1, len)
		local binClasses = t:storage()

		binClasses[i] = 1
		DataLoader.classes[labelSet[i]] = torch.Tensor(binClasses)
	end
end

function DataLoader.load(path, labelSet)
	DataLoader.makeBinaryClasses(labelSet)

	DataLoader.dataset = {}
	DataLoader.dataset.metaData = nil

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
		                	table.insert(DataLoader.dataset, sequence)

		                	if not DataLoader.dataset.metaData.sequenceLength then
		                		DataLoader.dataset.metaData['sequenceLength'] = #sequence
		                	end
		                end

		                sequence = {}
		                outputVect = DataLoader.classes[label]
		            elseif string.match(line, ".") then
		            	dataPoints = line:split(",")
		            	
		            	local len = #dataPoints
		            	local t = torch.Tensor(1, len)
		            	local inputVect = t:storage()

		            	for j = 1, len do
		            		inputVect[j] = dataPoints[j]
		            	end

		            	table.insert(sequence, {torch.Tensor(inputVect), outputVect})

		            	if DataLoader.dataset.metaData == nil then
		            		DataLoader.dataset.metaData = {inputSize = len, outputSize = #labelSet}
		            	end
		            end
				end
			end

	    	data.close()
	    end
	end
	function DataLoader.dataset:size() return #DataLoader.dataset end
end

return DataLoader
