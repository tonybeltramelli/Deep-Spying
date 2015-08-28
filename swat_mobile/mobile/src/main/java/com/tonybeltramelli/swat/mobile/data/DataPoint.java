package com.tonybeltramelli.swat.mobile.data;

import com.tonybeltramelli.swat.mobile.common.Const;

import org.json.JSONException;
import org.json.JSONObject;

/**
 * Created by Tony Beltramelli www.tonybeltramelli.com on 12/08/15.
 */
public class DataPoint
{
    private String _sensorName;
    private long _timestamp;
    private float _x;
    private float _y;
    private float _z;

    public DataPoint(String sensorName, long timestamp, float x, float y, float z)
    {
        _sensorName = sensorName;
        _timestamp = timestamp;
        _x = x;
        _y = y;
        _z = z;
    }

    @Override
    public String toString()
    {
        return super.toString() + " timestamp:" + _timestamp + ", x: " +_x + ", y: " +_y+", z: "+_z;
    }

    public JSONObject getJSONObject() throws JSONException
    {
        JSONObject root = new JSONObject();
        root.put(Const.TIMESTAMP, _timestamp);
        root.put(Const.X, _x);
        root.put(Const.Y, _y);
        root.put(Const.Z, _z);

        return root;
    }
}
