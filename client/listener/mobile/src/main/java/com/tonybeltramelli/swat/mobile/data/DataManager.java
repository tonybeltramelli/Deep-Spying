package com.tonybeltramelli.swat.mobile.data;

import android.app.Activity;
import android.hardware.Sensor;
import android.os.Handler;
import android.preference.PreferenceManager;

import com.tonybeltramelli.swat.mobile.R;
import com.tonybeltramelli.swat.mobile.socket.SocketClient;
import com.tonybeltramelli.swat.mobile.common.Const;
import com.tonybeltramelli.swat.mobile.common.Out;

import org.json.JSONException;

import java.security.SecureRandom;
import java.util.Date;

/**
 * Created by Tony Beltramelli www.tonybeltramelli.com on 10/08/15.
 */
public class DataManager
{
    private static DataManager _instance = null;

    private DataStore _dataStore;
    private SocketClient _socketClient;

    private String _serverAddress;
    private int _serverPort;
    private Activity _context;

    private DataManager()
    {
        _dataStore = new DataStore();
        _socketClient = new SocketClient();

        startSession();
    }

    public static DataManager getInstance()
    {
        if (_instance == null)
        {
            _instance = new DataManager();
        }

        return _instance;
    }

    public void storeSensorData(final int sensorType, final long timestamp, final float[] values)
    {
        if(values.length < 3) return;

        String sensorName = _getSensorName(sensorType);

        DataPoint dataPoint = new DataPoint(
                sensorName,
                timestamp,
                values[0],
                values[1],
                values[2]
        );

        if(_dataStore.push(sensorName, dataPoint))
        {
            try
            {
                String jsonString = _dataStore.getJSONString(sensorName);
                Out.print("full "+sensorName+" -> "+_dataStore.getSizeReport());
                _socketClient.send(_serverAddress, _serverPort, jsonString);
            } catch (JSONException e)
            {
                Out.report(e.getMessage());
            }
        }
    }

    public void flush()
    {
        try
        {
            Out.print("flush "+_dataStore.getSizeReport());

            String jsonStrings[] = _dataStore.getJSONStrings();
            for (String jsonString: jsonStrings)
            {
                _socketClient.send(_serverAddress, _serverPort, jsonString);
            }
            _dataStore.clear();
        } catch (JSONException e)
        {
            Out.report(e.getMessage());
        } finally
        {
            Handler handler = new Handler();
            handler.postDelayed(new Runnable()
            {
                public void run()
                {
                    _socketClient.send(_serverAddress, _serverPort, Const.END_SESSION, Thread.MIN_PRIORITY);
                }
            }, 1000);
        }
    }

    private String _getSensorName(int sensorType)
    {
        String sensorName;

        switch (sensorType){
            case Sensor.TYPE_ACCELEROMETER:
                sensorName = Const.ACCELEROMETER;
                break;
            case Sensor.TYPE_GYROSCOPE:
                sensorName = Const.GYROSCOPE;
                break;
            default:
                sensorName = Const.UNSUPPORTED;
                break;
        }

        return sensorName;
    }

    public void startSession()
    {
        _socketClient.send(_serverAddress, _serverPort, Const.START_SESSION, Thread.MAX_PRIORITY);
    }

    public void setContext(Activity context)
    {
        _context = context;
        savePreferences();
    }

    public void savePreferences()
    {
        _serverAddress = PreferenceManager.getDefaultSharedPreferences(_context).getString(Const.PREF_KEY_SERVER_ADDRESS, _context.getResources().getString(R.string.default_server_address));
        _serverPort = Integer.parseInt(PreferenceManager.getDefaultSharedPreferences(_context).getString(Const.PREF_KEY_SERVER_PORT, _context.getResources().getString(R.string.default_server_port)));
    }
}
