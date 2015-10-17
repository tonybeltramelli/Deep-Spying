package com.tonybeltramelli.swat.mobile;

import android.os.Bundle;
import android.view.View;
import android.widget.Button;

import com.tonybeltramelli.swat.mobile.data.DataManager;
import com.tonybeltramelli.swat.mobile.preference.APrefActivity;

/**
 * Created by Tony Beltramelli www.tonybeltramelli.com on 05/08/15.
 */
public class MainActivity extends APrefActivity implements View.OnClickListener
{
    private MeasurementController _measurementController;

    @Override
    protected void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        DataManager.getInstance().setContext(this);

        Button button = (Button) findViewById(R.id.recording_button);
        button.setOnClickListener(this);

        _measurementController = new MeasurementController(this);
    }

    @Override
    public void onClick(View v)
    {
        Button target = (Button) v;

        if (!_measurementController.isRecording)
        {
            DataManager.getInstance().startSession();
            _measurementController.startRecording();
            target.setText(getResources().getString(R.string.stop_recording_button));
        } else
        {
            _measurementController.stopRecording();
            target.setText(getResources().getString(R.string.start_recording_button));
        }
    }

    @Override
    protected void onDestroy()
    {
        super.onDestroy();

        _measurementController.kill();
    }
}
