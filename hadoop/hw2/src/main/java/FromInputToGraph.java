import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.conf.Configuration;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.MultipleInputs;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.fs.Path;

import java.io.IOException;

import org.apache.hadoop.util.Tool;
import org.apache.hadoop.util.ToolRunner;

import java.util.LinkedList;


public class FromInputToGraph extends Configured implements Tool{

    public static class FromInputToGraphMapper
            extends Mapper <LongWritable, Text, IntWritable, Text>{

        @Override
        protected void map(LongWritable offset, Text data, Context context)
            throws  IOException, InterruptedException
        {
            String line = data.toString();
            String[] idContent = line.split("\t");
            int id = Integer.valueOf(idContent[0]);
            String content = idContent[1];

            LinkedList<String> links = getLinks.extract(content);

            StringBuilder sb = new StringBuilder();
            sb.append("LINKS");

            for (String l: links){
                String temp = l + "\t";
                sb.append(temp);
            }

            context.write(new IntWritable(id), new Text(sb.toString()));
        }
    }

    public static class FromInputToGraphUrlsMapper
            extends Mapper <LongWritable, Text, IntWritable, Text>{

        @Override
        protected void map(LongWritable offset, Text text, Context context){
            String line = text.toString();

            System.out.println(line);
        }
    }

    public static class FromInputToGraphReducer
            extends Reducer <IntWritable, Text, Text, Text>{

        @Override
        protected void reduce(IntWritable id, Iterable<Text> values, Context context)
                throws IOException, InterruptedException{

        }


    }

    private static Job GetJobConf(Configuration conf) throws IOException {
        Job job = Job.getInstance(conf);
        job.setJarByClass(FromInputToGraph.class);
        job.setJobName(FromInputToGraph.class.getCanonicalName());

        Path inputPath = Constants.inputPath;
        Path outputPath = Constants.outputPath;
        Path urlsPath = Constants.urlsPath;

        MultipleInputs.addInputPath(job, urlsPath, TextInputFormat.class, FromInputToGraphUrlsMapper.class);
        MultipleInputs.addInputPath(job, inputPath, TextInputFormat.class, FromInputToGraphMapper.class);
        FileOutputFormat.setOutputPath(job, outputPath);

        job.setMapOutputKeyClass(IntWritable.class);
        job.setMapOutputValueClass(Text.class);
        job.setOutputKeyClass(IntWritable.class);
        job.setOutputValueClass(Text.class);

        job.setReducerClass(FromInputToGraphReducer.class);

        return job;

    }

    @Override
    public int run(String[] args) throws Exception{
        Job job = GetJobConf(getConf());
        return job.waitForCompletion(true) ? 0: 1;
    }


    static public void main(String[] args) throws Exception{
        int ret = ToolRunner.run(new FromInputToGraph(), args);
        System.exit(ret);
    }
}
