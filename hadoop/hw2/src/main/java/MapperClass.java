

import java.io.IOException;
import java.util.StringTokenizer;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

import org.apache.hadoop.util.Tool;
import org.apache.hadoop.conf.Configured;
import java.util.LinkedList;


public class MapperClass extends Mapper <LongWritable, Text, Text, IntWritable>
{

    private final static IntWritable one = new IntWritable(1);
    private Text word = new Text();

    @Override
    protected void map(LongWritable key, Text value, Context context)
        throws  IOException, InterruptedException{
        String line = value.toString();
        StringTokenizer st = new StringTokenizer(line, " ");

        while (st.hasMoreTokens()){
            word.set(st.nextToken());
            context.write(word, one);
        }
    }
}

