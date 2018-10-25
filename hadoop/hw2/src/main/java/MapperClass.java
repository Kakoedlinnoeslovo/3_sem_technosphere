

import java.io.IOException;
import java.util.StringTokenizer;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

import org.apache.hadoop.util.Tool;
import org.apache.hadoop.conf.Configured;
import java.util.LinkedList;
import  java.util.logging.Logger;

public class MapperClass extends Mapper <LongWritable, Text, Text, IntWritable>
{
    private static Logger log = Logger.getLogger(MapperClass.class.getName());

    private final static IntWritable one = new IntWritable(1);
    private Text word = new Text();

    @Override
    protected void map(LongWritable offset, Text data, Context context)
        throws  IOException, InterruptedException
    {
        String line = data.toString();
        System.out.println(line);
        String[] idContent = line.split("\t");
        int id = Integer.valueOf(idContent[0]);
        String content = idContent[1];
        System.out.println(content);

    }
}

