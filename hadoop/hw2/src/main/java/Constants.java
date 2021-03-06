import org.apache.hadoop.fs.Path;

class Constants {
    static final Path inputPath = new Path("/data/infopoisk/hits_pagerank/docs-*.txt");
    static final Path urlsPath = new Path("/data/infopoisk/hits_pagerank/urls.txt");
    static final Path outputPath = new Path("out");
    static final Path HitsOutputPath = new Path("HitsInitJobOut");

    static final Path HitsTopOutputPath = new Path("HitsTopOutput");
}
