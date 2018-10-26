import java.io.IOException;
import java.util.Base64;
import java.util.zip.DataFormatException;
import java.util.zip.Inflater;
import java.util.LinkedList;
import java.io.ByteArrayOutputStream;
import java.util.logging.Logger;

class getLinks {
    private static final Logger LOG = Logger.getLogger(getLinks.class.getName());

     static LinkedList<String> extract (String data) throws IOException {

        LinkedList result  = new LinkedList<String>();
        byte[] decoded = Base64.getDecoder().decode(data);

        Inflater inflater = new Inflater();
        inflater.setInput(decoded);

        ByteArrayOutputStream baos = new ByteArrayOutputStream(data.length());
        byte[] buffer = new byte[1024];

        while (!inflater.finished()){
            int bytesInflated = 0;
            try{
                bytesInflated = inflater.inflate(buffer);
            } catch (DataFormatException e){
                throw new RuntimeException(e.getMessage());
            }
            baos.write(buffer, 0, bytesInflated);
        }

        String HTML = baos.toString("UTF-8");

        LOG.fine("Original size: " + data.length()/1024 + "KB");
        LOG.fine ("Compressed size: " + HTML.length()/1024 + "KB");


        return result;

    }

}