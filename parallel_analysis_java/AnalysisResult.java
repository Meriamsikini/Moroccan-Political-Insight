import java.util.Map;

public class AnalysisResult {
    private final int totalTweets;
    private final int positiveTweets;
    private final int negativeTweets;
    private final int neutralTweets;
    private final Map<String, Integer> topPositiveKeywords;
    private final Map<String, Integer> topNegativeKeywords;

    public AnalysisResult(int total, int positive, int negative, int neutral,
                          Map<String, Integer> topPositive, Map<String, Integer> topNegative) {
        this.totalTweets = total;
        this.positiveTweets = positive;
        this.negativeTweets = negative;
        this.neutralTweets = neutral;
        this.topPositiveKeywords = topPositive;
        this.topNegativeKeywords = topNegative;
    }

    // Getters
    public int getTotalTweets() { return totalTweets; }
    public int getPositiveTweets() { return positiveTweets; }
    public int getNegativeTweets() { return negativeTweets; }
    public int getNeutralTweets() { return neutralTweets; }
    public Map<String, Integer> getTopPositiveKeywords() { return topPositiveKeywords; }
    public Map<String, Integer> getTopNegativeKeywords() { return topNegativeKeywords; }

    @Override
    public String toString() {
        return String.format(
                "Analysis[Total: %d, Positive: %d (%.1f%%), Negative: %d (%.1f%%), Neutral: %d]",
                totalTweets,
                positiveTweets, (positiveTweets * 100.0 / totalTweets),
                negativeTweets, (negativeTweets * 100.0 / totalTweets),
                neutralTweets
        );
    }
}