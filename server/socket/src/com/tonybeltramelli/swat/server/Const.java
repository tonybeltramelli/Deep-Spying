package com.tonybeltramelli.swat.server;

/**
 * @author Tony Beltramelli www.tonybeltramelli.com - created 23/07/15
 */
public class Const
{
    public static final int TCP_SOCKET_SERVER_PORT = 25500;
    public static final int HTTP_SERVER_PORT = 8000;
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
    public static final String START_SIGNAL = "/start/";
    public static final String END_SIGNAL = "/end/";
    //
    public static final String DATA_OUT_PATH = "data/" + SESSION_ID + "_" + SENSOR_NAME + ".csv";
    public static final String CSV_HEADER = Const.TIMESTAMP+","+ Const.X+","+ Const.Y+","+ Const.Z;
}
