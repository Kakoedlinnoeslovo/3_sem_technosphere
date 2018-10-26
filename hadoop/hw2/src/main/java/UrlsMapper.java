

import java.io.IOException;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

import  java.util.logging.Logger;

public class UrlsMapper extends Mapper <LongWritable, Text, Text, IntWritable>
{
    private static Logger log = Logger.getLogger(UrlsMapper.class.getName());

    private final static IntWritable one = new IntWritable(1);
    private Text word = new Text();

    @Override
    protected void map(LongWritable offset, Text data, Context context)
        throws  IOException, InterruptedException
    {
        String line = data.toString();
        String[] idUrl = line.split("\t");
        int id = Integer.valueOf(idUrl[0]);
        String url = idUrl[1];

        context.write(new Text(url), new IntWritable(id));

    }

}

