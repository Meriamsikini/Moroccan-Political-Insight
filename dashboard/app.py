import streamlit as st
import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
import seaborn as sns
#from wordcloud import WordCloud
from datetime import datetime
from io import StringIO

# --- CONFIG ---
st.set_page_config(page_title="Analyse Big Data - Tweets Politiques Marocains", layout="wide")

# --- LOAD DATA ---
@st.cache_data
def load_data():
    # Load cleaned tweets
    with open("cleaned_tweets.json", "r", encoding="utf-8") as f:
        cleaned = json.load(f)
    df_cleaned = pd.DataFrame(cleaned)
    # Load classified tweets
    df_classified = pd.read_csv("classified_tweets.csv", encoding="utf-8")
    # Clean classified orientation
    df_classified['classe'] = df_classified['classe'].str.lower().str.replace(' ', '').str.replace('"', '')
    return df_cleaned, df_classified

df_cleaned, df_classified = load_data()

# --- PREPROCESS ---
# Parse dates
df_cleaned['date'] = pd.to_datetime(df_cleaned['date'], errors='coerce')
df_classified['date'] = pd.to_datetime(df_classified['date'], errors='coerce')

# Merge orientation politique
def match_orientation(row):
    # Find classified tweet with same date and similar content
    candidates = df_classified[df_classified['date'] == row['date']]
    for _, cand in candidates.iterrows():
        if cand['tweet'][:30] in row.get('content_cleaned', '') or cand['tweet'][:30] in row.get('content', ''):
            return cand['classe']
    return np.nan

if 'orientation' not in df_cleaned.columns:
    df_cleaned['orientation'] = df_cleaned.apply(match_orientation, axis=1)

# --- FILTERS ---
st.sidebar.header("Filtres")
min_date = min(df_cleaned['date'].min(), df_classified['date'].min())
max_date = max(df_cleaned['date'].max(), df_classified['date'].max())
date_start = st.sidebar.date_input("Date de début", min_value=min_date.date(), value=min_date.date())
date_end = st.sidebar.date_input("Date de fin", min_value=min_date.date(), value=max_date.date())
partis = st.sidebar.multiselect(
    "Partis politiques",
    options=["PJD", "RNI", "PAM", "perdre confiance"],
    default=["PJD", "RNI", "PAM", "perdre confiance"]
)

def filter_data(df_cleaned, df_classified, date_start, date_end, partis):
    # Filter by date
    mask_cleaned = (df_cleaned['date'] >= pd.to_datetime(date_start)) & (df_cleaned['date'] <= pd.to_datetime(date_end))
    mask_classified = (df_classified['date'] >= pd.to_datetime(date_start)) & (df_classified['date'] <= pd.to_datetime(date_end))
    # Filter by orientation
    def has_parti(classe):
        for p in partis:
            if p.lower() in classe:
                return True
        return False
    df_cleaned_f = df_cleaned[mask_cleaned & df_cleaned['orientation'].fillna('').apply(has_parti)]
    df_classified_f = df_classified[mask_classified & df_classified['classe'].fillna('').apply(has_parti)]
    return df_cleaned_f, df_classified_f

if st.sidebar.button("Actualiser"):
    st.experimental_rerun()

df_cleaned_f, df_classified_f = filter_data(df_cleaned, df_classified, date_start, date_end, partis)

# --- OVERVIEW CARDS ---
st.markdown("## Vue d'ensemble")
col1, col2, col3, col4 = st.columns(4)

def get_percent(df, key):
    total = len(df)
    if total == 0:
        return 0
    return round(100 * df['orientation'].fillna('').str.contains(key).sum() / total, 1)

def get_evolution(df, key):
    # Compare last month vs previous month
    dfm = df.copy()
    dfm['month'] = dfm['date'].dt.to_period('M')
    months = sorted(dfm['month'].unique())
    if len(months) < 2:
        return 0
    last, prev = months[-1], months[-2]
    last_count = dfm[(dfm['month'] == last) & dfm['orientation'].fillna('').str.contains(key)].shape[0]
    prev_count = dfm[(dfm['month'] == prev) & dfm['orientation'].fillna('').str.contains(key)].shape[0]
    if prev_count == 0:
        return 0
    return round(100 * (last_count - prev_count) / prev_count, 1)

pro_pjd = get_percent(df_cleaned_f, "propjd")
contre_pjd = get_percent(df_cleaned_f, "contrepjd")
pro_rni = get_percent(df_cleaned_f, "prorni")
contre_rni_abs = df_cleaned_f['orientation'].fillna('').str.contains("contrerni").sum()
contre_rni_evol = get_evolution(df_cleaned_f, "contrerni")

