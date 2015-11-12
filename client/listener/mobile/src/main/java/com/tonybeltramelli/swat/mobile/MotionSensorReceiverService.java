package com.tonybeltramelli.swat.mobile;

import android.net.Uri;
import android.widget.Toast;

import com.google.android.gms.wearable.Channel;
import com.google.android.gms.wearable.DataEvent;
import com.google.android.gms.wearable.DataEventBuffer;
import com.google.android.gms.wearable.DataItem;
import com.google.android.gms.wearable.DataMap;
import com.google.android.gms.wearable.DataMapItem;
import com.google.android.gms.wearable.Node;
import com.google.android.gms.wearable.WearableListenerService;
import com.tonybeltramelli.swat.mobile.common.Const;
import com.tonybeltramelli.swat.mobile.common.Out;
import com.tonybeltramelli.swat.mobile.data.DataManager;

/**
 * Created by Tony Beltramelli www.tonybeltramelli.com on 11/08/15.
 * Adapted from https://github.com/pocmo/SensorDashboard
 */
public class MotionSensorReceiverService extends WearableListenerService
{
    private Toast _toast;

    @Override
    public void onCreate()
    {
        super.onCreate();

        _toast = Toast.makeText(getApplicationContext(), getResources().getString(R.string.receiving_data_message), Toast.LENGTH_SHORT);
    }

    @Override
    public void onPeerDisconnected(Node peer) {
        Out.print("onPeerDisconnected");
    }

    @Override
    public void onChannelClosed(Channel channel, int closeReason, int appSpecificErrorCode) {
        Out.print("onChannelClosed");
    }

    @Override
    public void onInputClosed(Channel channel, int closeReason, int appSpecificErrorCode) {
        Out.print("onInputClosed");
    }

    @Override
    public void onOutputClosed(Channel channel, int closeReason, int appSpecificErrorCode) {
        Out.print("onOutputClosed");
    }

    @Override
    public void onDataChanged(DataEventBuffer dataEvents)
    {
        super.onDataChanged(dataEvents);

        for (DataEvent dataEvent : dataEvents)
        {
            if (dataEvent.getType() != DataEvent.TYPE_CHANGED) continue;

            DataItem dataItem = dataEvent.getDataItem();
            Uri uri = dataItem.getUri();
            String path = uri.getPath();

            if (path.startsWith(Const.SENSOR_ROOT))
            {
                _toast.show();

                int sensorType = Integer.parseInt(uri.getLastPathSegment());
                DataMap dataMap = DataMapItem.fromDataItem(dataItem).getDataMap();

                long timestamp = dataMap.getLong(Const.TIMESTAMP);
                float[] values = dataMap.getFloatArray(Const.VALUES);

                DataManager.getInstance().storeSensorData(sensorType, timestamp, values);
            } else if (path.startsWith(Const.END_SESSION))
            {
                DataManager.getInstance().flush();
            }
        }
    }
}
