import streamlit as st
from pathlib import Path

# ==========================================
# CHETANA - KANNADA CHURCH MEDIA LIBRARY
# ==========================================

st.set_page_config(
    page_title="CHETANA | Kannada Catholic Hymns",
    page_icon="🎵",
    layout="wide"
)

BASE = Path(__file__).resolve().parent
ASSETS = BASE / "assets"
HYMNS = ASSETS / "hymns"
PRESENTATIONS = ASSETS / "presentations"

CATEGORIES = [
    "ಪ್ರವೇಶ ಗೀತೆಗಳು (Entrance Hymns)",
    "ದಯಾ ಬೇಡಿಕೆ (Lord have Mercy)",
    "ಮಹೋನ್ನತ ಗೀತೆಗಳು (Glory Hymns)",
    "ವಾಚನಾಂತರ ಗೀತೆಗಳು (Reading Hymns)",
    "ಅಲ್ಲೇಲೂಯ (Alleluia)",
    "ಅರ್ಪಣಾ ಗೀತೆಗಳು (Offering Hymns)",
    "ಪರಿಶುದ್ಧರು (Holy holy)",
    "ವಿಶ್ವಾಸ ಘೋಷಣೆ (Mystery of Faith)",
    "ಕ್ಷಮಾ ಯಾಚನೆ (Lamb of God)",
    "ಪರಮ ಪ್ರಸಾದ ಗೀತೆಗಳು (Communion Hymns)",
    "ಪೂಜಾಂತ್ಯ ಗೀತೆಗಳು (Recessional Hymns)",
    "Adoration",
    "Mother Mary",
    "Saints",
    "Praise and Worship",
    "Sunday Psalms",
    "Christmas",
    "Easter",
    "Other Hymns",
    "Holy Mass"
]

for folder in [HYMNS, PRESENTATIONS]:
    folder.mkdir(parents=True, exist_ok=True)

for category in CATEGORIES:
    (HYMNS / category).mkdir(exist_ok=True)
    (PRESENTATIONS / category).mkdir(exist_ok=True)

if "favorites" not in st.session_state:
    st.session_state.favorites = set()

if "pending_delete" not in st.session_state:
    st.session_state.pending_delete = None

if "delete_notice" not in st.session_state:
    st.session_state.delete_notice = None

# ==========================================
# CUSTOM DESIGN
# ==========================================

