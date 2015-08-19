package com.tonybeltramelli.swat.mobile;

import android.content.Intent;
import android.widget.Toast;

import com.google.android.gms.wearable.MessageEvent;
import com.google.android.gms.wearable.WearableListenerService;
import com.tonybeltramelli.swat.mobile.common.Const;
import com.tonybeltramelli.swat.mobile.common.Out;

/**
 * Created by Tony Beltramelli www.tonybeltramelli.com on 05/08/15.
 */
public class MainService extends WearableListenerService
{
    @Override
    public void onCreate()
    {
        super.onCreate();
    }

    @Override
    public void onMessageReceived(MessageEvent messageEvent)
    {
        switch (messageEvent.getPath())
        {
            case Const.START_RECORDING:
                Out.print("Start recording motion sensors");
                Toast.makeText(getApplicationContext(), "Start recording motion sensors", Toast.LENGTH_SHORT).show();

                SensorDataSender.getInstance(getApplicationContext()).init();
                startService(new Intent(this, MotionSensorListenerService.class));
                break;
            case Const.STOP_RECORDING:
                Out.print("Stop recording motion sensors");
                Toast.makeText(getApplicationContext(), "Stop recording motion sensors", Toast.LENGTH_SHORT).show();

                stopService(new Intent(this, MotionSensorListenerService.class));
                break;
            default:
                break;
        }
    }

    @Override
    public void onDestroy()
    {
        super.onDestroy();

        stopService(new Intent(this, MotionSensorListenerService.class));
    }
}
