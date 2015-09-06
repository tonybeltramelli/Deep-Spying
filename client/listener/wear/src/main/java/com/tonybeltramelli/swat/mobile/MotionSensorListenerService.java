package com.tonybeltramelli.swat.mobile;

import android.app.Service;
import android.content.Intent;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.os.IBinder;

import com.tonybeltramelli.swat.mobile.common.Out;

/**
 * Created by Tony Beltramelli www.tonybeltramelli.com on 05/08/15.
 */
public class MotionSensorListenerService extends Service implements SensorEventListener
{
    private SensorManager _sensorManager;

    @Override
    public void onCreate()
    {
        super.onCreate();

        _sensorManager = (SensorManager) getSystemService(SENSOR_SERVICE);

        _listenTo(Sensor.TYPE_ACCELEROMETER);
        _listenTo(Sensor.TYPE_GYROSCOPE);
    }

    private void _listenTo(final int TYPE)
    {
        Sensor sensor = _sensorManager.getDefaultSensor(TYPE);

        if (!_isSupported(sensor)) return;

        _sensorManager.registerListener(this, sensor, sensor.getMaxDelay());
    }

    @Override
    public void onSensorChanged(SensorEvent event)
    {
        long timestamp = System.currentTimeMillis();
        SensorDataSender.getInstance(getApplicationContext()).sendSensorData(event.sensor.getType(), timestamp, event.values);
    }

    @Override
    public void onAccuracyChanged(Sensor sensor, int accuracy)
    {

    }

    private boolean _isSupported(Sensor sensor)
    {
        boolean isSupported = !(sensor == null);

        if (isSupported)
        {
            Out.print("Sensor " + sensor.getName() + " type " + sensor.getType() + " found.");
        } else
        {
            Out.print("Sensor " + sensor.getName() + " type " + sensor.getType() + " not found.");
        }

        return isSupported;
    }

    @Override
    public IBinder onBind(Intent intent)
    {
        return null;
    }

    @Override
    public void onDestroy()
    {
        super.onDestroy();

        _sensorManager.unregisterListener(this);
    }
}
