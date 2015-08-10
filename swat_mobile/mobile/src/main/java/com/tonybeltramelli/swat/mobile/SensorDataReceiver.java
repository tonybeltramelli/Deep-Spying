package com.tonybeltramelli.swat.mobile;

import android.content.Context;
import android.util.Log;

import com.google.android.gms.common.api.ResultCallback;
import com.google.android.gms.wearable.MessageApi;
import com.google.android.gms.wearable.Node;
import com.google.android.gms.wearable.Wearable;
import com.tonybeltramelli.swat.mobile.common.ADataManager;
import com.tonybeltramelli.swat.mobile.common.Const;

import java.util.List;

/**
 * Created by tbeltramelli on 10/08/15.
 */
public class SensorDataReceiver extends ADataManager {

    private static SensorDataReceiver _instance = null;

    public boolean isRecording = false;

    private SensorDataReceiver(Context context)
    {
        super(context);
    }

    public static SensorDataReceiver getInstance(Context context)
    {
        if (_instance == null)
        {
            _instance = new SensorDataReceiver(context);
        }

        return _instance;
    }

    public void startRecording()
    {
        _threadPool.submit(new Runnable() {
            @Override
            public void run() {
                isRecording = true;
                _controlMeasurementInBackground(Const.START_RECORDING);
            }
        });
    }

    public void stopRecording()
    {
        _threadPool.submit(new Runnable() {
            @Override
            public void run() {
                isRecording = false;
                _controlMeasurementInBackground(Const.STOP_RECORDING);
            }
        });
    }

    private void _controlMeasurementInBackground(final String path) {
        if (!_isConnected()) return;

        List<Node> nodes = Wearable.NodeApi.getConnectedNodes(_client).await().getNodes();

        Log.wtf(this.getClass().getName(), "-----> " + nodes.size() + " connected");

        for (Node node : nodes) {
            Wearable.MessageApi.sendMessage(_client, node.getId(), path, null).setResultCallback(new ResultCallback<MessageApi.SendMessageResult>() {
                @Override
                public void onResult(MessageApi.SendMessageResult sendMessageResult) {
                    Log.wtf(this.getClass().getName(), "controlMeasurementInBackground(" + path + "): " + sendMessageResult.getStatus().isSuccess());
                }
            });
        }
    }
}
