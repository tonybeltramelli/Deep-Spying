package com.tonybeltramelli.swat.server.data;

import com.tonybeltramelli.swat.server.Const;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.util.Collections;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.Map;

/**
 * @author Tony Beltramelli www.tonybeltramelli.com - created 28/08/15
 */
public class DataStore
{
    private HashMap<String, LinkedList<DataPoint>> _data;

    public DataStore()
    {
        _init();
    }

    private void _init()
    {
        if(_data != null)
        {
            for (Map.Entry<String, LinkedList<DataPoint>> entry: _data.entrySet())
            {
                String key = entry.getKey();
                _data.get(key).clear();
            }
        }

        _data = null;
        _data = new HashMap<String, LinkedList<DataPoint>>();
    }

    public void push(String filePath, DataPoint dataPoint)
    {
        if (!_data.containsKey(filePath))
        {
            _data.put(filePath, new LinkedList<DataPoint>());
        }

        _data.get(filePath).addLast(dataPoint);
    }

    public void save() throws Exception
    {
        for (Map.Entry<String, LinkedList<DataPoint>> entry: _data.entrySet())
        {
            String filePath = entry.getKey();
            LinkedList<DataPoint> dataPoints = entry.getValue();
            Collections.sort(dataPoints);

            File file = new File(filePath);

            boolean isCreated = false;
            if(!file.exists())
            {
                file.createNewFile();
                isCreated = true;
            }

            FileWriter fileWriter = new FileWriter(file.getAbsoluteFile(), true);
            BufferedWriter bufferedWriter = new BufferedWriter(fileWriter);

            if(isCreated)
            {
                bufferedWriter.write(Const.CSV_HEADER);
                bufferedWriter.newLine();
            }

            for(DataPoint dataPoint: dataPoints)
            {
                bufferedWriter.write(dataPoint.getCSVLine());
                bufferedWriter.newLine();
            }

            bufferedWriter.close();
            fileWriter.close();
        }

        _init();
    }

    public String getSizeReport()
    {
        String size = _data.size() + "( ";
        for (Map.Entry<String, LinkedList<DataPoint>> entry: _data.entrySet())
        {
            size += "[ "+entry.getKey() + " : " + entry.getValue().size() + " ] ";
        }
        size += ")";
        return size;
    }

    @Override
    public String toString()
    {
        String string = super.toString() + "\n";

        for (Map.Entry<String, LinkedList<DataPoint>> entry: _data.entrySet())
        {
            String key = entry.getKey();
            LinkedList<DataPoint> value = entry.getValue();

            string += key + "[\n";

            for (DataPoint dataPoint: value)
            {
                string += " " + dataPoint + "\n";
            }

            string += "]\n";
        }

        return string;
    }
}
