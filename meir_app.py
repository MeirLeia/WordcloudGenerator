import streamlit as st
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
import io

# Download NLTK resources
nltk.download('punkt')
nltk.download('stopwords')

# App title
st.title("Word Cloud Generator")

# Sidebar controls
st.sidebar.header("Word Cloud Options")
max_words = st.sidebar.slider("Number of words", min_value=5, max_value=100, step=5, value=50)
text_color = st.sidebar.selectbox("Text colour", ["Black text", "Colorful"])
text_case = st.sidebar.selectbox("Text case", ["All lower case", "All upper case"])
additional_stopwords = st.sidebar.text_input("Additional stop words (comma-separated)", "")

# Text input or file upload
st.subheader("Paste text below or upload a file")
uploaded_file = st.file_uploader("Upload file (.csv or .txt)", type=["csv", "txt"])
raw_text = st.text_area("Paste text here...")

# Process input data
if uploaded_file:
    if uploaded_file.name.endswith('.txt'):
        text_data = uploaded_file.read().decode('utf-8')
    elif uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
        text_data = ' '.join(df.iloc[:, 0].dropna().astype(str))
else:
    text_data = raw_text

# Generate word cloud button
if st.button("Generate word cloud"):
    if text_data.strip():
        # Tokenization and stop words removal
        words = word_tokenize(text_data)
        default_stopwords = set(stopwords.words('english'))
        custom_stopwords = set(map(str.strip, additional_stopwords.split(',')))
        all_stopwords = default_stopwords.union(custom_stopwords)

        filtered_words = [word.lower() for word in words if word.isalnum() and word.lower() not in all_stopwords]

        # Adjust case based on user input
        if text_case == "All upper case":
            filtered_words = [word.upper() for word in filtered_words]

        # Generate word cloud
        wordcloud = WordCloud(
            max_words=max_words,
            background_color='white',
            color_func=None if text_color == "Black text" else lambda *args, **kwargs: (st.sidebar.slider, )

)
    else:
        st.error("Please enter some text or upload a file to generate a word cloud.")