col1.metric("Opinion pro PJD (%)", pro_pjd, f"{get_evolution(df_cleaned_f, 'propjd')}%")
col2.metric("Opinion contre PJD (%)", contre_pjd, f"{get_evolution(df_cleaned_f, 'contrepjd')}%")
col3.metric("Opinion pro RNI (%)", pro_rni, f"{get_evolution(df_cleaned_f, 'prorni')}%")
col4.metric("Opinion contre RNI (abs)", contre_rni_abs, f"{contre_rni_evol}%")

st.markdown("---")



# --- ENGAGEMENT PAR MOIS ---
st.subheader("Engagement par mois")
df_eng = df_cleaned_f.copy()
df_eng['month'] = df_eng['date'].dt.to_period('M')
dfm = df_eng.groupby('month').agg({
    'reaction': 'sum',
    'shares': 'sum',
    'comments': 'sum'
}).reset_index()
dfm['month'] = dfm['month'].astype(str)

fig, ax = plt.subplots(figsize=(10, 4))
ax.bar(dfm['month'], dfm['reaction'], label='Réactions', color='royalblue')
ax.bar(dfm['month'], dfm['shares'], bottom=dfm['reaction'], label='Partages', color='mediumseagreen')
ax.bar(dfm['month'], dfm['comments'], bottom=dfm['reaction']+dfm['shares'], label='Commentaires', color='orange')
ax.set_ylabel("Engagement")
ax.set_xlabel("Mois")
ax.legend()
plt.xticks(rotation=45)
st.pyplot(fig)

# --- EVOLUTION DES OPINIONS ---
st.subheader("Évolution des opinions")
df_classified_f['month'] = df_classified_f['date'].dt.to_period('M')
categories = {
    "pro PJD": "propjd",
    "pro RNI": "prorni",
    "pro PAM": "propam",
    "perdre confiance": "perdreconfiance"
}
df_evol = pd.DataFrame({'month': sorted(df_classified_f['month'].unique())})
for label, key in categories.items():
    df_evol[label] = [
        df_classified_f[(df_classified_f['month'] == m) & df_classified_f['classe'].str.replace(' ', '').str.contains(key)].shape[0]
        for m in df_evol['month']
    ]
df_evol['month'] = df_evol['month'].astype(str)

fig, ax = plt.subplots(figsize=(10, 4))
for label in categories.keys():
    ax.plot(df_evol['month'], df_evol[label], marker='o', label=label)
ax.set_xlabel("Mois")
ax.set_ylabel("Nombre de publications")
ax.legend()
plt.xticks(rotation=45)
st.pyplot(fig)

# --- REPARTITION PAR PARTI ---
st.subheader("Répartition par parti politique")
parti_map = {
    "PJD": "pjd",
    "RNI": "rni",
    "PAM": "pam",
    "perdre confiance": "perdreconfiance"
}
counts = []
labels = []
for label, key in parti_map.items():
    count = df_classified_f['classe'].str.replace(' ', '').str.contains(key).sum()
    if count > 0:
        counts.append(count)
        labels.append(label)
fig, ax = plt.subplots()
ax.pie(counts, labels=labels, autopct='%1.1f%%', startangle=90)
ax.axis('equal')
st.pyplot(fig)

# --- TABLEAU DES PUBLICATIONS LES PLUS ENGAGÉES ---
orientation_map = {
    "propjd": "Pro PJD",
    "contrepjd": "Contre PJD",
    "prorni": "Pro RNI",
    "contrerni": "Contre RNI",
    "propam": "Pro PAM",
    "perdreconfiance": "Perdre confiance"
}

st.subheader("Publications les plus engagées")
df_tab = df_cleaned_f.copy()
df_tab['engagement'] = (
    df_tab['reaction'].fillna(0) 
    + df_tab['shares'].fillna(0) 
    + df_tab['comments'].fillna(0)
)
df_tab = df_tab.sort_values('engagement', ascending=False).head(5)

def truncate(text, n=60):
    return text if len(text) <= n else text[:n] + "..."

table_data = []
for _, row in df_tab.iterrows():
    orientation = row.get('orientation', '')
    orientation = orientation_map.get(orientation, orientation)  # conversion lisible
    
    table_data.append([
        row.get('username', ''),
        truncate(row.get('content_cleaned', row.get('content', '')), 60),
        row['date'].strftime('%Y-%m-%d') if pd.notnull(row['date']) else '',
        int(row.get('reaction', 0)),
        int(row.get('shares', 0)),
        int(row.get('comments', 0)),
        orientation
    ])

df_table = pd.DataFrame(table_data, columns=[
    "Utilisateur", "Contenu", "Date", "Réactions", "Partages", "Commentaires", "Orientation politique"
])
st.dataframe(df_table)


# --- EXPORT BUTTON ---
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Exporter le tableau en CSV",
    data=convert_df(df_table),
    file_name='publications_engagees.csv',
    mime='text/csv'
)