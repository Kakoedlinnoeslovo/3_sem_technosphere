import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Partitioner;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.util.ToolRunner;

import java.net.URL;
import java.io.IOException;



public class SeoSortJob extends Configured implements Tool {

    public static int getMinClicks(Configuration conf)
    {
        return conf.getInt("seo.minclicks", 1);
    }

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


    public static class SeoSortJobMapper extends Mapper<LongWritable, Text, TextTextPair, Text>
    {

        @Override
        protected void map(LongWritable id, Text value, Context context)
                throws IOException, InterruptedException
        {

            String[] line = value.toString().split("\t");

            if (line.length != 2){
                throw  new RuntimeException("Invalid line" + line[0]);
            }

            String host;

            try{
                host = new URL(line[1]).getHost();
            } catch (IOException e){
                host = line[1];
            }

            String query = line[0];

            TextTextPair pair = new TextTextPair(host, query);

            context.write(pair, new Text(query));

        }
    }

    public static class SeoSortJobPartitioner extends Partitioner <TextTextPair, Text>
    {
        @Override
        public int getPartition(TextTextPair key, Text val, int numPartitions)
        {
            return Math.abs(key.getFirst().hashCode()) % numPartitions;
        }

    }



    public static class SeoSortJobKeyComporator extends WritableComparator
    {

        protected SeoSortJobKeyComporator()
        {
            super(TextTextPair.class, true);
        }

        @Override
        public int compare(WritableComparable a, WritableComparable b)
        {
            return ((TextTextPair)a).compareTo((TextTextPair)b);
        }
    }


    public static class SeoSortJobGrouper extends WritableComparator
    {
        protected SeoSortJobGrouper()
        {
            super(TextTextPair.class, true);
        }

        @Override
        public int compare(WritableComparable a, WritableComparable b)
        {
            Text a_first = ((TextTextPair)a).getFirst();
            Text b_first = ((TextTextPair)b).getFirst();

            return a_first.compareTo(b_first);
        }
    }


    public static class SeoSortJobReducer extends Reducer <TextTextPair, Text, Text, Text>
    {
        @Override
        protected void reduce(TextTextPair key, Iterable<Text> values, Context context)
                throws IOException, InterruptedException
        {

            String host = key.getFirst().toString();
            Configuration conf = context.getConfiguration();
            int minClicks = getMinClicks(conf);

            System.out.println("MINCLICKS = " + minClicks);


            String prevQuery = "";
            int counter = 0;
            int counterBest = minClicks;
            String bestQuery = "";

            for (Text t: values)
            {
                String tempQuery = t.toString();

                if (! tempQuery.equals(prevQuery)){
                    prevQuery = tempQuery;
                    counter = 0;
                }

                counter+=1;

                if (counter > counterBest){
                    bestQuery = tempQuery;
                    counterBest = counter;

                }

            }

            if (counterBest > minClicks)
            {

                TextTextPair pair = new TextTextPair(host, bestQuery);
                System.out.println("HERE IS RESULT " + pair.toString() + new Text(Integer.toString(counterBest)));
                context.write(new Text(pair.toString()), new Text(Integer.toString(counterBest)));
            }

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

        job.setMapOutputKeyClass(TextTextPair.class);
        job.setMapOutputValueClass(Text.class);

        job.setOutputValueClass(Text.class);
        job.setOutputKeyClass(Text.class);

        job.setPartitionerClass(SeoSortJobPartitioner.class);
        job.setSortComparatorClass(SeoSortJobKeyComporator.class);
        job.setGroupingComparatorClass(SeoSortJobGrouper.class);



        return job;
    }





}
