package com.tonybeltramelli.swat.server.network;

import java.io.IOException;

/**
 * @author Tony Beltramelli www.tonybeltramelli.com - created 05/09/15
 */
public interface IServer
{
    void listen() throws IOException;
    void close() throws IOException;
}
