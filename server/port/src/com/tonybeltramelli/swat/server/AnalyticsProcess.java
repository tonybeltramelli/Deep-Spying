package com.tonybeltramelli.swat.server;

import java.io.BufferedReader;
import java.io.InputStreamReader;

/**
 * @author Tony Beltramelli www.tonybeltramelli.com - created 12/12/15
 */
public class AnalyticsProcess
{
    public static void run(String sessionName)
    {
        try {
            Process process = Runtime.getRuntime().exec(Const.DATA_ANALYTICS_SCRIPT + " -name "+sessionName);
            BufferedReader stdInput = new BufferedReader(new InputStreamReader(process.getInputStream()));

            String s;
            while ((s = stdInput.readLine()) != null) {
                System.out.println(s);
            }
        } catch(Exception e) {
            e.printStackTrace();
        }
    }
}
