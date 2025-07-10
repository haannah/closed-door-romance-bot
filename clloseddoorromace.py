import streamlit as st
import pandas as pd

# Load book data
@st.cache_data
def load_books():
    return pd.read_csv("Closed_Door_Romance_Tropes_Updated.csv")

# Background style
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://imgur.com/a/fppnOxb");  /* Cozy books example */
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center center;
        background-attachment: fixed;
        height: 100vh;
        width: 100vw;
    }
    </style>
    """,
    unsafe_allow_html=True
)
from PIL import Image
import streamlit as st

image = Image.open("ENEMIES TO LOVERS.jpg")
st.image(image, caption="Popular Romance Tropes", use_column_width=True)


df = load_books()

# App layout
st.set_page_config(page_title="Find your next Closed-Door Romance Book", layout="centered")
st.title("💖 Find your next Closed-Door Romance Book")

# Toggle between search types
search_type = st.radio("Search by:", ["Tropes", "Author"])
placeholder_text = "e.g. slowburn, enemies to more" if search_type == "Tropes" else "e.g. Jenny Proctor, Emma St. Clair"
user_input = st.text_input(f"What {search_type.lower()} are you looking for?", placeholder=placeholder_text)

# Recommendation logic
if user_input:
    user_input = user_input.strip().lower()

    if search_type == "Tropes":
        keywords = [kw.strip() for kw in user_input.split(",")]
        matches = df[df["Tropes"].str.lower().apply(lambda x: any(k in x for k in keywords))]
    else:
        matches = df[df["Author"].str.lower().str.contains(user_input)]

    if not matches.empty:
        st.subheader("📚 Recommended for you:")
        for _, row in matches.iterrows():
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
    st.info(f"💡 Start by typing a {search_type.lower()} to explore clean romance recs.")
