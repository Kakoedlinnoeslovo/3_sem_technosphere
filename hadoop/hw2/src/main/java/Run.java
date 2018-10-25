import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.io.IntWritable;

import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.lib.input.MultipleInputs;
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.util.ToolRunner;
import org.apache.hadoop.mapred.JobConf;
import org.apache.hadoop.io.Text;
import java.io.IOException;

public class Run extends Configured implements Tool {
    public int run (String[] args) throws Exception{
        Job job = GetJobConf(getConf(), args[0], args[1]);
        return job.waitForCompletion(true) ? 0 : 1;
    }

    private static Job GetJobConf(Configuration conf, String input, String output)
            throws IOException{
        Job job = Job.getInstance(conf);
        job.setJarByClass(Run.class);
        job.setJobName(Run.class.getCanonicalName());

        Path inputPath = new Path(input);

        MultipleInputs.addInputPath(job, inputPath,
                TextInputFormat.class, MapperClass.class);

        FileOutputFormat.setOutputPath(job, new Path(output));

        job.setMapperClass(MapperClass.class);
        //job.setReducerClass(ReducerClass.class);

        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(IntWritable.class);

        return job;
    }

    public static void main(String[] args) throws Exception {
        int exitCode = ToolRunner.run(new Run(), args);
        System.exit(exitCode);
    }

}
