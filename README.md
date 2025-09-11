# 🟢 Moroccan-Political-Insight

**Moroccan-Political-Insight** is a comprehensive project designed to analyze and visualize political opinions and trends in Morocco. It implements a **real-time Big Data pipeline**, leverages a **large language model (Mistral 7B)** for tweet classification, and performs **parallel sentiment analysis in Java**. Finally, the results are presented in an interactive **Streamlit dashboard**.  

---

## 📌 Project Overview

This project provides insights into Moroccan political discussions on social media by analyzing public tweets related to political parties, leaders, and government actions. The pipeline includes:

1. **Data ingestion**: Tweets are collected and stored in Firebase.  
2. **Real-time streaming & cleaning**: Data is streamed from Firebase to Kafka, processed with Spark Streaming, and stored in Hadoop HDFS.  
3. **Export cleaned data**: Cleaned JSON tweets are exported from Hadoop to local storage using WinSCP.  
4. **AI-based classification**: Tweets are classified using the **Mistral 7B** model to detect support or criticism toward political parties.  
5. **Parallel sentiment analysis (Java)**: Positive, negative, and neutral tweet counts are computed, with top keywords identified using a parallelized Java implementation.  
6. **Interactive dashboard**: A Streamlit app visualizes trends, keyword frequencies, and classification results.  


---

## 🗂️ Project Structure
```
Moroccan-Political-Insight/
│── README.md
│── requirements.txt
│
├── producer/                     # Data ingestion
│   └── firebase_producer.py
│
├── streaming/                    # Real-time cleaning
│   └── stream_to_hdfs.py
│
├── data/                         # Raw input data
│   └── tweets.json
│
├── exports/                      # Data exported from Hadoop
│   └── cleaned_tweets.json
│
├── LLM_classification/               # AI classification (Colab)
│   └── mistral_classification.ipynb
│
├── parallel_analysis/             # Java sentiment analysis
│   ├── Tweet.java
│   ├── AnalysisResult.java
│   ├── TweetAnalyzer.java
│   └── Main.java
│
├── dashboard/                    # Visualization
│   └── app.py
│
└── commands/                     # Hadoop, Kafka & Spark commands
    └── hadoop_commands.txt

```

---

## 🛠️ Key Components

### 1️⃣ Producer: `firebase_producer.py`
- Reads raw tweets from Firebase Realtime Database.  
- Publishes tweets to a Kafka topic (`json-topic`) for real-time streaming.

### 2️⃣ Streaming: `stream_to_hdfs.py`
- Spark Structured Streaming job that:
  - Reads tweets from Kafka.  
  - Cleans the text (removes extra spaces, special characters).  
  - Saves the cleaned data to **HDFS** in JSON format.  

### 3️⃣ Exports
- `cleaned_tweets.json` is first exported from HDFS to the local Hadoop VM using Hadoop commands:
 ``` hdfs dfs -get /user/root/cleaned_tweets_output_json/part-00000-*.json /root/cleaned_tweets.json```
- Then, the file is copied from the Hadoop VM to Windows using WinSCP.
- This ensures the cleaned dataset is available locally for LLM classification.
 
### 4️⃣ Classification: `mistral_classification.ipynb`
- Loads **cleaned tweets**.  
- Uses **Mistral 7B LLM** for classification into political labels (pro/contre parties).  
- Generates a CSV with `tweet` and `classe` columns.

### 5️⃣ Parallel Analysis: Java
- Computes **positive, negative, and neutral tweet counts** in parallel.  
- Extracts top keywords for positive and negative tweets.  
- Classes: `Tweet`, `TweetAnalyzer`, `AnalysisResult`, and `Main`.

### 6️⃣ Dashboard: `dashboard_app.py`
- Streamlit-based interactive dashboard.  
- Visualizes:
  - Tweet distribution by political class.  
  - Top keywords in positive/negative tweets.  
  - Interactive trend graphs.

### 7️⃣ Commands: `hadoop_commands.txt`
- Provides **step-by-step commands** for:
  - Starting Zookeeper and Kafka.  
  - Creating Kafka topics.  
  - Running Spark Streaming.  
  - Exporting cleaned tweets from HDFS.

---

## ⚡ Workflow / Pipeline
```
Firebase (raw tweets)
      │
      ▼
Kafka Topic ("json-topic")
      │
      ▼
Spark Streaming → HDFS (cleaned_tweets.json)
      │
      ▼
Export from HDFS → Local Hadoop VM → Windows (WinSCP)
      │
      ▼
LLM Classification (Mistral 7B, in Colab)
      │
      ▼
Parallel Sentiment Analysis (Java)
      │
      ▼
Streamlit Dashboard (dashboard_app.py)
```
---
## 🛠️ Tech Stack

- **Data sources & ingestion**: Firebase Realtime Database

- **Streaming & Processing**: Kafka, Apache Spark Streaming, Hadoop HDFS

- **LLM Classification**: Mistral 7B (executed in Google Colab)

- **Parallel Analysis**: Java (multithreaded sentiment analysis)

- **Visualization**: Streamlit

- **Utilities** : WinSCP (for file transfer from Hadoop VM to Windows)
##  👩‍💻 Author

**Meriam Sikini**
