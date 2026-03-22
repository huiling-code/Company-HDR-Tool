import streamlit as st
import numpy as np
from PIL import Image
import io
from processor import enhance_image # This line must match the 'def' above!

st.set_page_config(page_title="Company HDR Tool", layout="wide")
st.sidebar.title("Photoshop Controls")
hdr_val = st.sidebar.slider("HDR Limit", 1.0, 5.0, 2.3)

st.title("📸 Company Self-Service HDR")
uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

if uploaded_file:
    img = Image.open(uploaded_file)
    # This sends the image and the slider value to the brain
    res = enhance_image(np.array(img.convert('RGB')), hdr_val)
    
    col1, col2 = st.columns(2)
    col1.image(img, caption="Original")
    col2.image(res, caption=f"HDR Mode (Limit: +{hdr_val})")
    
    result_pil = Image.fromarray(res)
    buf = io.BytesIO()
    result_pil.save(buf, format="PNG")
    st.download_button("Download HDR Result", buf.getvalue(), "hdr_photo.png")