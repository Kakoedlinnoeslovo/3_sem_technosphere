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

public class HitsGetTop extends Configured implements Tool {

   static Map <String, Integer> from = new HashMap<>();
   static  Map <String, Integer> to = new HashMap<>();

    static public class HitsgetTopMapperInit extends Mapper <LongWritable, Text, Text, Text>{
        @Override
        public final void map(LongWritable offset, Text data, Context context)
                throws IOException{

                String dataStr = data.toString();

                String[] dataArray = dataStr.split("\t");
                String baseUrl = dataArray[0];

                //System.out.println(baseUrl);

                for (Integer i = 1; i< dataArray.length; i+=1){
                    if (dataArray[i].substring(0, 3).equals("|F|")){
                        System.out.println("FROM URLS is " + dataArray[i].substring(3));
                        from.put(baseUrl, Integer.getInteger(dataArray[i].substring(3)));
                    }
                    if (dataArray[i].substring(0, 3).equals("|T|")){
                        System.out.println("TO URLS is " + dataArray[i].substring(3));
                        to.put(baseUrl, Integer.getInteger(dataArray[i].substring(3)));
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

        Path inputPath = Constants.HitsOutputPath;

        Path outputPath = Constants.HitsGetTopOutputPath;

        job.setMapperClass(HitsgetTopMapperInit.class);
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
