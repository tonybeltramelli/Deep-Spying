package com.tonybeltramelli.swat.server.network;

import com.sun.net.httpserver.Headers;
import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpServer;
import com.tonybeltramelli.swat.server.Const;
import com.tonybeltramelli.swat.server.data.DataStore;
import com.tonybeltramelli.swat.server.data.LabelDataPoint;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.util.Date;
import java.util.concurrent.Executors;

/**
 * @author Tony Beltramelli www.tonybeltramelli.com - created 05/09/15
 */
public class HTTPServer extends Thread implements IServer, HttpHandler
{
    private HttpServer _listener;
    private DataStore _dataStore;

    public HTTPServer(int port, DataStore dataStore) throws IOException
    {
        _dataStore = dataStore;

        _listener = HttpServer.create(new InetSocketAddress(port), 0);

        System.out.println("Start HTTP Server on port " + port);
    }

    @Override
    public void run()
    {
        try
        {
            listen();
        } catch(IOException e)
        {
            e.printStackTrace();
        }
    }

    @Override
    public void listen() throws IOException
    {
        _listener.createContext("/", this);
        _listener.setExecutor(Executors.newCachedThreadPool());
        _listener.start();
    }

    @Override
    public void handle(HttpExchange httpExchange) throws IOException
    {
        BufferedReader input = new BufferedReader(new InputStreamReader(httpExchange.getRequestBody()));
        String data = input.readLine();

        System.out.println(Const.getDataSnapshot(data));

        try {
            if(data.length() > 1) _dataStore.store(data, LabelDataPoint.class);
        } catch(Exception e) {
            e.printStackTrace();
        }

        Headers responseHeaders = httpExchange.getResponseHeaders();
        responseHeaders.set("Access-Control-Allow-Origin", "*");
        responseHeaders.set("Content-Type", "text/plain");

        String response = "#" + String.valueOf(new Date().getTime()) + "#";
        httpExchange.sendResponseHeaders(200, response.length());
        OutputStream responseBody = httpExchange.getResponseBody();
        responseBody.write(response.getBytes());
        responseBody.close();
    }

    @Override
    public void close() throws IOException
    {
        _listener.stop(0);
    }
}
