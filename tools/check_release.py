"""Check the public VPK, notices, artwork and optional packaging baseline."""
from pathlib import Path
import argparse
import hashlib
import json
import struct
import io

from PIL import Image
from check_client_behavior import ProxyVM
from read_vpk import entries, read_entry
from promotion_assets import load_publication
from addon_metadata import addoninfo_text, addon_description

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=ROOT / "dist/client-build-manifest.json")
    parser.add_argument("--baseline", type=Path, help="Compare runtime resources with a previously tested VPK")
    args = parser.parse_args()
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    vpk = args.manifest.parent / manifest["vpk"]
    assert hashlib.sha256(vpk.read_bytes()).hexdigest() == manifest["sha256"]
    data = {name: read_entry(vpk, name) for name, _ in entries(vpk)}
    assert len(data) == manifest["files"] == 10, "The branded public package should contain ten files"
    assert manifest["speed"] == 1 and manifest["diagnostic"] is None, "Development diagnostics must not ship"
    namespace = Path(manifest["material"]).parent.name
    publication = load_publication(ROOT)
    title = publication["editions"][manifest["character"]]["title"]
    assert manifest["title"] == title and f'"addonTitle" "{title}"' in data["addoninfo.txt"].decode("utf-8")
    assert manifest["maintainer"] == publication["maintainer"]
    assert manifest["addon_description"] == addon_description(publication, manifest["character"])
    assert data["addoninfo.txt"].decode("utf-8") == addoninfo_text(publication, manifest["character"], manifest["version"])
    icon = data["addonimage.jpg"]
    assert hashlib.sha256(icon).hexdigest() == manifest["branding"]["addon_image_sha256"]
    with Image.open(io.BytesIO(icon)) as image:
        assert image.format == "JPEG" and image.mode == "RGB" and image.size == (256, 256)
    assert b"AI-assisted" in data[f"resource/{namespace}/COVER-CREDITS.txt"]
    cover = ROOT / manifest["branding"]["cover_source"]
    assert hashlib.sha256(cover.read_bytes()).hexdigest() == manifest["branding"]["cover_source_sha256"]
    preview = args.manifest.parent / "branding" / manifest["character"] / "preview.jpg"
    assert hashlib.sha256(preview.read_bytes()).hexdigest() == manifest["branding"]["workshop_preview_sha256"]
    assert preview.stat().st_size < 1_000_000
    assert not any(name.endswith((".nut", ".nuc", ".sp", ".dll", ".cfg")) or name.startswith("modes/") for name in data)
    assert "scripts/hudanimations.txt" not in data
    assert data[f"resource/{namespace}/CODE-LICENSE.txt"] == (ROOT / "LICENSE").read_bytes()
    pack = ROOT / "assets/mascot_pack" / manifest["source_pack"]
    license_name = "EVILING-LICENSE.txt" if manifest["character"] == "evil" else "NEURON-LICENSE.txt"
    assert data[f"resource/{namespace}/{license_name}"] == (pack / "LICENSE").read_bytes()
    assert data[f"resource/{namespace}/LICENSE-CC-BY-NC-SA-4.0.txt"] == (pack / "LICENSE-CC-BY-NC-SA-4.0.txt").read_bytes()
    for name, digest in manifest["source_images"].items():
        assert hashlib.sha256((pack / "img" / name).read_bytes()).hexdigest() == digest
    material = data[manifest["material"]].decode("ascii")
    vm = ProxyVM(material)
    assert len(vm.instructions) == manifest["proxy_count"] <= 256
    assert sum(name.startswith("$np_") for name in vm.values) == manifest["vmt_variables"] <= 155
    atlas = data[f"materials/vgui/{namespace}/poses.vtf"]
    assert atlas[:4] == b"VTF\0"
    assert struct.unpack_from("<II", atlas, 4) == (7, 2)
    header = struct.unpack_from("<I", atlas, 12)[0]
    width, height = struct.unpack_from("<HH", atlas, 16)
    frames = struct.unpack_from("<H", atlas, 24)[0]
    assert struct.unpack_from("<I", atlas, 52)[0] == 0, "Expected RGBA8888"
    assert (width, height, frames) == (256, 256, 202)
    assert frames == sum(pose["frames"] for pose in manifest["poses"].values())
    span = width * height * 4
    assert len(atlas) == header + frames * span
    for index in range(frames):
        frame = Image.frombytes("RGBA", (width, height), atlas[header + index * span:header + (index + 1) * span])
        bounds = frame.getchannel("A").getbbox()
        assert bounds and 0 < bounds[0] < bounds[2] < width and 0 < bounds[1] < bounds[3] < height, (index, bounds)
    comparison = None
    if args.baseline:
        previous = {name: read_entry(args.baseline, name) for name, _ in entries(args.baseline)}
        approved_added = {"addonimage.jpg", f"resource/{namespace}/CODE-LICENSE.txt", f"resource/{namespace}/COVER-CREDITS.txt"}
        added = set(data) - set(previous)
        assert added <= approved_added
        assert not set(previous) - set(data)
        changed = []
        for name, value in previous.items():
            if data[name] != value:
                assert name == "addoninfo.txt", "Runtime or license entry changed: " + name
                changed.append(name)
        comparison = {"sha256": hashlib.sha256(args.baseline.read_bytes()).hexdigest(),
                      "baseline_entries_unchanged": len(previous) - len(changed),
                      "changed_metadata_files": changed, "extra_files": sorted(added),
                      "runtime_material_atlas_and_hud_unchanged": True}
    result = {"vpk": vpk.name, "sha256": manifest["sha256"], "files_crc_verified": len(data),
              "licenses": "passed", "source_fingerprints": "passed", "atlas_frames": frames,
              "transparent_borders": "passed", "proxy_count": len(vm.instructions),
              "vmt_variables": manifest["vmt_variables"], "diagnostics_off": True,
              "title": title, "author": publication["maintainer"], "bilingual_addon_description": "passed",
              "addon_image": "passed", "workshop_preview": "passed", "cover_source": "passed",
              "baseline_comparison": comparison}
    output = args.manifest.with_name(args.manifest.name.replace("build-manifest", "release-checks"))
    assert output != args.manifest
    output.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result))


if __name__ == "__main__":
    main()
