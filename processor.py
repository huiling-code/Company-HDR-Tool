import streamlit as st
import numpy as np
from PIL import Image
import io
st.set_page_config(page_title="Photoshop HDR Mimic", layout="wide")

st.sidebar.title("Photoshop Controls")
# Setting default to 2.3 to match your screenshot exactly
hdr_val = st.sidebar.slider("HDR Limit", 1.0, 5.0, 2.3)

st.title("📸 Company Self-Service HDR")
st.write("Upload a photo to apply the Photoshop HDR Preset.")

uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

if uploaded_file:
    img = Image.open(uploaded_file)
    # Process
    res = enhance_image(np.array(img.convert('RGB')), hdr_val)
    
    col1, col2 = st.columns(2)
    col1.image(img, caption="Original")
    col2.image(res, caption=f"HDR Mode (Limit: +{hdr_val})")
    
    # Download
    result_pil = Image.fromarray(res)
    buf = io.BytesIO()
    result_pil.save(buf, format="PNG")
    st.download_button("Download HDR Result", buf.getvalue(), "hdr_photo.png")
