package com.tonybeltramelli.swat.mobile;

import android.content.Context;
import android.hardware.Sensor;

import com.google.android.gms.common.ConnectionResult;
import com.google.android.gms.common.api.GoogleApiClient;
import com.google.android.gms.wearable.DataMap;
import com.google.android.gms.wearable.Wearable;
import com.tonybeltramelli.swat.mobile.common.Const;
import com.tonybeltramelli.swat.mobile.common.Out;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

/**
 * Created by tbeltramelli on 10/08/15.
 */
public class DataManager
{
    private static DataManager _instance = null;

    private DataManager()
    {
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
        Out.print("--> got sensor data " + getSensorName(sensorType));
    }

    public String getSensorName(int sensorType)
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
}
