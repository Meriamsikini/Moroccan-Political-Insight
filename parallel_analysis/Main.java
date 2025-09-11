import com.google.gson.*;
import com.google.gson.reflect.TypeToken;
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.util.List;

public class Main {
    public static void main(String[] args) {
        try {
            List<Tweet> tweets = loadTweets();
            System.out.println("Loaded " + tweets.size() + " tweets");

            TweetAnalyzer analyzer = new TweetAnalyzer();
            AnalysisResult result = analyzer.analyzeTweets(tweets);

            System.out.println("\n=== Analysis Result ===");
            System.out.println(result);

            System.out.println("\nTop Positive Keywords:");
            result.getTopPositiveKeywords().forEach((k, v) ->
                    System.out.printf("- %s (%d occurrences)%n", k, v));

            System.out.println("\nTop Negative Keywords:");
            result.getTopNegativeKeywords().forEach((k, v) ->
                    System.out.printf("- %s (%d occurrences)%n", k, v));

        } catch (Exception e) {
            System.err.println("Error: " + e.getMessage());
            e.printStackTrace();
        }
    }

    private static List<Tweet> loadTweets() throws IOException {
        String filePath = "resources/cleaned_tweets.json";
        try (InputStream is = new FileInputStream(filePath);
             InputStreamReader reader = new InputStreamReader(is, StandardCharsets.UTF_8)) {
            return new Gson().fromJson(reader, new TypeToken<List<Tweet>>(){}.getType());
        }
    }
}