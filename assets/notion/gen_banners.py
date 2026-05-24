#!/usr/bin/env python3
"""Generate on-brand abstract gradient banner PNGs for Notion page covers.

Brand palette: Navy #0B1F3A (primary) - Teal #1C6E71 (secondary) - Gold #D4AF37 (accent).
Pure stdlib (zlib + struct + binascii) so it runs anywhere.
Wide banners (1600x640) with a smooth diagonal navy->teal base and a radial
gold glow. Smoothness means any Notion crop (desktop wide band or mobile
square-ish) looks centered and intentional.
"""
import zlib, struct, binascii, math

W, H = 1600, 640

def lerp(a, b, t):
    return a + (b - a) * t

def mix(c1, c2, t):
    return tuple(lerp(c1[i], c2[i], t) for i in range(3))

def clamp(v):
    return max(0, min(255, int(round(v))))

# Brand colors
NAVY      = (11, 31, 58)     # #0B1F3A
NAVY_DEEP = (6, 16, 33)      # #061021
TEAL      = (28, 110, 113)   # #1C6E71
GOLD      = (212, 175, 55)   # #D4AF37

def build(path, base_stops, glow_x, glow_y, glow_r, glow_intensity, glow_color=GOLD, darken=1.0):
    """base_stops: list of (pos0..1, rgb) for the diagonal base gradient.
    glow_*: radial accent glow (screen-blended) positioned at fractional coords."""
    def base_at(t):
        # find surrounding stops
        for i in range(len(base_stops) - 1):
            p0, c0 = base_stops[i]
            p1, c1 = base_stops[i + 1]
            if p0 <= t <= p1:
                local = (t - p0) / (p1 - p0) if p1 > p0 else 0
                return mix(c0, c1, local)
        return base_stops[-1][1]

    gx, gy = glow_x * W, glow_y * H
    raw = bytearray()
    for y in range(H):
        raw.append(0)  # filter type 0 (None) per scanline
        for x in range(W):
            # diagonal parameter: mostly horizontal, slight vertical tilt
            t = (x / W) * 0.82 + (y / H) * 0.18
            r, g, b = base_at(t)
            # radial gold glow, screen blend for a soft luminous accent
            d = math.hypot(x - gx, y - gy)
            gi = max(0.0, 1.0 - d / glow_r) ** 2 * glow_intensity
            r = 255 - (255 - r) * (1 - gi * glow_color[0] / 255)
            g = 255 - (255 - g) * (1 - gi * glow_color[1] / 255)
            b = 255 - (255 - b) * (1 - gi * glow_color[2] / 255)
            # subtle vignette toward edges keeps text legible
            vy = abs((y / H) - 0.5) * 2
            vig = 1.0 - 0.12 * (vy ** 2)
            r *= vig * darken; g *= vig * darken; b *= vig * darken
            raw += bytes((clamp(r), clamp(g), clamp(b)))

    def chunk(typ, data):
        c = typ + data
        return struct.pack(">I", len(data)) + c + struct.pack(">I", binascii.crc32(c) & 0xffffffff)

    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0))  # 8-bit RGB
    png += chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    png += chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(png)
    print(f"wrote {path} ({len(png)} bytes)")

# Shared cool base: deep navy -> navy -> teal -> deep navy (dark, smooth)
BASE = [(0.0, NAVY_DEEP), (0.30, NAVY), (0.62, TEAL), (1.0, NAVY_DEEP)]
BASE_TEAL = [(0.0, NAVY_DEEP), (0.25, NAVY), (0.55, TEAL), (0.80, TEAL), (1.0, NAVY)]
BASE_GOLD = [(0.0, NAVY_DEEP), (0.35, NAVY), (0.70, TEAL), (1.0, NAVY)]

# Home: balanced, gold glow center-right
build("home.png",    BASE,      0.72, 0.55, 760, 0.55)
# Sales: gold-forward (money), strong glow far right
build("sales.png",   BASE_GOLD, 0.86, 0.50, 820, 0.72)
# Podcast: teal-dominant, soft gold glow left
build("podcast.png", BASE_TEAL, 0.18, 0.45, 720, 0.42)
# Brand: balanced with a centered gold glow
build("brand.png",   BASE,      0.50, 0.48, 700, 0.60)
