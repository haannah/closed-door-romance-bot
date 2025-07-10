import streamlit as st
import pandas as pd

# Load book data
@st.cache_data
def load_books():
    return pd.read_csv("Closed_Door_Romance_Tropes_Updated.csv")


st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://imgur.com/a/bUKTm6G");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    </style>
    """,
    unsafe_allow_html=True
)

df = load_books()

# App layout
st.set_page_config(page_title="Find your next Closed-Door Romance Book", layout="centered")
st.title("💖 Find your next Closed-Door Romance Book")
st.write("Type in the tropes or vibes you're in the mood for! (e.g. `slowburn`, `enemies to more`, `second chance`)")

# User input
user_input = st.text_input("What are you looking for?")

# Recommendation logic
if user_input:
    keywords = [kw.strip().lower() for kw in user_input.split(",")]
    matches = df[df["Tropes"].str.lower().apply(lambda x: any(k in x for k in keywords))]

    if not matches.empty:
        st.subheader("📚 Recommended for you:")
        for _, row in matches.head(5).iterrows():
            st.markdown(f"### {row['Title']} by {row['Author']}")
            if "Image" in df.columns and pd.notna(row["Image"]):
                st.image(row["Image"], width=150)
            st.markdown(f"_Tropes:_ {row['Tropes']}")
            if "Description" in df.columns and pd.notna(row["Description"]) and row["Description"]:
                st.markdown(f"**{row['Description']}**")
            st.markdown("---")
    else:
        st.warning("😔 No matches found. Try simpler or different keywords.")
else:
    st.info("💡 Start by typing a trope like 'friends to lovers' or 'grumpy sunshine'.")
