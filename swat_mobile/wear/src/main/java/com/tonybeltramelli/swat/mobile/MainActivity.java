package com.tonybeltramelli.swat.mobile;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.support.wearable.view.WatchViewStub;
import android.widget.TextView;

public class MainActivity extends Activity {

    private TextView _textView;
    private SensorDataSender _sender;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        final WatchViewStub stub = (WatchViewStub) findViewById(R.id.watch_view_stub);
        stub.setOnLayoutInflatedListener(new WatchViewStub.OnLayoutInflatedListener() {
            @Override
            public void onLayoutInflated(WatchViewStub stub) {
                _textView = (TextView) stub.findViewById(R.id.text);
            }
        });

        _sender = SensorDataSender.getInstance(getApplicationContext());

        startService(new Intent(this, MotionSensorService.class));
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();

        _sender.kill();
    }
}
