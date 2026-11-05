import streamlit as st
from pathlib import Path

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="CHETANA Church Media Library",
    page_icon="🎵",
    layout="wide"
)

st.title("🎵 CHETANA")
st.subheader("Church Media Library")

# --------------------------------------------------
# FOLDER CONFIGURATION
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

HYMNS = BASE_DIR / "assets" / "hymns"
PRESENTATIONS = BASE_DIR / "assets" / "presentations"

HYMNS.mkdir(parents=True, exist_ok=True)
PRESENTATIONS.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------
# FILE UPLOAD
# --------------------------------------------------

st.header("Upload Church Media")

media_type = st.selectbox(
    "Select file type",
    ["Audio Hymn", "PowerPoint Presentation"]
)

if media_type == "Audio Hymn":
    allowed_types = ["mp3", "wav", "m4a"]
    upload_folder = HYMNS
else:
    allowed_types = ["pptx", "ppt"]
    upload_folder = PRESENTATIONS

uploaded_file = st.file_uploader(
    "Choose a file",
    type=allowed_types
)

if uploaded_file is not None:

    file_path = upload_folder / Path(uploaded_file.name).name

    if file_path.exists():
        st.warning("This file already exists.")
    else:
        with open(file_path, "wb") as file:
            file.write(uploaded_file.getbuffer())

        st.success(f"Uploaded successfully: {uploaded_file.name}")

# --------------------------------------------------
# DISPLAY AUDIO HYMNS
# --------------------------------------------------

st.header("🎵 Your Hymns")

hymn_files = sorted(
    [f for f in HYMNS.iterdir() if f.is_file()],
    key=lambda f: f.name.lower()
)

if not hymn_files:
    st.info("No audio hymns uploaded yet.")

for hymn in hymn_files:

    st.write(f"**{hymn.stem}**")

    if hymn.suffix.lower() in [".mp3", ".wav", ".m4a"]:
        st.audio(str(hymn))

# --------------------------------------------------
# DISPLAY POWERPOINT PRESENTATIONS
# --------------------------------------------------

st.header("📂 Your Presentations")

presentation_files = sorted(
    [
        f for f in PRESENTATIONS.iterdir()
        if f.is_file()
        and f.suffix.lower() in [".pptx", ".ppt"]
    ],
    key=lambda f: f.name.lower()
)

if not presentation_files:
    st.info("No presentations uploaded yet.")

for presentation in presentation_files:

    st.write(f"**{presentation.name}**")

    with open(presentation, "rb") as file:
        st.download_button(
            label=f"Download {presentation.name}",
            data=file.read(),
            file_name=presentation.name,
            mime=(
                "application/vnd.openxmlformats-officedocument."
                "presentationml.presentation"
                if presentation.suffix.lower() == ".pptx"
                else "application/vnd.ms-powerpoint"
            ),
            key=f"download_{presentation.name}"
        )
