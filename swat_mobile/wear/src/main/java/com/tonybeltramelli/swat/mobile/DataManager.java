package com.tonybeltramelli.swat.mobile;

import android.content.Context;
import android.util.Log;

import com.google.android.gms.common.ConnectionResult;
import com.google.android.gms.common.api.GoogleApiClient;
import com.google.android.gms.common.api.ResultCallback;
import com.google.android.gms.wearable.DataApi;
import com.google.android.gms.wearable.PutDataMapRequest;
import com.google.android.gms.wearable.PutDataRequest;
import com.google.android.gms.wearable.Wearable;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

/**
 * Created by tbeltramelli on 05/08/15.
 */
public class DataManager implements ISensorDataSender {

    private static DataManager _instance = null;

    private GoogleApiClient _client;
    private ExecutorService _threadPool;

    private DataManager(Context context)
    {
        _client = new GoogleApiClient.Builder(context).addApi(Wearable.API).build();
        _threadPool = Executors.newCachedThreadPool();
    }

    public static DataManager getInstance(Context context)
    {
        if (_instance == null)
        {
            _instance = new DataManager(context);
        }

        return _instance;
    }

    private boolean _isConnected()
    {
        if (_client.isConnected()) return true;

        ConnectionResult result = _client.blockingConnect();
        return result.isSuccess();
    }

    @Override
    public void sendSensorData(final int sensorType, final int accuracy, final long timestamp, final float[] values)
    {
        _threadPool.submit(new Runnable() {
            @Override
            public void run() {
                PutDataMapRequest dataMap = PutDataMapRequest.create("sensor_" + sensorType);
                dataMap.getDataMap().putLong("timestamp", timestamp);
                dataMap.getDataMap().putFloatArray("values", values);

                PutDataRequest putDataRequest = dataMap.asPutDataRequest();

                _sendSensorDataInBackground(putDataRequest);
            }
        });
    }

    private void _sendSensorDataInBackground(PutDataRequest data)
    {
        if (!_isConnected()) return;

        Wearable.DataApi.putDataItem(_client, data).setResultCallback(new ResultCallback<DataApi.DataItemResult>() {
            @Override
            public void onResult(DataApi.DataItemResult dataItemResult) {
                Log.wtf(this.getClass().getName(), "Sending sensor data: " + dataItemResult.getStatus().isSuccess());
            }
        });
    }

    public void kill()
    {
        if(_threadPool != null) _threadPool.shutdownNow();
        if(_client != null) _client.disconnect();
    }
}
