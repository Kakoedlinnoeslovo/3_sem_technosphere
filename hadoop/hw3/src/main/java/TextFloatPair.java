import org.apache.hadoop.io.FloatWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.io.WritableComparable;

import java.io.DataOutput;
import java.io.IOException;
import java.io.DataInput;
import javax.annotation.Nonnull;


public class TextFloatPair implements WritableComparable<TextFloatPair>
{
    private Text first;
    private FloatWritable second;


    public TextFloatPair()
    {
        set (new Text(), new FloatWritable());
    }

    public TextFloatPair(String first, float second)
    {
     set(new Text(first), new FloatWritable(second));
    }

    private void set(Text a, FloatWritable b)
    {
        first = a;
        second = b;
    }

    public Text getFirst()
    {
        return first;
    }

    public FloatWritable getSecond()
    {
        return second;
    }

    @Override
    public void write(DataOutput out) throws IOException
    {
        first.write(out);
        second.write(out);
    }

    @Override
    public void readFields(DataInput in) throws IOException {
        first.readFields(in);
        second.readFields(in);
    }

    @Override
    public int compareTo(@Nonnull TextFloatPair o)
    {
        int cmp = first.compareTo(o.first);
        return (cmp == 0) ? - second.compareTo(o.second) : cmp;
    }

    @Override
    public int hashCode()
    {
        return first.hashCode() * 163 + second.hashCode();
    }


    public boolean equals(Object obj){
        if (obj instanceof TextFloatPair){
            TextFloatPair tp = (TextFloatPair) obj;
            return first.equals(tp.first) && second.equals(tp.second);
        }
        return false;
    }

    public String toString()
    {
        return first + "\t" + second;
    }


}
