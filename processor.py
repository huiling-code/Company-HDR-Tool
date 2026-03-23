import cv2
import numpy as np

def enhance_image(image_np, hdr_power):
    # 1. Setup - Convert to float for light math
    img = image_np.astype(np.float32) / 255.0
    img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    # 2. High-Key Exposure Boost
    # Pushes whites up to create that 'studio light' feel
    boost = hdr_power * 0.4
    img_res = np.power(img_bgr, 1.0 / (1.0 + boost))
    
    # 3. Convert to 8-bit for detail work
    img_8bit = np.clip(img_res * 255, 0, 255).astype(np.uint8)

    # 4. Local Contrast (The 'HDR Detail' step)
    # This recovers the texture in the skin and hair
    lab = cv2.cvtColor(img_8bit, cv2.COLOR_BGR2Lab)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    l = clahe.apply(l)
    img_final = cv2.cvtColor(cv2.merge((l, a, b)), cv2.COLOR_Lab2BGR)

    # 5. Background Clean-up
    # Forces almost-white pixels to be PURE white for a clean look
    gray = cv2.cvtColor(img_final, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray, 245, 255, cv2.THRESH_BINARY)
    img_final[mask > 0] = [255, 255, 255]

    # 6. Smooth skin slightly
    img_final = cv2.bilateralFilter(img_final, 7, 50, 50)

    return cv2.cvtColor(img_final, cv2.COLOR_BGR2RGB)
