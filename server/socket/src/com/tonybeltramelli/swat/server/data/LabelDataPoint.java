package com.tonybeltramelli.swat.server.data;

import com.tonybeltramelli.swat.server.Const;
import org.json.simple.JSONObject;

/**
 * @author Tony Beltramelli www.tonybeltramelli.com - created 06/09/15
 */
public class LabelDataPoint extends ADataPoint
{
    private String _label;

    public LabelDataPoint(JSONObject values)
    {
        _timestamp = ((Number) values.get(Const.TIMESTAMP)).longValue();
        _label = (String) values.get(Const.LABEL);
    }

    @Override
    public String toString()
    {
        return super.toString() + " timestamp:" + _timestamp + ", label: " +_label;
    }

    @Override
    public String getCSVLine()
    {
        return _timestamp + "," + _label;
    }

    @Override
    public String getCSVHeader()
    {
        return Const.CSV_HEADER_LABEL;
    }
}
