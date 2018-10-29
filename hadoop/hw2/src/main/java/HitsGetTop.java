import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.util.ToolRunner;

import java.io.IOException;

public class HitsGetTop extends Configured implements Tool {


    static public class HitsgetTopMapper extends Mapper <LongWritable, Text, Text, Text>{
        @Override
        public final void map(LongWritable offset, Text data, Context context) throws IOException{

            

        }


    }

    static public class HitsgetTopReducer extends Reducer <Text, Text, Text, Text>{
        @Override
        public final void reduce(Text url, Iterable<Text> data, Context context){

        }

    }



    private static Job GetJobConf(Configuration conf) throws IOException {
        Job job = Job.getInstance(conf);
        job.setJarByClass(HitsGetTop.class);
        job.setJobName(HitsGetTop.class.getCanonicalName());

        Path inputPath = Constants.HitsOutputPath;
        Path outputPath = Constants.HitsGetTopOutputPath;

        job.setMapperClass(HitsgetTopMapper.class);
        job.setReducerClass(HitsgetTopReducer.class);

        FileInputFormat.addInputPath(job, inputPath);
        FileOutputFormat.setOutputPath(job, outputPath);

        job.setMapOutputKeyClass(Text.class);
        job.setMapOutputValueClass(Text.class);

        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(Text.class);

        return job;
    }

    @Override
    public int run(String[] args) throws Exception{
        Job job = GetJobConf(getConf());
        return job.waitForCompletion(true) ? 0 : 1;
    }

    void main (String[] args) throws  Exception{
        int exitCode = ToolRunner.run(new HitsGetTop(), args);
        System.exit(exitCode);
    }
}
