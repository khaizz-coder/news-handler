import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai

# Load API Key
load_dotenv()
GOOGLE_API_KEY = os.getenv("AIzaSyBkqGIHS7iY8fLt5N__OEJELyD8aMoVVOs")
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize Gemini Flash
model = genai.GenerativeModel("gemini-2.0-flash")

# Clean and correct article
def clean_article(text, tone):
    prompt = f"""
    Clean and improve the following Urdu news article.
    - Fix grammar and structure.
    - Apply a {tone} tone.

    Article:
    \"\"\"{text}\"\"\"

    Cleaned Article:"""
    res = model.generate_content(prompt)
    return res.text.strip()

# Generate 2 headlines
def generate_headlines(text, tone):
    prompt = f"""
    Generate two headlines for the following Urdu article.
    Tone: {tone}
    Limit: 15 words each.

    Article:
    \"\"\"{text}\"\"\"

    Headlines:
    1.
    2."""
    res = model.generate_content(prompt)
    lines = res.text.strip().split("\n")
    headlines = [line.replace("1.", "").replace("2.", "").strip() for line in lines if line.strip()]
    return headlines[:2]

# Streamlit UI
st.set_page_config(page_title="📰 Urdu News AI", layout="centered")
st.title("📰 Urdu News Article Cleaner + Headline Generator")

st.write("Enter your Urdu news article below. Select a tone. The app will clean it and generate 2 headlines.")

# User inputs
article_input = st.text_area("📝 Paste Urdu News Article Here", height=250)
tone = st.selectbox("🎭 Select Tone", ["Neutral", "Formal", "Dramatic", "Funny", "Sensational", "Inspiring"])

if st.button("Generate"):
    if article_input.strip():
        with st.spinner("Cleaning and Generating..."):
            cleaned = clean_article(article_input, tone)
            headlines = generate_headlines(cleaned, tone)

        st.subheader("🧹 Cleaned Article")
        st.write(cleaned)

        st.subheader("📝 Generated Headlines")
        for i, h in enumerate(headlines, 1):
            st.markdown(f"**{i}.** {h}")
    else:
        st.warning("Please enter an article.")
