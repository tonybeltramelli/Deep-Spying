package com.tonybeltramelli.swat.mobile;

import android.content.Intent;
import android.util.Log;

import com.google.android.gms.wearable.MessageEvent;
import com.google.android.gms.wearable.WearableListenerService;
import com.tonybeltramelli.swat.mobile.common.Const;

/**
 * Created by tbeltramelli on 05/08/15.
 */
public class MainService extends WearableListenerService
{
    @Override
    public void onCreate()
    {
        super.onCreate();

        Log.d(this.getClass().getName(), "------> here");
    }

    @Override
    public void onMessageReceived(MessageEvent messageEvent)
    {
        Log.d(this.getClass().getName(), "Received message: " + messageEvent.getPath());

        switch (messageEvent.getPath())
        {
            case Const.START_RECORDING:
                Log.d(this.getClass().getName(), "Start recording");
                startService(new Intent(this, MotionSensorService.class));
                break;
            case Const.STOP_RECORDING:
                Log.d(this.getClass().getName(), "Stop recording");
                stopService(new Intent(this, MotionSensorService.class));
                break;
            default:
                break;
        }
    }

    @Override
    public void onDestroy()
    {
        super.onDestroy();

        stopService(new Intent(this, MotionSensorService.class));
    }
}
