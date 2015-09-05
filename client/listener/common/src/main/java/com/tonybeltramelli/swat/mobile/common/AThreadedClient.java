package com.tonybeltramelli.swat.mobile.common;

import android.content.Context;

import com.google.android.gms.common.ConnectionResult;
import com.google.android.gms.common.api.GoogleApiClient;
import com.google.android.gms.wearable.Wearable;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

/**
 * Created by Tony Beltramelli www.tonybeltramelli.com on 11/08/15.
 */
public class AThreadedClient
{
    protected GoogleApiClient _client;
    protected ExecutorService _threadPool;

    protected AThreadedClient(Context context)
    {
        _client = new GoogleApiClient.Builder(context).addApi(Wearable.API).build();
        _threadPool = Executors.newCachedThreadPool();
    }

    public boolean connect()
    {
        ConnectionResult result = _client.blockingConnect();
        return result.isSuccess();
    }

    public boolean isConnected()
    {
        if (_client.isConnected()) return true;

        return connect();
    }

    public void kill()
    {
        if (_threadPool != null) _threadPool.shutdownNow();
        if (_client != null) _client.disconnect();
    }
}
