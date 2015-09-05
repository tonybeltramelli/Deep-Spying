package com.tonybeltramelli.swat.mobile;

import android.content.Context;

import com.google.android.gms.common.api.ResultCallback;
import com.google.android.gms.wearable.MessageApi;
import com.google.android.gms.wearable.Node;
import com.google.android.gms.wearable.Wearable;
import com.tonybeltramelli.swat.mobile.common.AThreadedClient;
import com.tonybeltramelli.swat.mobile.common.Const;
import com.tonybeltramelli.swat.mobile.common.Out;

import java.util.List;

/**
 * Created by Tony Beltramelli www.tonybeltramelli.com on 11/08/15.
 */
public class MeasurementController extends AThreadedClient
{
    public boolean isRecording = false;

    protected MeasurementController(Context context)
    {
        super(context);
    }

    public void startRecording()
    {
        _threadPool.submit(new Runnable()
        {
            @Override
            public void run()
            {
                isRecording = true;
                _controlMeasurementInBackground(Const.START_RECORDING);
            }
        });
    }

    public void stopRecording()
    {
        _threadPool.submit(new Runnable()
        {
            @Override
            public void run()
            {
                isRecording = false;
                _controlMeasurementInBackground(Const.STOP_RECORDING);
            }
        });
    }

    private void _controlMeasurementInBackground(final String path)
    {
        if (!isConnected()) return;

        List<Node> nodes = Wearable.NodeApi.getConnectedNodes(_client).await().getNodes();

        for (Node node : nodes)
        {
            if (node.getId().equalsIgnoreCase("cloud")) continue;

            final String target = node.getDisplayName();

            Wearable.MessageApi.sendMessage(_client, node.getId(), path, null).setResultCallback(new ResultCallback<MessageApi.SendMessageResult>()
            {
                @Override
                public void onResult(MessageApi.SendMessageResult sendMessageResult)
                {
                    Out.print("Send control " + path + " to " + target + ": " + sendMessageResult.getStatus().isSuccess());
                }
            });
        }
    }
}
