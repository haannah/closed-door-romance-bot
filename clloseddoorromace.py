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
    html, body, .stApp {
        height: 100%;
        width: 100%;
        margin: 0;
        padding: 0;
        background-image: url"https://i.imgur.com/2jg9Htu.jpeg"); /* Replace with your image */
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center center;
        background-attachment: fixed;
    }

    .block-container {
        padding-top: 3rem;
        padding-bottom: 3rem;
        background-color: rgba(255, 255, 255, 0.0); /* transparent background */
    }

    /* Remove padding around main container */
    .main .block-container {
        padding-left: 0rem;
        padding-right: 0rem;
    }

    /* Prevent layout constraints */
    .css-18ni7ap.e8zbici2 {
        max-width: 100%;
    }
    </style>
    """,
    unsafe_allow_html=True
)

from PIL import Image
import streamlit as st

image = Image.open("Add a heading.jpg")
st.image(image, caption=" ", use_container_width=True)




df = load_books()

# App layout
st.set_page_config(page_title="Find your next Closed-Door Romance Book", layout="centered")
st.title("Find your next Closed-Door Romance Book")

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
