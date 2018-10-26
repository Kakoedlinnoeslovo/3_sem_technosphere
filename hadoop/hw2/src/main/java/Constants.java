import org.apache.hadoop.fs.Path;

public class Constants {
    public static final Path inputPath = new Path("/data/infopoisk/hits_pagerank/docs-*.txt");
    public static final Path urlsPath = new Path("/data/infopoisk/hits_pagerank/urls.txt");
    public static final Path outputPath = new Path("out");
}
