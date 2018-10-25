import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.util.ToolRunner;


import javax.xml.soap.Text;
import java.io.IOException;

public class RunJob extends Configured implements Tool {
    public int run (String[] args) throws Exception{
        Job job = GetJobConf(getConf(), args[0], args[1]);
        return job.waitForCompletion(true) ? 0 : 1;
    }

    private static Job GetJobConf(Configuration conf, String input, String output)
            throws IOException{
        Job job = Job.getInstance(conf);
        job.setJarByClass(RunJob.class);
        job.setJobName(RunJob.class.getCanonicalName());

        FileInputFormat.setInputPaths(job, new Path(input));
        FileOutputFormat.setOutputPath(job, new Path(output));

        job.setMapperClass(MapperClass.class);
        job.setReducerClass(ReducerClass.class);

        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(IntWritable.class);

        return job;
    }

    public static void main(String[] args) throws Exception {
        int exitCode = ToolRunner.run(new RunJob(), args);
        System.exit(exitCode);
    }

}