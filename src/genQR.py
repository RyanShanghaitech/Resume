# pip install qrcode[pil] pillow

import os
import qrcode
from PIL import Image, ImageDraw

tasks = [
    {
        "website_url": "https://scholar.google.com/citations?user=llTqHTUAAAAJ&hl=en",
        "logo_path": "resource/scholar.png",
        "output_path": "qr/scholar.png",
    },
    {
        "website_url": "https://pypi.org/user/ryan_shanghaitech",
        "logo_path": "resource/pypi.png",
        "output_path": "qr/pypi.png",
    },
    {
        "website_url": "https://github.com/RyanShanghaitech",
        "logo_path": "resource/github.png",
        "output_path": "qr/github.png",
    },
]

for item in tasks:
    website_url = item["website_url"]
    logo_path = item["logo_path"]
    output_path = item["output_path"]

    # Ensure output folder exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Create QR code (high error correction for center logo)
    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4
    )
    qr.add_data(website_url)
    qr.make(fit=True)

    qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGBA")
    qr_w, qr_h = qr_img.size

    # Logo background (white rounded rectangle)
    bg_size = qr_w // 6                  # background size relative to QR
    radius = bg_size // 5                # rounded corner radius
    padding = bg_size // 8               # inner padding for logo

    badge = Image.new("RGBA", (bg_size, bg_size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(badge)
    draw.rounded_rectangle(
        [(0, 0), (bg_size - 1, bg_size - 1)],
        radius=radius,
        fill=(255, 255, 255, 255)
    )

    # Open logo and fit into badge area (keep aspect ratio)
    logo = Image.open(logo_path).convert("RGBA")
    max_logo_size = bg_size - 2 * padding
    logo.thumbnail((max_logo_size, max_logo_size), Image.LANCZOS)

    lx = (bg_size - logo.width) // 2
    ly = (bg_size - logo.height) // 2
    badge.paste(logo, (lx, ly), logo)

    # Paste badge at QR center
    x = (qr_w - bg_size) // 2
    y = (qr_h - bg_size) // 2
    qr_img.paste(badge, (x, y), badge)

    # Save
    qr_img.convert("RGB").save(output_path)
    print(f"Saved: {output_path}")