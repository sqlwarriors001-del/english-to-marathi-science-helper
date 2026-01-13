import streamlit as st
import os
import re
import pandas as pd
from openai import OpenAI

# ---------------------------
# CONFIG
# ---------------------------
st.set_page_config(
    page_title="English → Marathi Science Helper",
    page_icon="📘",
    layout="wide"
)

# ---------------------------
# OPENAI CLIENT
# ---------------------------
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ---------------------------
# SAFE SENTENCE SPLITTER
# ---------------------------
def split_sentences(text):
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    return [s.strip() for s in sentences if s.strip()]

# ---------------------------
# UI
# ---------------------------
st.title("📘 English → Marathi Science Helper")
st.write(
    "Paste English science text below. "
    "You will get **direct Marathi meaning** and an **easy explanation for children**."
)

text = st.text_area(
    "📋 Paste English science text here:",
    height=200,
    placeholder="Example:\nMatter is anything that occupies space.\nIt has mass."
)

# ---------------------------
# PROCESS
# ---------------------------
if st.button("✨ Generate Learning Table") and text.strip():

    with st.spinner("Generating explanations… please wait ⏳"):
        sentences = split_sentences(text)

        results = []

        for sentence in sentences:
            prompt = f"""
You are a teaching assistant for school children.

For the given English sentence, return:
1) Direct Marathi translation (accurate, textbook style)
2) Simple Marathi explanation that:
   - uses very easy words
   - explains the idea clearly
   - helps children remember the concept
   - sounds like a teacher explaining orally
   - maximum 2 short sentences
   - no English words

Return ONLY valid JSON in this exact format:

{{
  "english": "",
  "direct_marathi": "",
  "simple_marathi": ""
}}

English sentence:
\"\"\"{sentence}\"\"\"
"""

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2
            )

            data = response.choices[0].message.content

            try:
                parsed = eval(data)
                results.append(parsed)
            except:
                continue

        # ---------------------------
        # TABLE VIEW (Teacher)
        # ---------------------------
        df = pd.DataFrame(results)
        df.columns = [
            "English Sentence",
            "Direct Marathi Meaning",
            "Simple Marathi Meaning"
        ]

        st.subheader("📊 Learning Table")
        st.dataframe(df, use_container_width=True, hide_index=True)

        # ---------------------------
        # STUDENT FRIENDLY VIEW
        # ---------------------------
        st.subheader("🧠 Easy Explanation (Student Friendly)")

        for _, row in df.iterrows():
            st.markdown(
                f"""
**🔹 English Sentence**  
{row['English Sentence']}

📘 **Direct Marathi Meaning**  
{row['Direct Marathi Meaning']}

🟢 **Easy Marathi Explanation**  
{row['Simple Marathi Meaning']}

---
"""
            )

# ---------------------------
# FOOTER
# ---------------------------
st.markdown(
    "<small>Built to help students learn and understand concepts easily. "
    "This tool supports learning and does not replace teachers.</small>",
    unsafe_allow_html=True
)
