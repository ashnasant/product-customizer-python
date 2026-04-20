import cv2
import numpy as np

def apply_logo(product_path, output_name, x, y, w=250, h=280, color="white"):
    product = cv2.imread(product_path)
    design = cv2.imread("logo.png")

    if product is None or design is None:
        print(f"Error loading {product_path}")
        return

    # Resize logo
    design = cv2.resize(design, (w, h))

    # Create mask
    gray = cv2.cvtColor(design, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)
    mask_inv = cv2.bitwise_not(mask)

    # 🎯 COLOR CONTROL
    if color == "white":
        logo_colored = np.ones_like(design) * 255   # pure white
    else:
        logo_colored = np.zeros_like(design) + 30   # black/dark

    h, w = design.shape[:2]

    # Safe bounds
    y_end = min(y + h, product.shape[0])
    x_end = min(x + w, product.shape[1])

    roi = product[y:y_end, x:x_end]

    # Resize safely
    mask = cv2.resize(mask, (roi.shape[1], roi.shape[0]))
    mask_inv = cv2.resize(mask_inv, (roi.shape[1], roi.shape[0]))
    logo_colored = cv2.resize(logo_colored, (roi.shape[1], roi.shape[0]))

    # Blend
    bg = cv2.bitwise_and(roi, roi, mask=mask_inv)
    fg = cv2.bitwise_and(logo_colored, logo_colored, mask=mask)

    result = cv2.addWeighted(bg, 1, fg, 0.8, 0)

    product[y:y_end, x:x_end] = result

    cv2.imwrite(output_name, product)
    print(f"{output_name} created")


# 🎯 APPLY TO ALL PRODUCTS (UNCHANGED POSITIONS)

# Hoodie (WHITE)
apply_logo("hoodie_front.jpg", "hoodie_front_out.jpg", 650, 700, color="white")
apply_logo("hoodie_back.jpg", "hoodie_back_out.jpg", 760, 1000, color="white")

# T-shirt (WHITE)
apply_logo("tshirt.jpg", "tshirt_out.jpg", 560, 700, color="white")

# Cap FRONT (BLACK)
apply_logo("cap_front.jpg", "cap_front_out.jpg", 400, 600, 120, 80, color="black")

# Cap BACK (WHITE)
apply_logo("cap_back.jpg", "cap_back_out.jpg", 190, 310, 120, 80, color="white")