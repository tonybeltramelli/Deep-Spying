-- Author Tony Beltramelli www.tonybeltramelli.com - 13/11/2015

local Report = {}

Report.training = {}
Report.evaluation = {}

function Report.store(losses, results, labels, datasetSize)
	for i = 1, #losses do
		table.insert(Report.training, tostring(losses[i]))
	end
	table.insert(Report.training, "--")

	for i = 1, #results do
		local expectedLabel = labels[results[i].predicted]
		local predictedLabel = labels[results[i].expected]
		local output = Report.toFlatString(results[i].output)

		table.insert(Report.evaluation, expectedLabel.."|"..predictedLabel.."|"..output)
	end
	table.insert(Report.evaluation, "--"..datasetSize)

	collectgarbage()
end

function Report.save(path)
	local file = io.open(path.."_training", "w")

	for i = 1, #Report.training do
		file:write(Report.training[i].."\n")
	end
	file:close()

	file = io.open(path.."_evaluation", "w")

	for i = 1, #Report.evaluation do
		file:write(Report.evaluation[i].."\n")
	end
	file:close()

	Report.training = {}
	Report.evaluation = {}

	collectgarbage()
end

function Report.toFlatString(tensor)
	local t = tensor:storage()
	local s = t[1]

	for i = 2, #t do
		s = s..","..t[i]
	end
	return s
end

return Report
