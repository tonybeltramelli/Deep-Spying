package com.tonybeltramelli.swat.server;

/**
 * @author Tony Beltramelli www.tonybeltramelli.com - created 23/07/15
 */
public class Config
{
    public static final int SERVER_PORT = 25500;
    //
    public static final String TIMESTAMP = "timestamp";
    public static final String X = "x";
    public static final String Y = "y";
    public static final String Z = "z";
    public static final String SENSOR_NAME = "sensor_name";
    public static final String DATA_POINTS = "data_points";
    public static final String SESSION_ID = "session_ID";
    //
    public static final String DATA_OUT_PATH = "data/" + SESSION_ID + "_" + SENSOR_NAME + ".csv";
}
