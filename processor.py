import cv2
import numpy as np

def enhance_image(image_np, hdr_power):
    img = image_np.astype(np.float32) / 255.0
    img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    
    # High-Key Studio math
    boost = hdr_power * 0.5
    img_res = np.power(img_bgr, 1.0 / (1.0 + boost))
    img_8bit = np.clip(img_res * 255, 0, 255).astype(np.uint8)
    
    # Local contrast pop
    lab = cv2.cvtColor(img_8bit, cv2.COLOR_BGR2Lab)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    l = clahe.apply(l)
    img_final = cv2.cvtColor(cv2.merge((l, a, b)), cv2.COLOR_Lab2BGR)

    return cv2.cvtColor(img_final, cv2.COLOR_BGR2RGB)
