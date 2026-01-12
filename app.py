import streamlit as st
import nltk
import json
import pandas as pd
import os
from nltk.tokenize import sent_tokenize
from openai import OpenAI

# -------------------------------
# One-time NLTK setup
# -------------------------------
nltk.download("punkt", quiet=True)

# -------------------------------
# OpenAI Client (KEEP KEY SAFE)
# -------------------------------
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# -------------------------------
# Streamlit UI
# -------------------------------
st.set_page_config(page_title="English → Marathi Science Helper", layout="wide")

st.title("📘 English → Marathi Science Helper")
st.caption("Designed for school children • Clear • Simple • Recall-friendly")

text = st.text_area(
    "📋 Paste English science text here:",
    height=220,
    placeholder="Paste one or more sentences from a science book..."
)

# -------------------------------
# Button Logic
# -------------------------------
if st.button("✨ Generate Learning Table") and text.strip():

    with st.spinner("Thinking like a teacher… ✍️"):
        sentences = sent_tokenize(text)

        results = []

        for sentence in sentences:
            prompt = f"""
You are an expert school teacher and Marathi language specialist.

For the given English sentence:
- Translate accurately into Marathi (textbook quality)
- Explain the idea in very simple Marathi so a child can easily understand and remember

Rules for Simple Marathi:
- Max 2 short sentences
- Use only easy Marathi
- No English words
- Explain the concept, not word-by-word
- Sound like a teacher explaining in class

Return ONLY valid JSON in this format:

{{
  "english": "{sentence}",
  "direct_marathi": "",
  "simple_marathi": ""
}}
"""

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2
            )

            content = response.choices[0].message.content.strip()

            try:
                parsed = json.loads(content)
                results.append(parsed)
            except json.JSONDecodeError:
                st.error("⚠️ Parsing error for a sentence. Please retry.")
                continue

    # -------------------------------
    # Convert to DataFrame
    # -------------------------------
    df = pd.DataFrame(results)
    df.columns = [
        "English Sentence",
        "Direct Marathi Meaning",
        "Simple Marathi Meaning"
    ]

    # -------------------------------
    # Display Table (Clean & Wide)
    # -------------------------------
    st.subheader("📊 Learning Table")

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    # -------------------------------
    # Student-Friendly Explanation View
    # -------------------------------
    st.subheader("🧠 Easy Explanation (For Students)")

    for _, row in df.iterrows():
        st.markdown(
            f"""
### 🔹 English Sentence
{row['English Sentence']}

📘 **Direct Marathi Meaning:**  
{row['Direct Marathi Meaning']}

🟢 **Easy Marathi (Teacher Explanation):**  
{row['Simple Marathi Meaning']}

---
"""
        )

    st.success("✅ Done! This is classroom-ready content.")
