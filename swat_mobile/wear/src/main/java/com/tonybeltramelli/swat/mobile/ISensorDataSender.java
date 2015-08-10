package com.tonybeltramelli.swat.mobile;

/**
 * Created by tbeltramelli on 05/08/15.
 */
public interface ISensorDataSender {
    void sendSensorData(final int sensorType, final int accuracy, final long timestamp, final float[] values);
}
