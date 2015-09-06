package com.tonybeltramelli.swat.mobile.socket;

import java.util.concurrent.ThreadFactory;

/**
 * Created by Tony Beltramelli www.tonybeltramelli.com on 06/09/15.
 */
public class SocketClientThreadFactory implements ThreadFactory
{
    private int _priority;

    public SocketClientThreadFactory()
    {
        _priority = Thread.NORM_PRIORITY;
    }

    @Override
    public Thread newThread(Runnable runnable)
    {
        Thread thread =  new Thread(runnable);
        thread.setPriority(_priority);
        return thread;
    }

    public void setPriority(int priority)
    {
        _priority = priority;
    }
}
