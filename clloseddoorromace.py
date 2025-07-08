import streamlit as st
import pandas as pd

# Load the book database
@st.cache_data
def load_data():
    return pd.read_csv("Closed-Door_Romance_Tropes.csv")

books = load_data()

st.set_page_config(page_title="Closed-Door Romance Recommender", layout="centered")
st.title("💖 Find Your Next Closed-Door Romance")
st.write("Type in your favorite tropes or themes (e.g. 'friends to lovers', 'second chance', 'grumpy sunshine'):")

user_input = st.text_input("Enter tropes or keywords:")

if user_input:
    keywords = [kw.strip().lower() for kw in user_input.split(",") if kw.strip()]
    matches = books[books["Tropes"].str.lower().apply(lambda x: any(k in x for k in keywords))]

    if not matches.empty:
        st.subheader("📚 Recommendations")
        for _, row in matches.head(3).iterrows():
            st.markdown(f"### {row['Title']} by {row['Author']}")
            st.markdown(f"_Tropes:_ {row['Tropes']}")
            st.markdown(f"**{row['Description']}**")
            st.markdown("---")
    else:
        st.warning("No matches found. Try different or simpler tropes!")
else:
    st.info("Enter a trope to get started.")
