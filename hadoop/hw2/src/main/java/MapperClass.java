

import java.io.IOException;
import java.util.StringTokenizer;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

import org.apache.hadoop.util.Tool;
import org.apache.hadoop.conf.Configured;
import java.util.LinkedList;


//public class MapperClass extends Mapper <LongWritable, Text, Text, IntWritable>
//{
//
//    private final static IntWritable one = new IntWritable(1);
//    private Text word = new Text();
//
//    @Override
//    protected void map(LongWritable key, Text value, Context context)
//        throws  IOException, InterruptedException{
//        String line = value.toString();
//        StringTokenizer st = new StringTokenizer(line, " ");
//
//        while (st.hasMoreTokens()){
//            word.set(st.nextToken());
//            context.write(word, one);
//        }
//    }
//}

public class MapperClass {

    static public class GraphBuilderMapper extends Mapper<LongWritable, Text, IntWritable, Text> {
        @Override
        protected void map(LongWritable offset, Text data, Context context)
                throws IOException, InterruptedException {
            String line = data.toString();
            String[] idContent = line.split("\t");
            int id = Integer.valueOf(idContent[0]);
            String content = idContent[1];

            LinkedList<String> outgoingLinksList = LinksExtractor.extract(content);

            StringBuilder sb = new StringBuilder();
            sb.append("L");
            for (String l : outgoingLinksList) {
                sb.append(l);
                sb.append("\t");
            }

            context.write(new IntWritable(id), new Text(sb.toString()));
        }
    }
}