st.markdown("""
<style>
.stApp {
    background-color: #f7f8f5;
}
.main-title {
    color: #174c3c;
    font-size: 38px;
    font-weight: 800;
}
.subtitle {
    color: #68766e;
    font-size: 15px;
}
div.stButton > button {
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="main-title">♫ CHETANA</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Kannada Catholic Hymns & Church Media Library</div>',
    unsafe_allow_html=True
)

st.divider()

if st.session_state.delete_notice:
    st.success(st.session_state.delete_notice)
    st.session_state.delete_notice = None

# ==========================================
# NAVIGATION
# ==========================================

page = st.sidebar.radio(
    "NAVIGATION",
    [
        "Home",
        "Hymn Library",
        "My Favourites",
        "Presentations",
        "Upload Media"
    ]
)

st.sidebar.divider()
st.sidebar.caption("CHETANA Church Media Library")

# ==========================================
# HELPER FUNCTIONS
# ==========================================

def get_hymns():
    return sorted(
        [
            f for f in HYMNS.rglob("*")
            if f.is_file()
            and f.suffix.lower() in [".mp3", ".wav", ".m4a"]
        ],
        key=lambda f: f.name.lower()
    )


def get_presentations():
    return sorted(
        [
            f for f in PRESENTATIONS.rglob("*")
            if f.is_file()
            and f.suffix.lower() in [".ppt", ".pptx"]
        ],
        key=lambda f: f.name.lower()
    )


def delete_media(file_path, media_type):
    """Delete a selected file after checking its storage location."""

    file_path = Path(file_path).resolve()

    allowed_root = (
        HYMNS.resolve()
        if media_type == "hymn"
        else PRESENTATIONS.resolve()
    )

    try:
        file_path.relative_to(allowed_root)
    except ValueError:
        st.error("This file is outside the CHETANA media folder.")
        return

    if not file_path.is_file():
        st.error("File not found. It may already have been deleted.")
        return

    file_path.unlink()

    if media_type == "hymn":
        # Delete matching Kannada lyrics and chords too.
        related_files = [
            file_path.with_suffix(".txt"),
            file_path.with_name(file_path.stem + ".chords.txt")
        ]

        for related_file in related_files:
            if related_file.is_file():
                try:
                    related_file.resolve().relative_to(allowed_root)
                    related_file.unlink()
                except ValueError:
                    pass

        st.session_state.favorites.discard(file_path.name)

    st.session_state.pending_delete = None
    st.session_state.delete_notice = (
        f"Successfully deleted: {file_path.name}"
    )
    st.rerun()


def show_delete_button(file_path, media_type):
    """Display delete and confirmation buttons."""

    file_id = str(file_path)

    if st.session_state.pending_delete == file_id:

        st.warning(
            f"Are you sure you want to permanently delete "
            f"'{file_path.name}'?"
        )

        if media_type == "hymn":
            st.caption(
                "Its matching lyrics and chords files will also be deleted."
            )

        col1, col2 = st.columns(2)

        with col1:
            if st.button(
                "Yes, Delete",
                key="confirm_" + file_id,
                type="primary",
                use_container_width=True
            ):
                delete_media(file_path, media_type)

        with col2:
            if st.button(
                "Cancel",
                key="cancel_" + file_id,
                use_container_width=True
            ):
                st.session_state.pending_delete = None
                st.rerun()

    else:
        if st.button(
            "🗑️ Delete",
            key="delete_" + file_id
        ):
            st.session_state.pending_delete = file_id
            st.rerun()


def show_hymn(hymn):

    st.markdown(f"### 🎵 {hymn.stem}")

    st.audio(
        hymn.read_bytes(),
        format="audio/" + {
            ".mp3": "mpeg",
            ".wav": "wav",
            ".m4a": "mp4"
        }.get(hymn.suffix.lower(), "mpeg")
    )

    lyrics = hymn.with_suffix(".txt")
    chords = hymn.with_name(hymn.stem + ".chords.txt")

    if lyrics.exists():
        with st.expander("📖 View Kannada Lyrics"):
            st.text(lyrics.read_text(encoding="utf-8"))

    if chords.exists():
        with st.expander("🎸 View Chords"):
            st.text(chords.read_text(encoding="utf-8"))

    if st.button(
        "❤️ Remove from Favourites"
        if hymn.name in st.session_state.favorites
        else "♡ Add to Favourites",
        key="fav_" + str(hymn)
    ):
        if hymn.name in st.session_state.favorites:
            st.session_state.favorites.remove(hymn.name)
        else:
            st.session_state.favorites.add(hymn.name)

        st.rerun()

    show_delete_button(hymn, "hymn")

    st.divider()


# ==========================================
# HOME PAGE
# ==========================================

if page == "Home":

    st.markdown("## Welcome to CHETANA")

    st.markdown("""
    Discover Kannada Catholic hymns, listen to devotional
    music and access church presentations in one place.
    """)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Audio Hymns", len(get_hymns()))

    with col2:
        st.metric("Presentations", len(get_presentations()))

    with col3:
        st.metric("Favourites", len(st.session_state.favorites))

    st.divider()

    st.subheader("Explore Hymn Categories")

    for i in range(0, len(CATEGORIES), 2):
        cols = st.columns(2)

        for j, col in enumerate(cols):
            if i + j < len(CATEGORIES):
                category = CATEGORIES[i + j]

                with col:
                    if st.button(
                        "🎵 " + category,
                        use_container_width=True
                    ):
                        st.session_state.selected_category = category
                        st.rerun()


# ==========================================
# HYMN LIBRARY
# ==========================================

elif page == "Hymn Library":

    st.header("🎵 Kannada Hymn Library")

    selected_category = st.selectbox(
        "Choose Category",
        ["All Categories"] + CATEGORIES,
        index=(
            CATEGORIES.index(st.session_state.selected_category) + 1
            if st.session_state.get("selected_category") in CATEGORIES
            else 0
        )
    )

    search = st.text_input(
        "🔍 Search Hymns",
        placeholder="Type the hymn name..."
    )

    hymns = get_hymns()

    for hymn in hymns:

        if selected_category != "All Categories":
            if hymn.parent.name != selected_category:
                continue

        if search.lower() not in hymn.stem.lower():
            continue

        show_hymn(hymn)

    if not hymns:
        st.info("No hymns uploaded yet.")


# ==========================================
# FAVOURITES
# ==========================================

elif page == "My Favourites":

    st.header("❤️ My Favourite Hymns")

    favourites = [
        h for h in get_hymns()
        if h.name in st.session_state.favorites
    ]

    if not favourites:
        st.info("You have not added any favourite hymns yet.")

    for hymn in favourites:
        show_hymn(hymn)


# ==========================================
# PRESENTATIONS
# ==========================================

elif page == "Presentations":

    st.header("📂 Church Presentations")

    search = st.text_input(
        "Search Presentations",
        placeholder="Enter presentation name..."
    )

    files = get_presentations()

    if not files:
        st.info("No presentations uploaded yet.")

    for presentation in files:

        if search.lower() not in presentation.stem.lower():
            continue

        st.markdown(f"**📄 {presentation.name}**")

        st.download_button(
            "Download Presentation",
            data=presentation.read_bytes(),
            file_name=presentation.name,
            mime=(
                "application/vnd.openxmlformats-officedocument."
                "presentationml.presentation"
                if presentation.suffix.lower() == ".pptx"
                else "application/vnd.ms-powerpoint"
            ),
            key="ppt_" + str(presentation)
        )

        show_delete_button(presentation, "presentation")

        st.divider()


# ==========================================
# UPLOAD MEDIA
# ==========================================

elif page == "Upload Media":

    st.header("📤 Upload Church Media")

    st.info(
        "Upload audio hymns, PowerPoint presentations, "
        "Kannada lyrics and chords from your phone or computer."
    )

    media_type = st.selectbox(
        "Select Media Type",
        [
            "Audio Hymn",
            "PowerPoint Presentation",
            "Kannada Lyrics",
            "Hymn Chords"
        ]
    )

    category = st.selectbox(
        "Select Category",
        CATEGORIES
    )

    if media_type == "Audio Hymn":
        folder = HYMNS / category
        allowed = ["mp3", "wav", "m4a"]

    elif media_type == "PowerPoint Presentation":
        folder = PRESENTATIONS / category
        allowed = ["ppt", "pptx"]

    else:
        folder = HYMNS / category
        allowed = ["txt"]

    uploaded = st.file_uploader(
        "Choose File",
        type=allowed
    )

    if uploaded is not None:

        original_name = Path(uploaded.name).name

        if media_type == "Hymn Chords":
            file_name = (
                Path(original_name).stem.replace(".chords", "")
                + ".chords.txt"
            )
        else:
            file_name = original_name

        destination = folder / file_name

        if st.button("Upload Now", type="primary"):

            if destination.exists():
                st.warning("This file already exists.")
            else:
                destination.write_bytes(uploaded.getbuffer())

                st.success(
                    f"Successfully uploaded: {file_name}"
                )

                st.rerun()

    st.divider()

    st.caption(
        "For lyrics, use the same filename as the audio hymn "
        "with a .txt extension. For chords, use the hymn name "
        "followed by .chords.txt."
    )


# ==========================================
# FOOTER
# ==========================================

st.divider()

st.caption(
    "CHETANA | Kannada Catholic Hymns & Church Media Library"
)
