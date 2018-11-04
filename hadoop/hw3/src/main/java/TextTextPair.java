import org.apache.hadoop.io.WritableComparable;
import org.apache.hadoop.io.Text;

import java.io.DataInput;
import java.io.DataOutput;
import java.io.IOException;
import javax.annotation.Nonnull;

public class TextTextPair implements WritableComparable <TextTextPair> {

    private Text query;
    private Text host;
    private static int HASHCONST = 163;



    public TextTextPair()
    {
        set(new Text(), new Text());
    }


    public TextTextPair(String host, String query)
    {

        set(new Text(query), new Text(host));
    }

    private void set(Text a, Text b)
    {
        query = a;
        host = b;
    }

    public Text getFirst()
    {
        return query;
    }

    public Text getSecond()
    {
        return host;
    }

    @Override
    public void write(DataOutput out) throws IOException
    {
        query.write(out);
        host.write(out);
    }

    @Override
    public void readFields(DataInput in) throws IOException
    {
        query.readFields(in);
        host.readFields(in);
    }


    @Override
    public int compareTo(@Nonnull TextTextPair o)
    {

        Text thisText = this.query;
        Text thisInt = this.host;

        int cmp = thisText.compareTo(o.query);


        int ccr =  thisInt.compareTo(o.host);

        //вк vk.com 7
        //вконтакте vk.com 7

        return (cmp == 0) ? ccr: cmp;
    }

    @Override
    public int hashCode()
    {
        return query.hashCode() * HASHCONST + host.hashCode();
    }

    @Override
    public String toString()
    {
        return query + "\t" + host;
    }



}
