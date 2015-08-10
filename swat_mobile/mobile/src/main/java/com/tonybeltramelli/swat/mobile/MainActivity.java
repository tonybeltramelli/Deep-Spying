package com.tonybeltramelli.swat.mobile;

import android.support.v7.app.ActionBarActivity;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;

public class MainActivity extends ActionBarActivity implements View.OnClickListener {

    private SensorDataReceiver _receiver;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        Button button = (Button) findViewById(R.id.recording_button);
        button.setOnClickListener(this);

        _receiver = SensorDataReceiver.getInstance(this);
    }

    @Override
    public void onClick(View v)
    {
        Button target = (Button) v;

        if (!_receiver.isRecording)
        {
            _receiver.startRecording();
            target.setText(getResources().getString(R.string.stop_recording_button));
        }else{
            _receiver.stopRecording();
            target.setText(getResources().getString(R.string.start_recording_button));
        }
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        getMenuInflater().inflate(R.menu.menu_main, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        int id = item.getItemId();

        if (id == R.id.action_settings) {
            return true;
        }

        return super.onOptionsItemSelected(item);
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();

        _receiver.kill();
    }
}
