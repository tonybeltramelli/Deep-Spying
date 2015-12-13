package com.tonybeltramelli.swat.server;

/**
 * @author Tony Beltramelli www.tonybeltramelli.com - created 23/07/15
 */
public class Const
{
    public static final int TCP_SOCKET_SERVER_PORT = 25500;
    public static final int HTTP_SERVER_PORT = 8000;
    //
    public static final String DATA_ANALYTICS_SCRIPT = "./predict.sh";
    //
    public static final String TIMESTAMP = "timestamp";
    public static final String X = "x";
    public static final String Y = "y";
    public static final String Z = "z";
    public static final String LABEL = "label";
    public static final String SENSOR_NAME = "sensor_name";
    public static final String DATA_POINTS = "data_points";
    public static final String SESSION_ID = "session_ID";
    //
    public static final String START_SESSION = "/start_session/";
    public static final String END_SESSION = "/end_session/";
    //
    public static final String DATA_OUT_PATH = "../data/raw/" + SESSION_ID + "_" + SENSOR_NAME + ".csv";
    public static final String CSV_HEADER_SENSOR = Const.TIMESTAMP + "," + Const.X + "," + Const.Y + "," + Const.Z;
    public static final String CSV_HEADER_LABEL = Const.TIMESTAMP + "," + Const.LABEL;
    //
    public static final String getDataSnapshot(String data)
    {
        int length = data.length();
        int max = 50;
        return data.substring(0, length < max ? length : max) + (length < max ? "" : "...");
    }
}
