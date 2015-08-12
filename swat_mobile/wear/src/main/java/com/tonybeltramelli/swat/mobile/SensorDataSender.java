package com.tonybeltramelli.swat.mobile;

import android.content.Context;

import com.google.android.gms.common.api.ResultCallback;
import com.google.android.gms.wearable.DataApi;
import com.google.android.gms.wearable.PutDataMapRequest;
import com.google.android.gms.wearable.PutDataRequest;
import com.google.android.gms.wearable.Wearable;
import com.tonybeltramelli.swat.mobile.common.AThreadedClient;
import com.tonybeltramelli.swat.mobile.common.Const;
import com.tonybeltramelli.swat.mobile.common.Out;

/**
 * Created by Tony Beltramelli www.tonybeltramelli.com on 11/08/15.
 */
public class SensorDataSender extends AThreadedClient
{
    protected SensorDataSender(Context context)
    {
        super(context);
    }

    public void sendSensorData(final int sensorType, final int accuracy, final long timestamp, final float[] values)
    {
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
        if (!isConnected()) return;

        Wearable.DataApi.putDataItem(_client, data).setResultCallback(new ResultCallback<DataApi.DataItemResult>()
        {
            @Override
            public void onResult(DataApi.DataItemResult dataItemResult)
            {
                Out.print("Sending sensor data: " + dataItemResult.getStatus().isSuccess());
            }
        });
    }
}
