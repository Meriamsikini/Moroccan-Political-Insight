import com.google.gson.annotations.SerializedName;
import java.util.List;

public class Tweet {
    @SerializedName("comments") private int comments;
    @SerializedName("content") private String content;
    @SerializedName("date") private String date;
    @SerializedName("id") private String id;
    @SerializedName("reaction") private int reaction;
    @SerializedName("repostes") private List<Repost> reposts;
    @SerializedName("shares") private int shares;
    @SerializedName("username") private String username;
    @SerializedName("content_cleaned") private String contentCleaned;

    public static class Repost {
        @SerializedName("comments") private String comment;
        @SerializedName("reposter_username") private String reposterUsername;

        public String getComment() { return comment; }
        public String getReposterUsername() { return reposterUsername; }
    }

    // Getters
    public int getComments() { return comments; }
    public String getContent() { return content; }
    public String getDate() { return date; }
    public String getId() { return id; }
    public int getReaction() { return reaction; }
    public List<Repost> getReposts() { return reposts; }
    public int getShares() { return shares; }
    public String getUsername() { return username; }
    public String getContentCleaned() { return contentCleaned; }

    @Override
    public String toString() {
        return String.format("Tweet[%s] by %s: %s... (reactions: %d)",
                id, username, contentCleaned.substring(0, Math.min(30, contentCleaned.length())), reaction);
    }
}