package com.tonybeltramelli.swat.mobile;

import android.content.Intent;
import android.util.Log;

import com.google.android.gms.wearable.MessageEvent;
import com.google.android.gms.wearable.WearableListenerService;
import com.tonybeltramelli.swat.mobile.common.Const;

/**
 * Created by tbeltramelli on 05/08/15.
 */
public class MeasurementService extends WearableListenerService {

    @Override
    public void onCreate() {
        super.onCreate();

        Log.wtf(this.getClass().getName(), "------> here");
    }

    @Override
    public void onDestroy() {
        super.onDestroy();

        stopService(new Intent(this, MotionSensorService.class));
    }

    @Override
    public void onMessageReceived(MessageEvent messageEvent) {
        Log.d(this.getClass().getName(), "Received message: " + messageEvent.getPath());

        switch (messageEvent.getPath()) {
            case Const.START_RECORDING:
                startService(new Intent(this, MotionSensorService.class));
                break;
            case Const.STOP_RECORDING:
                stopService(new Intent(this, MotionSensorService.class));
                break;
            default:
                break;
        }
    }
}
