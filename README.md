# 🟢 Moroccan-Political-Insight

**Moroccan-Political-Insight** is a comprehensive project designed to analyze and visualize political opinions and trends in Morocco. It implements a **real-time Big Data pipeline**, leverages a **large language model (Mistral 7B)** for tweet classification. Finally, the results are presented in an interactive **Streamlit dashboard**.  

---

## 📌 Project Overview

This project provides insights into Moroccan political discussions on social media by analyzing public tweets related to political parties, leaders, and government actions. The pipeline includes:

1. **Data ingestion**: Tweets are collected and stored in Firebase.  
2. **Real-time streaming & cleaning**: Data is streamed from Firebase to Kafka, processed with Spark Streaming, and stored in Hadoop HDFS.  
3. **Export cleaned data**: Cleaned JSON tweets are exported from Hadoop to local storage using WinSCP.  
4. **AI-based classification**: Tweets are classified using the **Mistral 7B** model to detect support or criticism toward political parties.  
5. **Interactive dashboard**: A Streamlit app visualizes trends, keyword frequencies, and classification results.  
 


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
├── classified/                   # Tweets classified by LLM (Mistral 7B)
│   └── classified_tweets.csv
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
- `cleaned_tweets.json` first exports the cleaned JSON from HDFS (Hortonworks Sandbox VM) to local VM using :
 ``` hdfs dfs -get /user/root/cleaned_tweets_output_json/part-00000-*.json /root/cleaned_tweets.json```
- Then, the file is copied from the Hadoop VM to Windows using WinSCP.
- This ensures the cleaned dataset is available locally for LLM classification.
 
### 4️⃣ Classification: `mistral_classification.ipynb`
- Loads **cleaned tweets**.  
- Uses **Mistral 7B LLM** for classification into political labels (pro/contre parties).  
- Generates a CSV with `tweet` and `classe` columns.

### 5️⃣ Dashboard: `app.py`
- Streamlit-based interactive dashboard.  
- Visualizes:
  - Tweet distribution by political class.  
  - Top keywords in positive/negative tweets.
  - - Interactive trend graphs. 

### 6️⃣ Commands: `hadoop_commands.txt`
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
LLM Classification (Mistral 7B, in Colab)  → classified/classified_tweets.csv
      │
      ▼
Streamlit Dashboard (app.py)
```
---
## 🛠️ Tech Stack

- **Data sources & ingestion**: Firebase Realtime Database

- **Streaming & Processing**: Kafka, Apache Spark Streaming, Hadoop HDFS

- **LLM Classification**: Mistral 7B (executed in Google Colab)

- **Visualization**: Streamlit

- **Utilities** : WinSCP (for file transfer from Hadoop VM to Windows)

 ---

### 📝 Note on the Hadoop Environment

- The entire Big Data pipeline was executed in **Hortonworks Sandbox (Hadoop VM)**.  
- Tweets collected from **Firebase** were **streamed in real-time to Kafka** on the Sandbox.  
- **Spark Streaming** processed these tweets in the Sandbox and stored them in **HDFS**.  
- The cleaned JSON file (`cleaned_tweets.json`) was then **exported from HDFS to the local file system of the Sandbox**, and subsequently transferred to **Windows** via **WinSCP** for LLM classification in Colab.  

---
⚠️ Note: LLM classification is executed in Google Colab, which provides GPU acceleration for the Mistral 7B model.
---
  
##  👩‍💻 Author

**Meriam Sikini**
