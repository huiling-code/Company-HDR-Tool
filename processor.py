import cv2
import numpy as np

def enhance_image(image_np, hdr_power):
    # 1. Convert to float32 for high-end processing
    img = image_np.astype(np.float32) / 255.0
    img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    # 2. THE "DARKER" ADJUSTMENT (Shadow Compression)
    # We use a 'Power' higher than 1.0 to push midtones into the shadows
    # This makes the overall image feel darker and more 'moody'
    img_dark = np.power(img_bgr, 1.5) 

    # 3. HDR Tone Mapping (Mantiuk)
    # We keep the scale high so we don't lose the detail in the shirt/hair
    tonemap = cv2.createTonemapMantiuk(gamma=1.0, scale=hdr_power * 0.5, saturation=1.1)
    img_hdr = tonemap.process(img_dark)

    # 4. SELECTIVE GLOW (The "Drama" Effect)
    # We only let the very brightest spots (like catchlights in eyes) glow
    glow_mask = np.where(img_hdr > 0.8, img_hdr, 0).astype(np.float32)
    glow_layer = cv2.GaussianBlur(glow_mask, (31, 31), 0)
    img_final = cv2.addWeighted(img_hdr, 1.0, glow_layer, 0.3, 0)

    # 5. FINAL SHADOW PUSH (Photoshop 'Blacks' Slider)
    # This ensures the background stays dark and the image isn't 'muddy'
    img_8bit = np.clip(img_final * 255, 0, 255).astype(np.uint8)
    
    # Increase Contrast (alpha) and Decrease Brightness (beta)
    # alpha=1.3 makes it punchy, beta=-20 makes it darker
    img_8bit = cv2.convertScaleAbs(img_8bit, alpha=1.3, beta=-20)

    # 6. Smooth the skin but keep the shirt sharp
    img_8bit = cv2.bilateralFilter(img_8bit, 7, 50, 50)

    return cv2.cvtColor(img_8bit, cv2.COLOR_BGR2RGB)
