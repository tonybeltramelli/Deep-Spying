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
 * Created by tbeltramelli on 05/08/15.
 */
public class MotionSensorListenerService extends Service implements SensorEventListener
{
    private SensorManager _sensorManager;
    private SensorDataSender _sensorDataSender;

    @Override
    public void onCreate()
    {
        super.onCreate();

        _sensorManager = (SensorManager) getSystemService(SENSOR_SERVICE);
        _sensorDataSender = new SensorDataSender(getApplicationContext());

        _listenTo(Sensor.TYPE_ACCELEROMETER);
        _listenTo(Sensor.TYPE_GYROSCOPE);
    }

    private void _listenTo(final int TYPE)
    {
        Sensor sensor = _sensorManager.getDefaultSensor(TYPE);

        if (!_isSupported(sensor)) return;

        _sensorManager.registerListener(this, sensor, SensorManager.SENSOR_DELAY_NORMAL);
    }

    @Override
    public void onSensorChanged(SensorEvent event)
    {
        //Out.print(event.sensor.getType() + " " + event.accuracy + " " + event.timestamp + " " + event.values);
        _sensorDataSender.sendSensorData(event.sensor.getType(), event.accuracy, event.timestamp, event.values);
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
        _sensorDataSender.kill();
    }
}
