package com.tonybeltramelli.swat.mobile;

import android.content.Context;

import com.google.android.gms.common.api.ResultCallback;
import com.google.android.gms.wearable.DataApi;
import com.google.android.gms.wearable.MessageApi;
import com.google.android.gms.wearable.PutDataMapRequest;
import com.google.android.gms.wearable.PutDataRequest;
import com.google.android.gms.wearable.Wearable;
import com.tonybeltramelli.swat.mobile.common.AThreadedClient;
import com.tonybeltramelli.swat.mobile.common.Const;
import com.tonybeltramelli.swat.mobile.common.Out;

import java.security.SecureRandom;
import java.util.Date;

/**
 * Created by Tony Beltramelli www.tonybeltramelli.com on 11/08/15.
 * Adapted from https://github.com/pocmo/SensorDashboard
 */
public class SensorDataSender extends AThreadedClient
{
    private static SensorDataSender _instance = null;

    private int _dataToSend;
    private int _dataSent;

    private SensorDataSender(Context context)
    {
        super(context);
    }

    public void init()
    {
        _dataToSend = 0;
        _dataSent = 0;
    }

    public static SensorDataSender getInstance(Context context)
    {
        if (_instance == null)
        {
            _instance = new SensorDataSender(context);
        }

        return _instance;
    }

    public void sendSensorData(final int sensorType, final long timestamp, final float[] values)
    {
        _dataToSend += 1;

        _threadPool.submit(new Runnable()
        {
            @Override
            public void run()
            {
                PutDataMapRequest dataMap = PutDataMapRequest.create(Const.SENSOR_ROOT + sensorType);
                dataMap.getDataMap().putLong(Const.TIMESTAMP, timestamp);
                dataMap.getDataMap().putFloatArray(Const.VALUES, values);

                PutDataRequest putDataRequest = dataMap.asPutDataRequest();

                if (!isConnected()) return;

                Wearable.DataApi.putDataItem(_client, putDataRequest).setResultCallback(new ResultCallback<DataApi.DataItemResult>()
                {
                    @Override
                    public void onResult(DataApi.DataItemResult dataItemResult)
                    {
                        Out.print("Sent sensor data: " + dataItemResult.getStatus().isSuccess());

                        _dataSent += 1;
                        if(_dataSent == _dataToSend)
                        {
                            _sendEndSignal();
                        }
                    }
                });
            }
        });
    }

    private void _sendEndSignal()
    {
        init();
        PutDataMapRequest dataMap = PutDataMapRequest.create(Const.END_SESSION + new Date().getTime());
        PutDataRequest putDataRequest = dataMap.asPutDataRequest();

        if (!isConnected()) return;

        Wearable.DataApi.putDataItem(_client, putDataRequest).setResultCallback(new ResultCallback<DataApi.DataItemResult>()
        {
            @Override
            public void onResult(DataApi.DataItemResult dataItemResult)
            {
                Out.print("Sent end signal: " + dataItemResult.getStatus().isSuccess());
            }
        });
    }
}
