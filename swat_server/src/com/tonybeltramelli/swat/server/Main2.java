package com.tonybeltramelli.swat.server;

import java.io.IOException;

/**
 * @author Tony Beltramelli www.tonybeltramelli.com - created 23/07/15
 */
public class Main2
{

    public static void main(String[] args) throws IOException
    {
        Client client = new Client();

        client.connect();
    }
}
