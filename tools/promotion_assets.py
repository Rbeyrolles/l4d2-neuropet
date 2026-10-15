"""Export accepted cover art for the addon list and Workshop without redrawing."""
from pathlib import Path
import hashlib
import io
import json

from PIL import Image


def load_publication(root, filename="publication.json"):
    config = json.loads((Path(root) / filename).read_text(encoding="utf-8"))
    if config.get("schema") != 1:
        raise ValueError("Unsupported publication configuration")
    return config


def jpeg_bytes(image, size):
    # Baseline RGB JPEG is also understood by the game's addon-list decoder.
    output = io.BytesIO()
    image.convert("RGB").resize((size, size), Image.Resampling.LANCZOS).save(
        output, format="JPEG", quality=95, subsampling=0, optimize=True, progressive=False)
    return output.getvalue()


def prepare_cover(root, key, config):
    edition = config["editions"][key]
    path = Path(root) / edition["cover"]
    original = path.read_bytes()
    if hashlib.sha256(original).hexdigest() != edition["cover_sha256"]:
        raise ValueError("The cover differs from the accepted publication asset")
    with Image.open(io.BytesIO(original)) as image:
        if image.width != image.height:
            raise ValueError("The accepted publication cover must be square")
        icon = jpeg_bytes(image, 256)
        preview = jpeg_bytes(image, 1024)
        size = [image.width, image.height]
    if len(preview) >= 1_000_000:
        raise ValueError("The Workshop preview must be below one megabyte")
    credits = (
        "Original mascot artwork: Paccha, https://linktr.ee/paccha_\n"
        "Source packs: Neuron / Eviling from CommentOut64/web-mascot;\n"
        "upstream qingchenyouforcc/NeurolingsCE-Qt.\n"
        "Cover: AI-assisted composition and character enlargement based on\n"
        "the original hugging artwork; Neuro-sama cover mirrored for the paired layout.\n"
        "Background, typography and cover redraw are not an original drawing by Paccha.\n"
        "The game's original sprite atlas is unaffected by cover preparation.\n"
        "Cover adaptation license: CC BY-NC-SA 4.0.\n"
        "https://creativecommons.org/licenses/by-nc-sa/4.0/\n")
    if edition.get("cover_credits_file"):
        credits = (Path(root) / edition["cover_credits_file"]).read_text(encoding="utf-8")
    metadata = {"cover_source": edition["cover"], "cover_source_sha256": edition["cover_sha256"],
                "cover_source_size": size, "addon_image": "addonimage.jpg", "addon_image_size": [256, 256],
                "addon_image_sha256": hashlib.sha256(icon).hexdigest(),
                "workshop_preview_size": [1024, 1024], "workshop_preview_bytes": len(preview),
                "workshop_preview_sha256": hashlib.sha256(preview).hexdigest(),
                "cover_processing": "size/format export only; accepted PNG preserved"}
    return icon, preview, credits, metadata
