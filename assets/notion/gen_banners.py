#!/usr/bin/env python3
"""On-brand gradient banner PNGs for Notion covers (v2 — stronger gold).

Brand: Navy #0B1F3A - Teal #1C6E71 - Gold #D4AF37. Pure stdlib.
v2 changes: brighter, more concentrated gold glow + a hot inner core so the
accent reads clearly; six domain variants for cohesive DB covers.
"""
import zlib, struct, binascii, math

W, H = 1600, 640

def lerp(a, b, t): return a + (b - a) * t
def mix(c1, c2, t): return tuple(lerp(c1[i], c2[i], t) for i in range(3))
def clamp(v): return max(0, min(255, int(round(v))))

NAVY      = (11, 31, 58)
NAVY_DEEP = (6, 16, 33)
TEAL      = (28, 110, 113)
GOLD      = (212, 175, 55)
GOLD_HOT  = (245, 212, 110)   # lighter gold for the bright core

def build(path, base_stops, glows):
    """glows: list of dicts {x,y,r,intensity,color} screen-blended in order."""
    def base_at(t):
        for i in range(len(base_stops) - 1):
            p0, c0 = base_stops[i]; p1, c1 = base_stops[i + 1]
            if p0 <= t <= p1:
                local = (t - p0) / (p1 - p0) if p1 > p0 else 0
                return mix(c0, c1, local)
        return base_stops[-1][1]

    G = [(g["x"] * W, g["y"] * H, g["r"], g["intensity"], g["color"]) for g in glows]
    raw = bytearray()
    for y in range(H):
        raw.append(0)
        for x in range(W):
            t = (x / W) * 0.82 + (y / H) * 0.18
            r, g, b = base_at(t)
            for (gx, gy, gr, gi0, gc) in G:
                d = math.hypot(x - gx, y - gy)
                gi = max(0.0, 1.0 - d / gr) ** 2 * gi0
                r = 255 - (255 - r) * (1 - gi * gc[0] / 255)
                g = 255 - (255 - g) * (1 - gi * gc[1] / 255)
                b = 255 - (255 - b) * (1 - gi * gc[2] / 255)
            vy = abs((y / H) - 0.5) * 2
            vig = 1.0 - 0.14 * (vy ** 2)
            r *= vig; g *= vig; b *= vig
            raw += bytes((clamp(r), clamp(g), clamp(b)))

    def chunk(typ, data):
        c = typ + data
        return struct.pack(">I", len(data)) + c + struct.pack(">I", binascii.crc32(c) & 0xffffffff)
    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    png += chunk(b"IEND", b"")
    open(path, "wb").write(png)
    print(f"wrote {path} ({len(png)} bytes)")

def gold(x, y, r=560, i=0.85):
    """A gold glow + tighter hot core at the same spot for a defined accent."""
    return [
        {"x": x, "y": y, "r": r,        "intensity": i,        "color": GOLD},
        {"x": x, "y": y, "r": r * 0.42, "intensity": i * 0.75, "color": GOLD_HOT},
    ]

BASE      = [(0.0, NAVY_DEEP), (0.30, NAVY), (0.62, TEAL), (1.0, NAVY_DEEP)]
BASE_TEAL = [(0.0, NAVY_DEEP), (0.25, NAVY), (0.55, TEAL), (0.80, TEAL), (1.0, NAVY)]
BASE_GOLD = [(0.0, NAVY_DEEP), (0.35, NAVY), (0.70, TEAL), (1.0, NAVY)]

build("home.png",     BASE,      gold(0.72, 0.55, 720, 0.92))
build("sales.png",    BASE_GOLD, gold(0.85, 0.50, 780, 1.05))
build("podcast.png",  BASE_TEAL, gold(0.16, 0.45, 640, 0.78))
build("brand.png",    BASE,      gold(0.50, 0.48, 680, 0.98))
build("exec.png",     BASE,      gold(0.36, 0.52, 700, 0.88))
build("projects.png", BASE_TEAL, gold(0.78, 0.50, 720, 0.92))
