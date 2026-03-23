import streamlit as st
import numpy as np
from PIL import Image
import io
from processor import enhance_image 

st.set_page_config(page_title="Company HDR Tool")
hdr_val = st.sidebar.slider("HDR Intensity", 1.0, 5.0, 2.3)

st.title("📸 Company HDR Tool")
file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

if file:
    img = Image.open(file)
    res = enhance_image(np.array(img.convert('RGB')), hdr_val)
    st.image(res, caption="HDR Result")
    
    buf = io.BytesIO()
    Image.fromarray(res).save(buf, format="PNG")
    st.download_button("Download", buf.getvalue(), "hdr_photo.png")
