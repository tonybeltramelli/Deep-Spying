package com.tonybeltramelli.swat.mobile;

import android.app.Activity;
import android.app.Service;
import android.content.Intent;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.os.IBinder;
import android.util.Log;

/**
 * Created by tbeltramelli on 05/08/15.
 */
public class MotionSensorService extends Service implements SensorEventListener {

    private SensorManager _sensorManager;

    private Sensor _accelerometer;
    private Sensor _gyroscope;

    @Override
    public void onCreate() {
        super.onCreate();

        _sensorManager = (SensorManager) getSystemService(SENSOR_SERVICE);

        _accelerometer = _sensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER);
        _gyroscope = _sensorManager.getDefaultSensor(Sensor.TYPE_GYROSCOPE);

        _startListening();
    }

    @Override
    public void onSensorChanged(SensorEvent event) {
        //Log.wtf(this.getClass().getName(), event.sensor.getType() + " " + event.accuracy + " " + event.timestamp + " " + event.values);
        DataManager.getInstance(this).sendSensorData(event.sensor.getType(), event.accuracy, event.timestamp, event.values);
    }

    @Override
    public void onAccuracyChanged(Sensor sensor, int accuracy) {

    }

    private void _startListening()
    {
        if(!(_isSupported(_accelerometer) && _isSupported(_gyroscope))) return;

        _sensorManager.registerListener(this, _accelerometer, SensorManager.SENSOR_DELAY_NORMAL);
        _sensorManager.registerListener(this, _gyroscope, SensorManager.SENSOR_DELAY_NORMAL);
    }

    private void _stopListening()
    {
        _sensorManager.unregisterListener(this);
    }

    private boolean _isSupported(Sensor sensor)
    {
        boolean isSupported = !(sensor == null);

        if (!isSupported)
        {
            Log.d(this.getClass().getName(), "Sensor " + sensor.getName() + " type " + sensor.getType() + " not found.");
        }else{
            Log.d(this.getClass().getName(), "Sensor " + sensor.getName() + " type " + sensor.getType() + " found.");
        }

        return isSupported;
    }

    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }

    @Override
    public void onDestroy() {
        super.onDestroy();

        _stopListening();
    }
}
