package com.tonybeltramelli.swat.server.data;

import com.tonybeltramelli.swat.server.Const;
import org.json.simple.JSONObject;

/**
 * @author Tony Beltramelli www.tonybeltramelli.com - created 28/08/15
 */
public class SensorDataPoint extends ADataPoint
{
    private double _x;
    private double _y;
    private double _z;

    public SensorDataPoint(JSONObject values)
    {
        _timestamp = ((Number) values.get(Const.TIMESTAMP)).longValue();
        _x = ((Number) values.get(Const.X)).doubleValue();
        _y = ((Number) values.get(Const.Y)).doubleValue();
        _z = ((Number) values.get(Const.Z)).doubleValue();
    }

    @Override
    public String toString()
    {
        return super.toString() + " timestamp:" + _timestamp + ", x: " +_x + ", y: " +_y+", z: "+_z;
    }

    @Override
    public String getCSVLine()
    {
        return _timestamp + "," + _x + "," + _y + "," + _z;
    }

    @Override
    public String getCSVHeader()
    {
        return Const.CSV_HEADER_SENSOR;
    }
}
