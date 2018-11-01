import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.util.ToolRunner;
import org.apache.hadoop.io.Text;

import java.io.IOException;


public class SeoSortJob extends Configured implements Tool {

    @Override
    public int run(String[] args)
            throws Exception
    {
        Job job = getJobConf(getConf());
        return job.waitForCompletion(true) ? 0: 1;
    }


    public static void main(String[] args)
            throws Exception
    {
        int result = ToolRunner.run(new SeoSortJob(), args);
        System.exit(result);
    }


    public static class SeoSortJobMapper extends Mapper<LongWritable, Text, TextIntPair, Text>
    {

        @Override
        protected void map(LongWritable id, Text value, Context context){

            String[] line = value.toString().split("\t");

            System.out.println("QUERY: " + line[0] + " URL: " + line[1]);
        }
    }


    public static class SeoSortJobReducer extends Reducer <TextIntPair, Text, Text, Text>
    {
        @Override
        protected void reduce(TextIntPair key, Iterable<Text> values, Context context)
        {

        }
    }


    private Job getJobConf(Configuration conf)
            throws IOException
    {
        Job job = Job.getInstance(conf);
        job.setJarByClass(SeoSortJob.class);
        job.setJobName(SeoSortJob.class.getCanonicalName());

        FileInputFormat.addInputPath(job, new Path(Constants.input));
        FileOutputFormat.setOutputPath(job, new Path(Constants.output));



        job.setMapperClass(SeoSortJobMapper.class);
        job.setReducerClass(SeoSortJobReducer.class);

        job.setMapOutputKeyClass(Text.class);
        job.setMapOutputValueClass(Text.class);

        job.setOutputValueClass(Text.class);
        job.setOutputKeyClass(Text.class);

        //job.setPartitionerClass();
        //job.setSortComparatorClass();
        //job.setGroupingComparatorClass();



        return job;
    }





}
