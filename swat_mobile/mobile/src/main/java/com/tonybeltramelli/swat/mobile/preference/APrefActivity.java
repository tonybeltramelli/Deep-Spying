package com.tonybeltramelli.swat.mobile.preference;

import android.content.Intent;
import android.content.pm.ActivityInfo;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.Menu;
import android.view.MenuItem;

import com.tonybeltramelli.swat.mobile.R;

/**
 * Created by Tony Beltramelli www.tonybeltramelli.com on 12/08/15.
 */
public abstract class APrefActivity extends AppCompatActivity
{
    @Override
    protected void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);

        setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_FULL_SENSOR);
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu)
    {
        getMenuInflater().inflate(R.menu.menu_main, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item)
    {
        int id = item.getItemId();

        if (id == R.id.action_settings)
        {
            _displaySettings();
            return true;
        }

        return super.onOptionsItemSelected(item);
    }

    protected void _displaySettings()
    {
        Intent intent = new Intent(this, PrefActivity.class);
        startActivity(intent);
    }
}
