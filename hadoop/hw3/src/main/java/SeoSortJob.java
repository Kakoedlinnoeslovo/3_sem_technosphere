import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.WritableComparable;
import org.apache.hadoop.io.WritableComparator;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Partitioner;
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
        protected void map(LongWritable id, Text value, Context context)
                throws IOException, InterruptedException
        {

            String[] line = value.toString().split("\t");

            //System.out.println("QUERY: " + line[0] + " URL: " + line[1]);

            TextIntPair pair = new TextIntPair(line[1], 1);
            Text query = new Text(line[0]);
            //в контакте vk.com
            context.write(pair, query);

        }
    }

    public static class SeoSortJobPartitioner extends Partitioner <TextIntPair, Text>
    {
        @Override
        public int getPartition(TextIntPair key, Text val, int numPartitions)
        {
            return Math.abs(key.getSecond().hashCode()) % numPartitions;
        }

    }



    public static class SeoSortJobKeyComporator extends WritableComparator
    {

        protected SeoSortJobKeyComporator()
        {
            super(TextIntPair.class, true);
        }

        @Override
        public int compare(WritableComparable a, WritableComparable b)
        {
            return ((TextIntPair)a).compareTo((TextIntPair)b);
        }
    }


    public static class SeoSortJobGrouper extends WritableComparator
    {
        protected SeoSortJobGrouper()
        {
            super(TextIntPair.class, true);
        }

        @Override
        public int compare(WritableComparable a, WritableComparable b)
        {
            Text a_first = ((TextIntPair)a).getFirst();
            Text b_first = ((TextIntPair)b).getFirst();

            //group is text part of key
            return a_first.compareTo(b_first);
        }
    }


    public static class SeoSortJobReducer extends Reducer <TextIntPair, Text, Text, Text>
    {
        @Override
        protected void reduce(TextIntPair key, Iterable<Text> values, Context context)
                throws IOException, InterruptedException
        {
            String query = values.iterator().next().toString();
            String url = key.getFirst().toString();
            int number = key.getSecond().get();

            System.out.println("CURRENT QUN IN REDUCER" + query + url + number);

            String numberStr = String.format("%d", number);


            context.write(new Text(query), new Text(url + " " + numberStr));
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

        job.setPartitionerClass(SeoSortJobPartitioner.class);
        job.setSortComparatorClass(SeoSortJobKeyComporator.class);
        job.setGroupingComparatorClass(SeoSortJobGrouper.class);



        return job;
    }





}
