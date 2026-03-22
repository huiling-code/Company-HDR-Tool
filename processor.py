import cv2
import numpy as np

def enhance_image(image_np, hdr_power):
    # 1. Convert to float32 for high-end light math
    img = image_np.astype(np.float32) / 255.0
    img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    # 2. Sigmoid Light Curve (The "Photoshop Secret")
    # This stretches the light at the top end to create that 'glowing white'
    # without making the face look like it's on fire.
    k = hdr_power * 2.0
    img_sigmoid = 1 / (1 + np.exp(-k * (img_bgr - 0.5)))

    # 3. Create the "Wrap-Around" Glow
    # We blur the brightest parts to let them 'bleed' into the hair and shoulders
    glow_mask = np.clip(img_sigmoid * 1.5, 0, 1)
    glow = cv2.GaussianBlur(glow_mask, (75, 75), 0)
    
    # 4. Mix the layers (Like 'Soft Light' blend mode in PS)
    img_final = cv2.addWeighted(img_sigmoid, 0.7, glow, 0.4, 0)

    # 5. Tone Mapping (Mantiuk) to keep detail in the shirt
    tonemap = cv2.createTonemapMantiuk(gamma=1.0, scale=0.7, saturation=1.2)
    img_final = tonemap.process(img_final)

    # 6. Final Polish
    img_8bit = np.clip(img_final * 255, 0, 255).astype(np.uint8)
    
    # Bilateral filter makes the skin look 'retouched' but keeps eyes sharp
    img_8bit = cv2.bilateralFilter(img_8bit, 9, 75, 75)

    return cv2.cvtColor(img_8bit, cv2.COLOR_BGR2RGB)