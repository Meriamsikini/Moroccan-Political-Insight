import com.google.gson.*;
import java.util.*;
import java.util.concurrent.*;
import java.util.concurrent.atomic.*;
import java.util.stream.*;

public class TweetAnalyzer {
    private static final Map<String, String> POSITIVE_KEYWORDS = Map.of(
            "العدالة والتنمية", "PJD", "بنكيران", "Ancien PM", "إصلاح", "Réforme",
            "التقدم", "Progrès", "الجدية", "Sérieux", "التنمية", "Développement"
    );

    private static final Map<String, String> NEGATIVE_KEYWORDS = Map.of(
            "الأحرار", "RNI", "أخنوش", "PM actuel", "الفساد", "Corruption",
            "الغلاء", "Vie chère", "الرشوة", "Pot-de-vin", "البطالة", "Chômage"
    );

    public AnalysisResult analyzeTweets(List<Tweet> tweets) {
        AtomicInteger positive = new AtomicInteger();
        AtomicInteger negative = new AtomicInteger();
        AtomicInteger neutral = new AtomicInteger();

        ExecutorService executor = Executors.newFixedThreadPool(Runtime.getRuntime().availableProcessors());

        tweets.forEach(tweet -> executor.execute(() -> {
            int score = analyzeSentiment(tweet.getContentCleaned());
            if (score > 0) positive.incrementAndGet();
            else if (score < 0) negative.incrementAndGet();
            else neutral.incrementAndGet();
        }));

        executor.shutdown();
        try { executor.awaitTermination(1, TimeUnit.MINUTES); }
        catch (InterruptedException e) { Thread.currentThread().interrupt(); }

        return new AnalysisResult(
                tweets.size(),
                positive.get(),
                negative.get(),
                neutral.get(),
                getTopKeywords(tweets, POSITIVE_KEYWORDS),
                getTopKeywords(tweets, NEGATIVE_KEYWORDS)
        );
    }

    private int analyzeSentiment(String text) {
        long positive = POSITIVE_KEYWORDS.keySet().stream().filter(text::contains).count();
        long negative = NEGATIVE_KEYWORDS.keySet().stream().filter(text::contains).count();
        return (int)(positive - negative);
    }

    private Map<String, Integer> getTopKeywords(List<Tweet> tweets, Map<String, String> keywords) {
        return keywords.keySet().stream()
                .collect(Collectors.toMap(
                        keyword -> keyword,
                        keyword -> (int)tweets.stream()
                                .filter(t -> t.getContentCleaned().contains(keyword))
                                .count()
                ))
                .entrySet().stream()
                .sorted(Map.Entry.<String, Integer>comparingByValue().reversed())
                .limit(5)
                .collect(Collectors.toMap(
                        Map.Entry::getKey,
                        Map.Entry::getValue,
                        (e1, e2) -> e1,
                        LinkedHashMap::new
                ));
    }
}