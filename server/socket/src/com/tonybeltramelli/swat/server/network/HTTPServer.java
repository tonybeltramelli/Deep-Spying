package com.tonybeltramelli.swat.server.network;

import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpServer;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.util.concurrent.Executors;

/**
 * @author Tony Beltramelli www.tonybeltramelli.com - created 05/09/15
 */
public class HTTPServer implements IServer, HttpHandler
{
    private HttpServer _listener;

    public HTTPServer(int port) throws IOException
    {
        _listener = HttpServer.create(new InetSocketAddress(port), 0);
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

        System.out.println("data: " + data);

        String response = "200 (Success)\n";
        httpExchange.sendResponseHeaders(200, response.length());
        OutputStream os = httpExchange.getResponseBody();
        os.write(response.getBytes());
        os.close();
    }

    @Override
    public void close() throws IOException
    {
        _listener.stop(0);
    }
}
