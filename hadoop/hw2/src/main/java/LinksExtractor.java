import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.Base64;
import java.util.LinkedList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.zip.DataFormatException;
import java.util.zip.Inflater;

/**
 * Created by user on 13.10.2018.
 */
public class LinksExtractor {
    public static String buildPath(String path, URL BASE_URL) {
        String result;
        try {
            URL url = new URL(BASE_URL, path);
            if (!url.getHost().endsWith("lenta.ru")) {
                return null;
            }
            result = url.toString();
        } catch (MalformedURLException e) {
            result = BASE_URL.toString() + path;
        }

        return result;
    }

    public static LinkedList<String> extract(String data) throws IOException {
        byte[] decoded = Base64.getDecoder().decode(data);

        Inflater inflater = new Inflater();
        inflater.setInput(decoded);
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        byte outBuffer[] = new byte[1024];
        while (!inflater.finished()) {
            int bytesInflated;
            try {
                bytesInflated = inflater.inflate(outBuffer);
            } catch (DataFormatException e) {
                throw new RuntimeException(e.getMessage());
            }

            baos.write(outBuffer, 0, bytesInflated);
        }
        String HTMLPage = baos.toString("UTF-8");

        Pattern linkPattern = Pattern.compile("<a[^>]+href=[\"']?([^\"'\\s>]+)[\"']?[^>]*>",  Pattern.CASE_INSENSITIVE|Pattern.DOTALL);
        Matcher pageMatcher = linkPattern.matcher(HTMLPage);
        LinkedList<String> links = new LinkedList<>();
        while (pageMatcher.find()) {
            links.add(pageMatcher.group(1));
        }
        return links;
    }

    public static LinkedList<String> merge(List<String> targets, String baseUrl) throws IOException {
        URL BASE_URL = new URL(baseUrl);
        LinkedList<String> links = new LinkedList<>();
        for (String l : targets) {
            String path = buildPath(l, BASE_URL);
            if (path != null) {
                links.add(path);
            }
        }
        return links;
    }

    public static LinkedList<String> extract(String data, String baseUrl) throws IOException {
        return merge(extract(data), baseUrl);
    }
}