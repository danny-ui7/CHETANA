
import streamlit as st

st.set_page_config(
    page_title="CHETANA Church Media Library",
    page_icon="🎵",
    layout="wide"
)

st.title("🎵 CHETANA")
st.subheader("Church Media Library")

st.write(
    "Your collection of hymns, prayers, "
    "and church presentations."
)

st.divider()

search = st.text_input(
    "Search for a hymn",
    placeholder="Type the hymn name..."
)

st.subheader("Your Media Library")

if search:
    st.info(f"Searching for: {search}")
else:
    st.write("Your hymns and presentations will appear here.")

st.divider()

st.subheader("PowerPoint Presentations")

st.write("Your church presentations will appear here.")
