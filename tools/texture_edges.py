"""Prepare hidden texture colours for straight-alpha GPU filtering.

The source PNGs keep white RGB under zero alpha. Extending the surrounding
artwork into those transparent texels prevents white entering the filtered
colour before the shader blends it. Alpha and all visible pixels stay intact.
"""
from collections import deque

from PIL import Image

BLEED_RADIUS = 4


def bleed_transparent_rgb(image, radius=BLEED_RADIUS):
    """Flood only alpha-zero RGB using eight-connected neighbourhoods.

    Distance is measured in eight-connected pixel steps. A bounded ring is
    enough for the single-mip client texture; far-away transparent padding is
    retained. The input image is never modified.
    """
    if radius < 0:
        raise ValueError("The colour bleed radius cannot be negative")
    rgba = image.convert("RGBA")
    width, height = rgba.size
    data = bytearray(rgba.tobytes())
    occupied = bytearray(bool(alpha) for alpha in data[3::4])
    queue = deque((index, 0) for index, known in enumerate(occupied) if known)
    while queue:
        index, depth = queue.popleft()
        if depth >= radius:
            continue
        x, y = index % width, index // width
        colour = data[index * 4:index * 4 + 3]
        for ny in range(max(0, y - 1), min(height, y + 2)):
            for nx in range(max(0, x - 1), min(width, x + 2)):
                neighbor = ny * width + nx
                if occupied[neighbor]:
                    continue
                occupied[neighbor] = 1
                data[neighbor * 4:neighbor * 4 + 3] = colour
                queue.append((neighbor, depth + 1))
    return Image.frombytes("RGBA", (width, height), bytes(data))


def prepare_frames(frames, radius=BLEED_RADIUS):
    """Process each distinct padded pose once and report the texture operation."""
    cache, result = {}, []
    changed_unique, changed_total = 0, 0
    for frame in frames:
        source = frame.tobytes()
        if source not in cache:
            fixed = bleed_transparent_rgb(frame, radius)
            output = fixed.tobytes()
            changed = sum(source[i:i + 4] != output[i:i + 4]
                          for i in range(0, len(source), 4))
            cache[source] = (fixed, changed)
            changed_unique += changed
        fixed, changed = cache[source]
        result.append(fixed)
        changed_total += changed
    return result, {"method": "transparent RGB colour bleed", "radius_texels": radius,
                    "alpha_changed": False, "visible_pixels_changed": False,
                    "unique_frames": len(cache), "changed_pixels_unique": changed_unique,
                    "changed_pixels_all_frames": changed_total}
