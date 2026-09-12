#!/usr/bin/env python3
"""Generate Dream Journal launcher icons."""
import math
from PIL import Image, ImageDraw, ImageFilter

def make_icon(size, rounded=True):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Gradient background (purple to pink)
    bg = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    bgdraw = ImageDraw.Draw(bg)
    for y in range(size):
        t = y / size
        r = int(124 + (236 - 124) * t)
        g = int(58 + (72 - 58) * t)
        b = int(211 + (153 - 211) * t)
        bgdraw.line([(0, y), (size, y)], fill=(r, g, b, 255))

    # Apply rounded corners mask
    if rounded:
        mask = Image.new("L", (size, size), 0)
        mdraw = ImageDraw.Draw(mask)
        radius = int(size * 0.22)
        mdraw.rounded_rectangle([(0, 0), (size, size)], radius=radius, fill=255)
        bg.putalpha(mask)

    img.paste(bg, (0, 0), bg)

    # Draw crescent moon in center
    cx, cy = size / 2, size / 2
    moon_r = size * 0.28
    # outer moon circle (light)
    outer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    odraw = ImageDraw.Draw(outer)
    odraw.ellipse([cx - moon_r, cy - moon_r, cx + moon_r, cy + moon_r],
                  fill=(255, 255, 255, 245))
    # inner offset circle to carve crescent (background color)
    offset = moon_r * 0.38
    inner_bg = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    idraw = ImageDraw.Draw(inner_bg)
    idraw.ellipse([cx - moon_r + offset, cy - moon_r - offset,
                   cx + moon_r + offset, cy + moon_r - offset],
                  fill=(168, 85, 247, 255))  # match bg gradient mid
    outer.paste(inner_bg, (0, 0), inner_bg)
    # small star
    star_x, star_y = cx + moon_r * 0.9, cy - moon_r * 0.8
    star_r = size * 0.04
    sdraw = ImageDraw.Draw(outer)
    sdraw.ellipse([star_x - star_r, star_y - star_r, star_x + star_r, star_y + star_r],
                  fill=(255, 255, 255, 230))

    # Soft glow for moon
    glow = outer.filter(ImageFilter.GaussianBlur(radius=size * 0.015))
    img = Image.alpha_composite(img, glow)
    img = Image.alpha_composite(img, outer)
    return img

densities = {
    "mipmap-mdpi": 48,
    "mipmap-hdpi": 72,
    "mipmap-xhdpi": 96,
    "mipmap-xxhdpi": 144,
    "mipmap-xxxhdpi": 192,
}

base = "/workspace/android/app/src/main/res"
for folder, size in densities.items():
    icon = make_icon(size, rounded=True)
    icon.save(f"{base}/{folder}/ic_launcher.png")
    round_icon = make_icon(size, rounded=True)
    round_icon.save(f"{base}/{folder}/ic_launcher_round.png")
    print(f"{folder}: {size}x{size} done")

print("All icons generated.")
