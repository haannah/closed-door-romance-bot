import streamlit as st
import pandas as pd

# Load book data
@st.cache_data
def load_books():
    return pd.read_csv("romance_database_cleaned.csv")

# Background style
st.markdown(
    """
    <style>
    html, body, .stApp {
        height: 100%;
        width: 100%;
        margin: 0;
        padding: 0;
        background-image: url("https://i.imgur.com/X78yb8n.jpeg");
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center center;
        background-attachment: fixed;
        font-family: 'sans-serif';
    }

    /* Make all content stand out with white background */
    .block-container {
        background-color: rgba(255, 255, 255, 0.92);
        padding: 2rem 2rem;
        border-radius: 1.25rem;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        margin-top: 2rem;
    }

    .main .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }

    /* Optional: Full-width layout override */
    .css-18ni7ap.e8zbici2 {
        max-width: 100%;
    }

    /* Optional: Style the page title text */
    .stApp h1 {
        font-size: 3em;
        color: #222;
        background-color: rgba(255, 255, 255, 0.9);
        padding: 1rem 1.5rem;
        border-radius: 1rem;
        text-align: center;
        box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
    }
    </style>
    """,
    unsafe_allow_html=True
)






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
