package com.tonybeltramelli.swat.mobile.data;

import android.app.Activity;
import android.hardware.Sensor;
import android.preference.PreferenceManager;

import com.tonybeltramelli.swat.mobile.R;
import com.tonybeltramelli.swat.mobile.SocketClient;
import com.tonybeltramelli.swat.mobile.common.Const;
import com.tonybeltramelli.swat.mobile.common.Out;

import org.json.JSONException;

import java.security.SecureRandom;
import java.util.Date;
import java.util.Map;

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
    private int _sessionID;

    private DataManager()
    {
        _dataStore = new DataStore();
        _socketClient = new SocketClient();

        _sessionID = _generateSessionID();
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
                String jsonString = _dataStore.getJSONString(_sessionID, sensorName);
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

            String jsonStrings[] = _dataStore.getJSONStrings(_sessionID);
            for (String jsonString: jsonStrings)
            {
                _socketClient.send(_serverAddress, _serverPort, jsonString);
            }

            _dataStore.clear();
        } catch (JSONException e)
        {
            Out.report(e.getMessage());
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

    private int _generateSessionID()
    {
        SecureRandom random = new SecureRandom();
        random.setSeed(new Date().getTime());

        return (int) Math.pow(8, 8) + random.nextInt(99999999 - (int) Math.pow(8, 8));
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
