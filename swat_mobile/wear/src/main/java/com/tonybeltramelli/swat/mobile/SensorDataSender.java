package com.tonybeltramelli.swat.mobile;

import android.content.Context;
import android.util.Log;

import com.google.android.gms.common.api.ResultCallback;
import com.google.android.gms.wearable.DataApi;
import com.google.android.gms.wearable.PutDataMapRequest;
import com.google.android.gms.wearable.PutDataRequest;
import com.google.android.gms.wearable.Wearable;
import com.tonybeltramelli.swat.mobile.common.AThreadedClient;
import com.tonybeltramelli.swat.mobile.common.Const;

/**
 * Created by tbeltramelli on 11/08/15.
 */
public class SensorDataSender extends AThreadedClient
{
    protected SensorDataSender(Context context)
    {
        super(context);
    }

    public void sendSensorData(final int sensorType, final int accuracy, final long timestamp, final float[] values)
    {
        System.out.print("-------> send sensor data");

        _threadPool.submit(new Runnable()
        {
            @Override
            public void run()
            {
                PutDataMapRequest dataMap = PutDataMapRequest.create(Const.SENSOR_ROOT + sensorType);
                dataMap.getDataMap().putLong(Const.TIMESTAMP, timestamp);
                dataMap.getDataMap().putFloatArray(Const.VALUES, values);

                PutDataRequest putDataRequest = dataMap.asPutDataRequest();

                _sendSensorDataInBackground(putDataRequest);
            }
        });
    }

    private void _sendSensorDataInBackground(PutDataRequest data)
    {
        if (!_isConnected()) return;

        Wearable.DataApi.putDataItem(_client, data).setResultCallback(new ResultCallback<DataApi.DataItemResult>()
        {
            @Override
            public void onResult(DataApi.DataItemResult dataItemResult)
            {
                Log.d(this.getClass().getName(), "Sending sensor data: " + dataItemResult.getStatus().isSuccess());
            }
        });
    }
}
