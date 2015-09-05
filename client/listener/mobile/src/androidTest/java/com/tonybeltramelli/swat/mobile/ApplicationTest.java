package com.tonybeltramelli.swat.mobile;

import android.app.Application;
import android.test.ApplicationTestCase;

import com.tonybeltramelli.swat.mobile.common.Const;
import com.tonybeltramelli.swat.mobile.data.DataPoint;
import com.tonybeltramelli.swat.mobile.data.DataStore;

import org.json.JSONException;

/**
 * <a href="http://d.android.com/tools/testing/testing_android.html">Testing Fundamentals</a>
 */
public class ApplicationTest extends ApplicationTestCase<Application> {
    public ApplicationTest() {
        super(Application.class);
    }
}