"""Build a client-only pet using VGUI images and time-driven material proxies."""
from pathlib import Path
import argparse
import hashlib
import json

from PIL import Image, ImageOps
from pose_layout import POSES
from source_formats import write_vtf, write_vpk
from read_vpk import entries, read_entry
from client_behavior import compile_behavior, material_text, random_routes, CREEP_SPEED, CREEP_MIN_DURATION
from animation_assets import (action_clip, rest_pool, REST_ACTIONS, EVIL_REST_ACTIONS,
                              TRIP_RECOVERY, TRIP_RECOVERY_FRAMES)
from texture_edges import prepare_frames
from hud_template import load_hud_template
from promotion_assets import load_publication, prepare_cover
from addon_metadata import addoninfo_text, addon_description

ROOT = Path(__file__).resolve().parents[1]
SIZE = 48  # proportional VGUI units, against a 480-high viewport
HEIGHT = 480
TEXTURE_SPAN = SIZE * 2  # transparent padding around the original 128x128 art
CHARACTERS = {
    "neuron": {"pack": "Neuron", "name": "Neuron", "namespace": "neuropet_client",
               "version": "0.5.2", "edge_bleed": False,
               "directory": "client-only", "title": "Neuropet – Neuro-sama Screen Pet (Fan-made HUD Mascot)",
               "vpk": "l4d2_neuropet_client.vpk", "manifest": "client-build-manifest.json",
               "license": "NEURON-LICENSE.txt", "rests": REST_ACTIONS},
    "evil": {"pack": "Eviling", "name": "Evil Neuro (Eviling)", "namespace": "neuropet_evil_client",
             "version": "0.5.3", "edge_bleed": True,
             "directory": "client-only-evil", "title": "Neuropet – Evil Neuro Screen Pet (Fan-made HUD Mascot)",
             "vpk": "l4d2_neuropet_evil_client.vpk", "manifest": "evil-client-build-manifest.json",
             "license": "EVILING-LICENSE.txt", "rests": EVIL_REST_ACTIONS},
}
CLIENT_POSES = POSES + [
    ("hang_left", ["shime23"], 1, False),
    ("hang_right", ["shime23"], 1, True),
    ("wall_hold_left", ["shime12"], 1, False),
    ("wall_hold_right", ["shime12"], 1, True),
    ("run_left", ["run1", "run2", "run3", "run4"], 12, False),
    ("run_right", ["run1", "run2", "run3", "run4"], 12, True),
    ("creep_left", ["shime20", "shime21", "shime20", "shime21"], 3, False),
    ("creep_right", ["shime20", "shime21", "shime20", "shime21"], 3, True),
]










