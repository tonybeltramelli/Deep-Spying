package com.tonybeltramelli.swat.mobile.preference;

import android.os.Bundle;
import android.preference.PreferenceActivity;

/**
 * Created by Tony Beltramelli www.tonybeltramelli.com on 12/08/15.
 */
public class PrefActivity extends PreferenceActivity
{
    @Override
    protected void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);

        getFragmentManager().beginTransaction().replace(android.R.id.content, new PrefFragment()).commit();
    }
}
