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

-- Data.dataset
-- example dataset of size n:
-- { -- sequence 1 of length m
-- 		{
-- 			1 : Tensor -- input 1
-- 			2 : Tensor -- output 1
-- 		}
-- 			...
-- 		{
-- 			1 : Tensor -- input m
-- 			2 : Tensor -- output m
-- 		}
-- 	}
-- 		...
-- 	{ -- sequence n
-- 		...
-- 	}
function Data.getNewDataset()
	local dataset = {}
	dataset.metaData = nil

	function dataset.insertInto(sequence, element)
		table.insert(sequence, element)
		dataset.setMetaData(element)
	end

	function dataset.insertSequence(sequence)
		table.insert(dataset, sequence)
		dataset.setMetaData(sequence[1])

		if not dataset.metaData.sequenceLength then
			dataset.metaData['sequenceLength'] = #sequence
		end
	end

	function dataset.setMetaData(element)
		if dataset.metaData == nil then
			dataset.metaData = {inputSize = element[1]:size()[1], outputSize = element[2]:size()[1]}
		end
	end

	function dataset:size() return #dataset end
	return dataset
end

function Data.load(path, labelSet)
	Data.makeBinaryClasses(labelSet)

	local dataset = Data.getNewDataset()

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
		                	dataset.insertSequence(sequence)
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

		            	dataset.insertInto(sequence, {torch.Tensor(inputVect), outputVect})
		            end
				end
			end

	    	data:close()
	    end
	end

	print("Dataset of size "..dataset:size().." loaded")
	
	return dataset
end

function Data.shuffleAndSplit(dataset, k)
	local indices = torch.randperm(dataset:size()):storage()
	local step =  math.floor(#indices / k)
	local remainder = #indices % k

	local datasets = {}

	for i = 1, #indices, step do
		local subDataset = Data.getNewDataset()

		local e = i + step - 1
		local toBreak = false

		if (e + step) > #indices then
			e = #indices
			toBreak = true
		end

		for j = i, e do
			subDataset.insertSequence(dataset[j])
		end

		table.insert(datasets, subDataset)
		if toBreak then break end
	end

	return datasets
end

function Data.excludeAndMerge(datasets, excludedIndex)
	local dataset = Data.getNewDataset()

	for i = 1, #datasets do
		if i ~= excludedIndex then
			local subDataset = datasets[i]
			for j = 1, #subDataset do
				dataset.insertSequence(subDataset[j])
			end
		end 
	end

	return dataset
end

return Data
