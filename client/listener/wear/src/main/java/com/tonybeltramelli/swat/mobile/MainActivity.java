package com.tonybeltramelli.swat.mobile;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.support.wearable.view.WatchViewStub;
import android.widget.TextView;

/**
 * Created by Tony Beltramelli www.tonybeltramelli.com on 05/08/15.
 */
public class MainActivity extends Activity
{
    private TextView _textView;

    @Override
    protected void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        final WatchViewStub stub = (WatchViewStub) findViewById(R.id.watch_view_stub);
        stub.setOnLayoutInflatedListener(new WatchViewStub.OnLayoutInflatedListener()
        {
            @Override
            public void onLayoutInflated(WatchViewStub stub)
            {
                _textView = (TextView) stub.findViewById(R.id.text);
            }
        });

        startService(new Intent(this, MainService.class));
        finish();
    }
}
