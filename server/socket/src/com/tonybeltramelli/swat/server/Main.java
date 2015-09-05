package com.tonybeltramelli.swat.server;

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
 * @author Tony Beltramelli www.tonybeltramelli.com - created 23/07/15
 */
public class Main {

    public static void main(String[] args) throws IOException
    {
        /*
        Server server = new Server(Const.SERVER_PORT);

        System.out.println(InetAddress.getLocalHost().getHostAddress());

        try {
            while(true)
            {
                server.listen();
            }
        } finally {
            server.close();
        }*/

        HttpServer server = HttpServer.create(new InetSocketAddress(8000), 0);
        server.createContext("/", new MyHandler());
        server.setExecutor(Executors.newCachedThreadPool());
        server.start();
    }

    static class MyHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange t) throws IOException {
            BufferedReader input = new BufferedReader(new InputStreamReader(t.getRequestBody()));
            String data = input.readLine();

            System.out.println("data: " + data);

            String response = "200 (Success)\n";
            t.sendResponseHeaders(200, response.length());
            OutputStream os = t.getResponseBody();
            os.write(response.getBytes());
            os.close();
        }
    }
}
