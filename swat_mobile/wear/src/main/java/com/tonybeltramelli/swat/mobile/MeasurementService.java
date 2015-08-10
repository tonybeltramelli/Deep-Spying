package com.tonybeltramelli.swat.mobile;

import android.content.Intent;
import android.util.Log;

import com.google.android.gms.wearable.MessageEvent;
import com.google.android.gms.wearable.WearableListenerService;

/**
 * Created by tbeltramelli on 05/08/15.
 */
public class MeasurementService extends WearableListenerService {

    @Override
    public void onCreate() {
        super.onCreate();

        Log.wtf(this.getClass().getName(), "------> here");

        startService(new Intent(this, MotionSensorService.class));
    }

    @Override
    public void onDestroy() {
        super.onDestroy();

        stopService(new Intent(this, MotionSensorService.class));
    }

    @Override
    public void onMessageReceived(MessageEvent messageEvent) {
        Log.d(this.getClass().getName(), "Received message: " + messageEvent.getPath());

        //startService(new Intent(this, MotionSensorService.class));
        //stopService(new Intent(this, MotionSensorService.class));
    }
}
