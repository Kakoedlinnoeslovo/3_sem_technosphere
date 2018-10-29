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
import java.util.LinkedList;

public class HitsGetTop extends Configured implements Tool {

    LinkedList <String> from = new LinkedList<>();
    LinkedList <String> to = new LinkedList<>();
    private static int FIRST_START = 0;

    static public class HitsgetTopMapper extends Mapper <LongWritable, Text, Text, Text>{
        @Override
        public final void map(LongWritable offset, Text data, Context context) throws IOException{

            if (FIRST_START == 1){
                String dataStr = data.toString();
                String[] dataArray = dataStr.split("\t");
                for (String d: dataArray){
                    if (d.substring(0, 2).equals("|F|")){
                        System.out.println("FROM URLS is " + d.substring(2));
                    }
                    if (d.substring(0, 2).equals("|T|")){
                        System.out.println("TO URLS is " + d.substring(2));
                    }
                }
            }

        }


    }

    static public class HitsgetTopReducer extends Reducer <Text, Text, Text, Text>{
        @Override
        public final void reduce(Text url, Iterable<Text> data, Context context){

        }

    }



    private static Job GetJobConf(Configuration conf, String[] args) throws IOException {
        Job job = Job.getInstance(conf);
        job.setJarByClass(HitsGetTop.class);
        job.setJobName(HitsGetTop.class.getCanonicalName());

        Path inputPath = new Path(args[0]);
        if (new Path(args[0]) == Constants.HitsOutputPath){
            FIRST_START = 1;
        }
        else{
            FIRST_START = 0;
        }
        Path outputPath = Constants.HitsGetTopOutputPath;

        job.setMapperClass(HitsgetTopMapper.class);
        //job.setReducerClass(HitsgetTopReducer.class);

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
        Job job = GetJobConf(getConf(), args);
        return job.waitForCompletion(true) ? 0 : 1;
    }

    public static void main (String[] args) throws  Exception{
        int exitCode = ToolRunner.run(new HitsGetTop(), args);
        System.exit(exitCode);
    }
}
