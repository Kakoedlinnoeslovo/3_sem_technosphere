import java.io.IOException;
import java.util.Iterator;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;



public class ReducerClass extends Reducer <Text, IntWritable, Text, IntWritable> {

    private IntWritable count = new IntWritable();

    @Override
    protected void reduce(Text key, Iterable<IntWritable> values, Context context)
            throws IOException, InterruptedException {
        int sum = 0;
        Iterator valuesIt = values.iterator();


        for(IntWritable value: values){
            sum += value.get();
        }

        count.set(sum);
        context.write(key, count);
    }
}
