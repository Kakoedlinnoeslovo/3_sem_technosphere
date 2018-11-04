import org.apache.hadoop.io.WritableComparable;
import org.apache.hadoop.io.Text;

import java.io.DataInput;
import java.io.DataOutput;
import java.io.IOException;
import javax.annotation.Nonnull;

public class TextTextPair implements WritableComparable <TextTextPair> {

    private Text host;
    private Text query;
    private static final int HASHCONST = 163;



    public TextTextPair()
    {
        set(new Text(), new Text());
    }


    public TextTextPair(String host, String query)
    {

        set(new Text(host), new Text(query));
    }

    private void set(Text a, Text b)
    {
        host = a;
        query = b;
    }

    public Text getFirst()
    {
        return host;
    }

    public Text getSecond()
    {
        return query;
    }

    @Override
    public void write(DataOutput out) throws IOException
    {
        host.write(out);
        query.write(out);
    }

    @Override
    public void readFields(DataInput in) throws IOException
    {
        host.readFields(in);
        query.readFields(in);
    }


    @Override
    public int compareTo(@Nonnull TextTextPair o)
    {

        Text thisText = this.host;
        Text thisInt = this.query;

        int cmp = thisText.compareTo(o.host);


        int ccr =  thisInt.compareTo(o.query);

        //вк vk.com 7
        //вконтакте vk.com 7

        return (cmp == 0) ? ccr: cmp;
    }

    @Override
    public int hashCode()
    {
        return host.hashCode() * HASHCONST + query.hashCode();
    }

    @Override
    public String toString()
    {
        return query + "\t" + host;
    }



}
