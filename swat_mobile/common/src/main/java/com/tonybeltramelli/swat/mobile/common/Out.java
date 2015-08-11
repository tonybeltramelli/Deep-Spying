package com.tonybeltramelli.swat.mobile.common;

import android.util.Log;

/**
 * Created by tbeltramelli on 11/08/15.
 */
public class Out
{
    public static void print(String message)
    {
        String caller = new Exception().getStackTrace()[1].getClassName();
        Log.d(caller, message);
    }
}
