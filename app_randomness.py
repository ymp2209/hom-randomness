import os
import csv
import random
from datetime import datetime

import streamlit as st

IMAGE_DIR = "image_randomness"
RESULTS_CSV = "randomness_100_results.csv"


def list_images():
    paths = []

    for root, dirs, files in os.walk(IMAGE_DIR):
        for file in files:
            if file.lower().endswith((".jpg", ".jpeg", ".png")):
                paths.append(os.path.join(root, file))

    paths = sorted(paths)
    random.shuffle(paths)
    return paths


def init_session_state(images):
    if "image_list" not in st.session_state:
        st.session_state.image_list = images

    if "idx" not in st.session_state:
        st.session_state.idx = 0

    if "session_id" not in st.session_state:
        st.session_state.session_id = (
            f"sess_{int(datetime.utcnow().timestamp())}_{random.randint(1000, 9999)}"
        )


def save_response(session_id, image_path, random_score):
    os.makedirs(os.path.dirname(RESULTS_CSV) or ".", exist_ok=True)
    file_exists = os.path.isfile(RESULTS_CSV)

    with open(RESULTS_CSV, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow([
                "timestamp_utc",
                "session_id",
                "image_name",
                "random_score"
            ])

        writer.writerow([
            datetime.utcnow().isoformat(),
            session_id,
            os.path.basename(image_path),
            random_score
        ])


def main():
    st.title("Image Randomness Rating")

    st.write("This study is part of a Master's project.")

    images = list_images()

    if not images:
        st.error(f"No images found in folder: {IMAGE_DIR}")
        return

    if len(images) != 100:
        st.warning(f"Expected 100 images, but found {len(images)} images.")

    init_session_state(images)

    idx = st.session_state.idx

    if idx >= len(st.session_state.image_list):
        st.success("You have finished rating all images. Thank you for your participation!")
        st.stop()

    current_image = st.session_state.image_list[idx]

    st.subheader(f"Image {idx + 1} of {len(st.session_state.image_list)}")
    st.image(current_image, use_container_width=True)

    likert_options = {
        "1 - Strongly disagree": 1,
        "2 - Disagree": 2,
        "3 - Neutral": 3,
        "4 - Agree": 4,
        "5 - Strongly agree": 5,
    }

    random_choice = st.radio(
        "The content in this image is random.",
        options=list(likert_options.keys()),
        index=2,
        key=f"random_{idx}",
    )

    if st.button("Submit and show next image"):
        random_score = likert_options[random_choice]

        save_response(
            session_id=st.session_state.session_id,
            image_path=current_image,
            random_score=random_score,
        )

        st.session_state.idx += 1
        st.rerun()


if __name__ == "__main__":
    main()

# =========================
# ADMIN SIDEBAR
# =========================

st.sidebar.title("Admin Panel")

admin_password = st.sidebar.text_input(
    "Enter admin password",
    type="password"
)

# Change this password
ADMIN_PASSWORD = "Yash1234"

if admin_password == ADMIN_PASSWORD:

    st.sidebar.success("Access granted")

    if os.path.exists(RESULTS_CSV):

        with open(RESULTS_CSV, "rb") as file:
            st.sidebar.download_button(
                label="Download CSV Results",
                data=file,
                file_name=RESULTS_CSV,
                mime="text/csv"
            )

    else:
        st.sidebar.warning("CSV file not found yet.")