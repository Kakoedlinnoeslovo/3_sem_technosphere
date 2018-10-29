import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Counters;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.util.ToolRunner;

import java.io.IOException;
import java.util.*;

public class HitsInitJob extends Configured implements Tool {

    @Override
    public int run(String[] args) throws Exception {
        Job job = GetJobConf(getConf());
        int result = job.waitForCompletion(true) ? 0 : 1;
        Counters counters = job.getCounters();
        long hang = counters.findCounter("COMMON_COUNTERS", "HANGING_VERTEXES").getValue();
        long total = counters.findCounter("COMMON_COUNTERS", "TOTAL_VERTEXES").getValue();
        System.out.println("Hanging vertexes " + hang + "/" + total);
        return result;
    }

    static public class HitsInitMapper extends Mapper<LongWritable, Text, Text, Text> {
        @Override
        protected void map(LongWritable offset, Text data, Context context)
                throws IOException, InterruptedException
        {
            String[] allLinks = data.toString().split("\t");
            String from = allLinks[0];
            String to;
            for (int i = 1; i < allLinks.length; i += 1) {
                to = allLinks[i];
                context.write(new Text(from), new Text('>' + to));
                context.write(new Text(to), new Text('<' + from));
            }
        }
    }

    public static class HitsInitReducer extends Reducer<Text, Text, Text, Text> {
        @Override
        protected void reduce(Text url, Iterable<Text> values, Context context)
                throws IOException, InterruptedException {

            LinkedList<String> from = new LinkedList<>();
            LinkedList<String> to = new LinkedList<>();

            for (Text _val : values) {
                String val = _val.toString();
                if (val.charAt(0) == '>') {
                    to.add(val.substring(1));
                } else {
                    from.add(val.substring(1));
                }
            }
            context.getCounter("COMMON_COUNTERS", "TOTAL_VERTEXES").increment(1);
            if (to.isEmpty()) {
                context.getCounter("COMMON_COUNTERS", "HANGING_VERTEXES").increment(1);
            }

            LinkedList<String> all = new LinkedList<>();

            all.add("|F|\t");
            String sizeFrom = Integer.toString(from.size());
            all.add(sizeFrom + "\t");

            for (String f : from) {
                all.add(f + "\t");
            }

            all.add("|T|\t");
            String sizeTo = Integer.toString(to.size());
            all.add(sizeTo + "\t");

            for (String t : to) {
                all.add(t + "\t");
            }

            context.write(new Text(url), new Text(all.toString()));

        }

    }

    private static Job GetJobConf(Configuration conf) throws IOException {
        Job job = Job.getInstance(conf);
        job.setJarByClass(HitsInitJob.class);
        job.setJobName(HitsInitJob.class.getCanonicalName());

        FileInputFormat.addInputPath(job, Constants.outputPath);
        FileOutputFormat.setOutputPath(job, Constants.HitsOutputPath);

        job.setMapperClass(HitsInitMapper.class);
        job.setReducerClass(HitsInitReducer.class);
        job.setMapOutputKeyClass(Text.class);
        job.setMapOutputValueClass(Text.class);

        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(Text.class);

        return job;
    }

    public static void main(String[] args) throws Exception {
        int exitCode = ToolRunner.run(new HitsInitJob(), args);
        System.exit(exitCode);
    }
}