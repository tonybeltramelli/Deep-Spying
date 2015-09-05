package com.tonybeltramelli.swat.mobile.preference;

import android.os.Bundle;
import android.preference.Preference;
import android.preference.PreferenceFragment;

import com.tonybeltramelli.swat.mobile.R;
import com.tonybeltramelli.swat.mobile.common.Const;
import com.tonybeltramelli.swat.mobile.data.DataManager;

/**
 * Created by Tony Beltramelli www.tonybeltramelli.com on 12/08/15.
 */
public class PrefFragment extends PreferenceFragment implements Preference.OnPreferenceClickListener, Preference.OnPreferenceChangeListener
{
    @Override
    public void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);

        addPreferencesFromResource(R.xml.preferences);

        findPreference(Const.PREF_KEY_SAVE).setOnPreferenceClickListener(this);
        findPreference(Const.PREF_KEY_SERVER_ADDRESS).setOnPreferenceChangeListener(this);
        findPreference(Const.PREF_KEY_SERVER_PORT).setOnPreferenceChangeListener(this);
    }

    @Override
    public boolean onPreferenceClick(Preference preference)
    {
        DataManager.getInstance().savePreferences();
        return true;
    }

    @Override
    public boolean onPreferenceChange(Preference preference, Object newValue)
    {
        DataManager.getInstance().savePreferences();
        return true;
    }
}
