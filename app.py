import glob
import os

import streamlit as st

st.title("CS 데이터 미니 대시보드 (배포 테스트)")

IMAGE_DIR = os.path.join("my-wiki-02", "components", "output")
image_paths = sorted(glob.glob(os.path.join(IMAGE_DIR, "*.png")))

for path in image_paths:
    st.image(path, caption=os.path.basename(path))
