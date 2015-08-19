package com.tonybeltramelli.swat.server;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.io.PrintWriter;
import java.net.InetAddress;
import java.net.Socket;

/**
 * @author Tony Beltramelli www.tonybeltramelli.com - created 23/07/15
 */
public class Client
{
    public void connect(String data) throws IOException
    {
        Socket socket = new Socket(InetAddress.getLocalHost().getHostAddress(), Config.SERVER_PORT);

        System.out.println("connect");

        try
        {
            PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
            out.println(data);
        } finally {
            socket.close();
        }

        System.out.println("send");
    }

    public static void main(String[] args) throws IOException
    {
        Client client = new Client();
        client.connect(getFileContent("data/gyroscope.json"));
    }

    public static String getFileContent(String fileName)
    {
        BufferedReader reader = null;
        String content = "";

        try
        {
            reader = new BufferedReader(new FileReader(fileName));
            String line;

            while ((line = reader.readLine()) != null) {
                content += line + "\n";
            }

            reader.close();
        } catch (IOException e) {
            e.printStackTrace();
        }

        return content;
    }
}
