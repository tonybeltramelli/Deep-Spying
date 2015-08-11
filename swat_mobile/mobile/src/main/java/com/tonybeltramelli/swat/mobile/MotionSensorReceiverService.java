package com.tonybeltramelli.swat.mobile;

import android.net.Uri;
import android.widget.Toast;

import com.google.android.gms.wearable.DataEvent;
import com.google.android.gms.wearable.DataEventBuffer;
import com.google.android.gms.wearable.DataItem;
import com.google.android.gms.wearable.DataMap;
import com.google.android.gms.wearable.DataMapItem;
import com.google.android.gms.wearable.Node;
import com.google.android.gms.wearable.WearableListenerService;
import com.tonybeltramelli.swat.mobile.common.Const;

/**
 * Created by tbeltramelli on 11/08/15.
 */
public class MotionSensorReceiverService extends WearableListenerService
{
    @Override
    public void onDataChanged(DataEventBuffer dataEvents)
    {
        super.onDataChanged(dataEvents);

        Toast.makeText(getApplicationContext(), "Receive data", Toast.LENGTH_SHORT).show();

        for (DataEvent dataEvent : dataEvents)
        {
            if (dataEvent.getType() != DataEvent.TYPE_CHANGED) continue;

            DataItem dataItem = dataEvent.getDataItem();
            Uri uri = dataItem.getUri();
            String path = uri.getPath();

            if (path.startsWith(Const.SENSOR_ROOT)) continue;

            int sensorType = Integer.parseInt(uri.getLastPathSegment());
            DataMap dataMap = DataMapItem.fromDataItem(dataItem).getDataMap();

            long timestamp = dataMap.getLong(Const.TIMESTAMP);
            float[] values = dataMap.getFloatArray(Const.VALUES);

            DataManager.getInstance().storeSensorData(sensorType, timestamp, values);
        }
    }
}
