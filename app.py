import streamlit as st
import numpy as np
from PIL import Image
import io
from processor import enhance_image

# 1. Page Configuration
st.set_page_config(page_title="Photoshop HDR Mimic", layout="wide")

st.sidebar.title("Photoshop Controls")
# Default set to 2.3 to match your original Photoshop 'HDR Limit'
hdr_val = st.sidebar.slider("HDR Limit", 1.0, 5.0, 2.3)

st.title("📸 Company Self-Service HDR")
st.write("Upload a photo to apply the Photoshop HDR Preset.")

uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

if uploaded_file:
    # Load Image
    img = Image.open(uploaded_file)
    img_array = np.array(img.convert('RGB'))
    
    # 2. Process Image (Sends data to processor.py)
    with st.spinner("Applying Studio Lighting..."):
        res = enhance_image(img_array, hdr_val)
    
    # 3. Side-by-Side Display
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Original")
        st.image(img, use_container_width=True)
    
    with col2:
        st.subheader(f"HDR Result (+{hdr_val})")
        st.image(res, use_container_width=True)
        
        # 4. Download Logic
        result_pil = Image.fromarray(res)
        buf = io.BytesIO()
        result_pil.save(buf, format="PNG")
        st.download_button(
            label="Download HDR Result", 
            data=buf.getvalue(), 
            file_name="hdr_photo.png", 
            mime="image/png"
        )
