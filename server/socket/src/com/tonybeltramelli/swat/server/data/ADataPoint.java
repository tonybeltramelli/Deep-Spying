package com.tonybeltramelli.swat.server.data;

/**
 * @author Tony Beltramelli www.tonybeltramelli.com - created 06/09/15
 */
public abstract class ADataPoint implements Comparable<ADataPoint>
{
    protected long _timestamp;

    public String getCSVLine()
    {
        return String.valueOf(_timestamp);
    }

    public long getTimestamp()
    {
        return _timestamp;
    }

    @Override
    public int compareTo(ADataPoint dataPoint)
    {
        long timestamp = dataPoint.getTimestamp();

        return (_timestamp > timestamp) ? 1 : -1;
    }
}
