package com.tonybeltramelli.swat.mobile.data;

import android.app.Activity;
import android.hardware.Sensor;
import android.preference.PreferenceManager;

import com.tonybeltramelli.swat.mobile.common.Const;
import com.tonybeltramelli.swat.mobile.common.Out;

import org.json.JSONException;

/**
 * Created by Tony Beltramelli www.tonybeltramelli.com on 10/08/15.
 */
public class DataManager
{
    private static DataManager _instance = null;

    private DataStore _dataStore;
    private String _serverAddress;
    private String _serverPort;
    private Activity _context;

    private DataManager()
    {
        _dataStore = new DataStore();
    }

    public static DataManager getInstance()
    {
        if (_instance == null)
        {
            _instance = new DataManager();
        }

        return _instance;
    }

    public void storeSensorData(final int sensorType, final long timestamp, final float[] values)
    {
        if(values.length < 3) return;

        String sensorName = _getSensorName(sensorType);

        DataPoint dataPoint = new DataPoint(
                sensorName,
                timestamp,
                values[0],
                values[1],
                values[2]
        );

        if(_dataStore.push(sensorName, dataPoint))
        {
            try
            {
                String jsonString = _dataStore.getJSONString(sensorName);
                Out.print("full "+sensorName);
            } catch (JSONException e)
            {
                Out.report(e.getMessage());
            }
        }
    }

    private String _getSensorName(int sensorType)
    {
        String sensorName;

        switch (sensorType){
            case Sensor.TYPE_ACCELEROMETER:
                sensorName = Const.ACCELEROMETER;
                break;
            case Sensor.TYPE_GYROSCOPE:
                sensorName = Const.GYROSCOPE;
                break;
            default:
                sensorName = Const.UNSUPPORTED;
                break;
        }

        return sensorName;
    }

    public void setContext(Activity context)
    {
        _context = context;
        savePreferences();
    }

    public void savePreferences()
    {
        _serverAddress = PreferenceManager.getDefaultSharedPreferences(_context).getString(Const.PREF_KEY_SERVER_ADDRESS, "");
        _serverPort = PreferenceManager.getDefaultSharedPreferences(_context).getString(Const.PREF_KEY_SERVER_PORT, "");
    }
}
