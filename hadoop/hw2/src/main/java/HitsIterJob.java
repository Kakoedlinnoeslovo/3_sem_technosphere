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
import java.util.Map;
import java.util.HashMap;

public class HitsIterJob extends Configured implements Tool {

    static Map <String, Integer> from = new HashMap<>();
    static  Map <String, Integer> to = new HashMap<>();

    static public class HitsIterJobMapper extends Mapper <LongWritable, Text, Text, Text>{
        @Override
        public final void map(LongWritable offset, Text data, Context context)
                throws IOException, InterruptedException{

            String dataStr = data.toString();

            String[] dataArray = dataStr.split("\t");
            String baseUrl = dataArray[0];

            Integer numberOfInputLinks = Integer.getInteger(dataArray[1].substring(3));
            Integer numberOfOutputLinks = Integer.getInteger(dataArray[2].substring(3));


            //System.out.println(baseUrl);

            for (Integer i = 3; i< numberOfInputLinks; i+=1){
                context.write(new Text (dataArray[i]), new Text("a" + numberOfOutputLinks.toString()));

            }

            for (Integer i = numberOfInputLinks + 3; i < dataArray.length; i+=1){
                context.write(new Text(dataArray[i]), new Text("h" + numberOfInputLinks.toString()));
            }


        }



    }

    static public class HitsIterJobReducer extends Reducer <Text, Text, Text, Text>{
        @Override
        public final void reduce(Text url, Iterable<Text> data, Context context){

        }

    }



    private static Job GetJobConf(Configuration conf, String[] args) throws IOException {
        Job job = Job.getInstance(conf);
        job.setJarByClass(HitsGetTop.class);
        job.setJobName(HitsGetTop.class.getCanonicalName());

        Path inputPath = Constants.HitsOutputPath;

        Path outputPath = Constants.HitsGetTopOutputPath;

        job.setMapperClass(HitsIterJobMapper.class);
        //job.setReducerClass(HitsIterJobReducer.class);

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
