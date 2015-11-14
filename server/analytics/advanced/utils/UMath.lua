-- Author Tony Beltramelli www.tonybeltramelli.com - 13/11/2015

local UMath = {}

function UMath.normalize(rangeMin, rangeMax, x, xMin, xMax)
	return rangeMin + (((x - xMin) * (rangeMax - rangeMin)) * (1 / (xMax - xMin)))
end

function UMath.normalizeTensor(tensor)
	local min = torch.min(tensor, 1)[1]
	local max = torch.max(tensor, 1)[1]
	local t = tensor:storage()
	
	for i = 1, #t do
		t[i] = UMath.normalize(0.0, 1.0, t[i], min, max)
	end
	return torch.Tensor(t)
end

return UMath