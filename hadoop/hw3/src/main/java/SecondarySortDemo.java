import org.apache.hadoop.io.*;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.util.ToolRunner;

import java.io.IOException;


public class SecondarySortDemo extends Configured implements Tool {

    public static void main(String[] args) throws Exception{
        int rc = ToolRunner.run(new SecondarySortDemo(), args);
        System.exit(rc);
    }

    @Override
    public int run(String[] args)
            throws IOException, InterruptedException, ClassNotFoundException
    {
        Job job = getJobConf(getConf(), args[0], args[1]);
        return job.waitForCompletion(true) ? 0: 1;
    }

    public static class SecondarySortDemoMapper extends Mapper <LongWritable, Text, TextFloatPair, IntWritable>
    {

        GSODRecord gsod = new GSODRecord();
        @Override
        protected  void map(LongWritable key, Text value, Context context)
                throws IOException, InterruptedException
        {
            String line = value.toString();
            gsod.parseFrom(line);

            if (gsod.hasMaxTemp())
            {
                String natural_key = String.format("%d:%02d.%02d",
                        gsod.station, gsod.day, gsod.month);
                TextFloatPair composite = new TextFloatPair(natural_key, gsod.max_temp);

                context.write(composite, new IntWritable(gsod.year));
            }
            else {
                context.getCounter("COMMON_COUNTERS", "SkippedValues").increment(1);
            }
        }

    }

    public static class SecondarySortDemoReducer extends Reducer <TextFloatPair, IntWritable, Text, Text>
    {
        @Override
        protected void reduce(TextFloatPair key, Iterable <IntWritable> values, Context context)
                throws IOException, InterruptedException
        {
            int year = values.iterator().next().get();
            float temp = key.getSecond().get();


            String value = String.format("%.1fC (%d)", temp, year);
            context.write(key.getFirst(), new Text(value));
        }


    }

    public static class KeyComparator extends WritableComparator
    {
        protected KeyComparator()
        {
            super (TextFloatPair.class, true);
        }

        @Override
        public int compare (WritableComparable a, WritableComparable b)
        {
            return ((TextFloatPair)a).compareTo((TextFloatPair)b);
        }
    }

    public static class MDStationGrouper extends WritableComparator
    {

        protected MDStationGrouper(){
            super(TextFloatPair.class, true);
        }

        //считаем за одну группу текстовую часть ключа: {id станци, день, месяц}
        @Override
        public int compare(WritableComparable a, WritableComparable b){
            Text a_first = ((TextFloatPair)a).getFirst();
            Text b_first = ((TextFloatPair)b).getFirst();
            return a_first.compareTo(b_first);
        }
    }


    public static Job getJobConf(Configuration conf, String input, String output) throws IOException{
        Job job = Job.getInstance(conf);

        job.setJarByClass(SecondarySortDemo.class);
        job.setJobName(SecondarySortDemo.class.getCanonicalName());

        FileInputFormat.addInputPath(job, new Path(input));
        FileOutputFormat.setOutputPath(job, new Path(output));


        return job;

    }

}
