import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.WritableComparable;
import org.apache.hadoop.io.Text;

import java.io.DataInput;
import java.io.DataOutput;
import java.io.IOException;
import javax.annotation.Nonnull;

public class TextIntPair implements WritableComparable <TextIntPair> {

    private Text url;
    private IntWritable counter;


    public TextIntPair(String url, int counter)
    {
        set(new Text(url), new IntWritable(counter));
    }

    private void set(Text a, IntWritable b)
    {
        url = a;
        counter = b;
    }

    public Text getFirst()
    {
        return url;
    }

    public IntWritable getSecond()
    {
        return counter;
    }

    @Override
    public void write(DataOutput out) throws IOException
    {
        url.write(out);
        counter.write(out);
    }

    @Override
    public void readFields(DataInput in) throws IOException {
        url.readFields(in);
        counter.readFields(in);
    }


    @Override
    public int compareTo(@Nonnull TextIntPair o){

        Text thisText = this.url;
        IntWritable thisInt = this.counter;

        int cmp = thisText.compareTo(o.url);
        return (cmp == 0) ? thisInt.compareTo(o.counter) : cmp;
    }



}