def panel(index, namespace="neuropet_client"):
    name = f"NeuroPetClient_{index:02d}"
    return f'''    "{name}"
    {{
        "ControlName" "ImagePanel"
        "fieldName" "{name}"
        "xpos" "0"
        "ypos" "0"
        "wide" "f0"
        "tall" "f0"
        "zpos" "100"
        "visible" "1"
        "enabled" "1"
        "usetitlesafe" "0"
        "scaleImage" "1"
        "image" "{namespace}/behavior"
        "drawcolor" "255 255 255 255"
        "fillcolor" "0 0 0 0"
        "mouseinputenabled" "0"
        "keyboardinputenabled" "0"
    }}
'''


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--character", choices=CHARACTERS, default="neuron", help="Build an independently packaged character edition")
    parser.add_argument("--pack", type=Path, help="Override the selected character's source pack")
    parser.add_argument("--game-root", type=Path, help="Read the stock HUD layout from a locally installed L4D2")
    parser.add_argument("--hud-template", type=Path, help="Use a locally extracted stock scripts/hudlayout.res instead")
    parser.add_argument("--speed", type=float, default=1, help="Accelerate the loop for engine diagnostics")
    parser.add_argument("--aspect", type=float, default=16 / 9, help="Sprite aspect correction; edge positions still follow the viewport")
    parser.add_argument("--fixed", action="store_true", help="Keep the original fixed 153.9-second loop")
    diagnostics = parser.add_mutually_exclusive_group()
    diagnostics.add_argument("--preview-trip", action="store_true", help="Development only: repeat running trips at normal animation speed")
    diagnostics.add_argument("--preview-creep", action="store_true", help="Development only: crawl across the floor at normal speed")
    args = parser.parse_args()
    publication = load_publication(ROOT)
    character = dict(CHARACTERS[args.character])
    character["title"] = publication["editions"][args.character]["title"]
    namespace = character["namespace"]
    bundled_pack = ROOT / "assets/mascot_pack" / character["pack"]
    pack = args.pack or (bundled_pack if bundled_pack.is_dir() else
                        ROOT.parent / "references/web-mascot/web-mascot/public/mascot_pack" / character["pack"])
    if args.speed <= 0 or args.aspect <= 0:
        parser.error("--speed and --aspect must be positive")
    if args.fixed:
        if args.character != "neuron":
            parser.error("The archived fixed edition only contains Neuron artwork")
        import shutil
        archive = ROOT / "dist/archives/l4d2_neuropet_client_0.2.0.vpk"
        if not archive.exists():
            parser.error("The archived fixed VPK is unavailable")
        shutil.copy2(archive, ROOT / "dist/l4d2_neuropet_client.vpk")
        shutil.copy2(ROOT / "dist/archives/client-build-manifest-0.2.0.json", ROOT / "dist/client-build-manifest.json")
        print("Restored the CRC-verified archived fixed 0.2.0 package")
        return
    template_path = args.hud_template
    local_template = ROOT / "scripts/neuropet_hudlayout_base.res"
    if template_path is None and args.game_root is None and local_template.is_file():
        template_path = local_template
    try:
        template, template_info = load_hud_template(args.game_root, template_path)
    except (OSError, ValueError) as error:
        parser.error(str(error))
    destination = ROOT / character["directory"]
    texture_dir = destination / "materials/vgui" / namespace
    texture_dir.mkdir(parents=True, exist_ok=True)
    routes = random_routes()
    required = {pose[0] for pose in CLIENT_POSES if pose[0] != "cheer"}
    files = {}
    poses = {}
    all_frames = []
    for name, sources, fps, mirror in CLIENT_POSES:
        if name not in required:
            continue
        frames = []
        if name in ("idle_left", "idle_right", "sit"):
            sources = list(dict.fromkeys(sources))
        for source in sources:
            with Image.open(pack / "img" / (source + ".png")) as image:
                frame = image.convert("RGBA")
                if mirror:
                    frame = ImageOps.mirror(frame)
                # Transparent borders prevent long clamped-texel streaks.
                padded = Image.new("RGBA", (256, 256))
                padded.paste(frame, (64, 64))
                frames.append(padded)
        poses[name] = {"frames": len(frames), "fps": fps, "mirror": mirror, "frame_base": len(all_frames),
                       "images": [source + ".png" for source in sources]}
        all_frames.extend(frames)
    def pad_rest(frame):
        padded = Image.new("RGBA", (256, 256))
        padded.paste(frame, (64, 64))
        return padded
    pool_frames, rest_clips = rest_pool(pack, pad_rest, character["rests"])
    poses["rest_pool"] = {"frames": len(pool_frames), "fps": 4, "mirror": False,
                          "frame_base": len(all_frames), "clip_frames": 8, "clips": rest_clips}
    all_frames.extend(pool_frames)
    for name, action, count, mirror in (
        ("trip_left", "Tripping", TRIP_RECOVERY_FRAMES, False),
        ("trip_right", "Tripping", TRIP_RECOVERY_FRAMES, True),
        ("hug", "HugAction", 28, False),
    ):
        recovery = [{"image": image, "duration": length, "anchor": "64,128"}
                    for _, image, length in TRIP_RECOVERY] if action == "Tripping" else None
        frames, images = action_clip(pack, action, count, mirror, source=recovery)
        poses[name] = {"frames": len(frames), "fps": 8, "mirror": mirror,
                       "frame_base": len(all_frames), "action": action,
                       "oneshot": True, "images": images}
        if action == "Tripping":
            poses[name]["timeline"] = [{"phase": phase, "image": image, "frames": length,
                                        "seconds": length / 8}
                                       for phase, image, length in TRIP_RECOVERY]
        all_frames.extend(frames)
    edge_processing = None
    if character["edge_bleed"]:
        all_frames, edge_processing = prepare_frames(all_frames)
    atlas_path = texture_dir / "poses.vtf"
    write_vtf(atlas_path, all_frames)
    files[atlas_path.relative_to(destination).as_posix()] = atlas_path.read_bytes()
    program = compile_behavior(routes, poses, args.aspect, args.speed, args.fixed, args.preview_trip, args.preview_creep)
    material_path = texture_dir / "behavior.vmt"
    material_path.write_text(material_text(program, namespace), encoding="ascii")
    files[material_path.relative_to(destination).as_posix()] = material_path.read_bytes()

    scripts = destination / "scripts"
    scripts.mkdir(parents=True, exist_ok=True)
    layout = template[:template.rfind("}")] + panel(0, namespace) + "}\n"
    (scripts / "hudlayout.res").write_text(layout, encoding="utf-8")
    files["scripts/hudlayout.res"] = layout.encode("utf-8")
    addon = addoninfo_text(publication, args.character, character["version"])
    (destination / "addoninfo.txt").write_text(addon, encoding="utf-8")
    files["addoninfo.txt"] = addon.encode("utf-8")
    icon, preview, cover_credits, cover_metadata = prepare_cover(ROOT, args.character, publication)
    (destination / "addonimage.jpg").write_bytes(icon)
    files["addonimage.jpg"] = icon
    branding_dir = ROOT / "dist/branding" / args.character
    branding_dir.mkdir(parents=True, exist_ok=True)
    (branding_dir / "preview.jpg").write_bytes(preview)
    notices = destination / "resource" / namespace
    notices.mkdir(parents=True, exist_ok=True)
    for target, source in ((character["license"], "LICENSE"), ("LICENSE-CC-BY-NC-SA-4.0.txt", "LICENSE-CC-BY-NC-SA-4.0.txt")):
        data = (pack / source).read_bytes()
        (notices / target).write_bytes(data)
        files[f"resource/{namespace}/" + target] = data
    modifications = (
        f"{character['name']} artwork by Paccha, https://linktr.ee/paccha_\n"
        "Source: https://github.com/CommentOut64/web-mascot\n"
        "PNG artwork converted to padded multi-frame RGBA8888 VTF; right-facing\n"
        "poses mirrored. A client material selects and retains random excursions;\n"
        "original action timing resampled; hug frames normalized to the foot anchor\n"
        "and displayed as a standalone one-shot scene.\n"
        "Tripping adapted with an extended ground hold, crouch, sit and stand recovery.\n"
        "Crawling retimed with alternating original poses and distance-based speed limiting.\n"
        "trajectories and material behavior independently written.\n"
        "Artwork license: CC BY-NC-SA 4.0. No web-mascot engine code included.\n")
    if edge_processing:
        modifications += ("Fully transparent RGB extended four texels from nearby artwork to\n"
                          "prevent white filtering fringes. Alpha and all visible source pixels unchanged.\n")
    (notices / "MODIFICATIONS.txt").write_text(modifications, encoding="ascii")
    files[f"resource/{namespace}/MODIFICATIONS.txt"] = modifications.encode("ascii")
    (notices / "COVER-CREDITS.txt").write_text(cover_credits, encoding="ascii")
    files[f"resource/{namespace}/COVER-CREDITS.txt"] = cover_credits.encode("ascii")
    code_license = ROOT / "LICENSE"
    if code_license.is_file():
        data = code_license.read_bytes()
        (notices / "CODE-LICENSE.txt").write_bytes(data)
        files[f"resource/{namespace}/CODE-LICENSE.txt"] = data
    assert "scripts/hudanimations.txt" not in files
    assert not any(name.endswith((".nut", ".nuc", ".dll", ".sp")) or name.startswith("modes/") for name in files)
    output = ROOT / "dist" / character["vpk"]
    write_vpk(output, files)
    assert {key for key, _ in entries(output)} == set(files)
    for name, data in files.items():
        assert read_entry(output, name) == data, name
    manifest = {"vpk": output.name, "sha256": hashlib.sha256(output.read_bytes()).hexdigest(),
                "files": len(files), "bytes": output.stat().st_size, "speed": args.speed,
                "aspect": args.aspect, "pose_size": SIZE, "version": character["version"],
                "character": args.character, "character_name": character["name"], "source_pack": character["pack"],
                "title": character["title"], "maintainer": publication["maintainer"],
                "addon_description": addon_description(publication, args.character), "branding": cover_metadata,
                "material": material_path.relative_to(destination).as_posix(),
                "hud_template": template_info,
                "behavior": "trip preview" if args.preview_trip else "creep preview" if args.preview_creep else "random excursions",
                "diagnostic": "repeat_trip" if args.preview_trip else "repeat_creep" if args.preview_creep else None,
                "loop_seconds": None,
                "renderer": "client material proxies", "poses": poses,
                "routes": routes, "proxy_count": len(program.proxies),
                "vmt_variables": len(program.values), "panels": 1,
                "ground_styles": {"walk": {"weight": 3, "duration": 10, "fps": 8},
                                  "run": {"weight": 1, "duration": 5, "fps": 12},
                                  "creep": {"weight": 1, "duration": "distance based", "min_duration": CREEP_MIN_DURATION,
                                            "speed_limit": CREEP_SPEED, "fps": 3}},
                "gestures": {"trip": {"weight": 1, "seconds": TRIP_RECOVERY_FRAMES / 8, "movement_only": True},
                             "hug": {"weight": 1, "seconds": 3.5, "standalone_scene": True},
                             "none": {"weight": 3}}}
    source_images = {name for pose in poses.values() for name in pose.get("images", [])}
    source_images.update(name for clip in rest_clips for name in clip["images"])
    manifest["source_images"] = {name: hashlib.sha256((pack / "img" / name).read_bytes()).hexdigest()
                                 for name in sorted(source_images)}
    if edge_processing:
        manifest["texture_processing"] = edge_processing
    (ROOT / "dist" / character["manifest"]).write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"Built and CRC-verified {output} ({len(files)} files, {len(routes)} routes, {len(program.proxies)} proxies)")


if __name__ == "__main__":
    main()
