"""Build a local interactive duo; original atlas frames remain byte-identical."""
from pathlib import Path
import argparse
import hashlib
import json
import struct
import sys

sys.dont_write_bytecode = True
WORK = Path(__file__).resolve().parent
PROJECT = WORK.parent
sys.path.insert(0, str(WORK))
from build_client import panel
from client_behavior import material_text
from check_client_behavior import ProxyVM
from read_vpk import entries, read_entry
from source_formats import write_vpk
from duo_perimeter_behavior import compile_pair
from addon_metadata import addoninfo_text
from promotion_assets import load_publication, prepare_cover

BASE = PROJECT / "dist"
NAME = "l4d2_neuropet_duo_interactive.vpk"
VERSION = "0.2.3"
SCENARIOS = tuple(kind + "-" + pet + side for kind in ("seek", "short", "encounter")
                  for pet in ("neuro", "evil") for side in ("", "-left"))


def configure_scene(program, scenario, clock=0):
    if scenario:
        assert scenario in SCENARIOS
        hero = 0 if "neuro" in scenario else 1
        encounter = scenario.startswith("encounter")
        short = scenario.startswith("short")
        left = scenario.endswith("-left")
        for i in (0, 1):
            if left:
                x = (300 if encounter else 250 if short else 240) if i == hero else (320 if encounter else 330 if short else 620)
            elif short:
                x = 330 if i == hero else 250
            elif i == hero:
                x = (290 if hero == 0 else 320) if encounter else 620
            else:
                x = 250 if encounter else 240
            settings = {"s": (x+10)/96, "goal_s": (x+10)/96,
                        "end": 0 if encounter and not left and i == hero else 100000, "start": 0,
                        "random": .1, "mode": 0}
            for key, value in settings.items():
                program.values[f"$np_a{i}_{key}"] = float(value)
        program.values["$np_social_deadline"] = 1.0
        # At decision clock 1, force a successful role sample (.1 or .5).
        # This changes only the diagnostic lottery salt; production uses .817.
        salts = [key for key, value in program.values.items() if value == .817]
        assert len(salts) == 1
        program.values[salts[0]] = .369 if hero == 0 else .769
    if clock:
        for proxy in program.proxies:
            if proxy["name"] == "LinearRamp" and proxy["values"]["resultVar"] == "$np_time":
                proxy["values"]["initialValue"] = -clock


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=PROJECT / "dist")
    parser.add_argument("--base-dist", type=Path, default=BASE,
                        help="Directory containing the two normal single-pet VPKs and manifests")
    parser.add_argument("--scenario", choices=SCENARIOS)
    parser.add_argument("--clock", type=float, default=0)
    parser.add_argument("--vpk-name", default=NAME)
    args = parser.parse_args()
    assert Path(args.vpk_name).name == args.vpk_name
    publication = load_publication(PROJECT, "publication-duo.json")
    icon, preview, cover_credits, cover_metadata = prepare_cover(PROJECT, "duo", publication)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    files, pets, prefix = {"addonimage.jpg": icon}, [], None
    for actor, (filename, edition) in enumerate((("client-build-manifest.json", "neuron"), ("evil-client-build-manifest.json", "evil"))):
        m = json.loads((args.base_dist / filename).read_text(encoding="utf-8"))
        assert not m.get("diagnostic") and m.get("speed", 1) == 1, "Use normal single-pet builds"
        source = args.base_dist / m["vpk"]
        assert hashlib.sha256(source.read_bytes()).hexdigest() == m["sha256"]
        data = {name: read_entry(source, name) for name, _ in entries(source)}
        old_ns = Path(m["material"]).parent.name
        ns = "neuropet_duo_interactive/" + edition
        old_layout = data["scripts/hudlayout.res"].decode("utf-8-sig").replace("\r\n", "\n")
        template, suffix = old_layout.rsplit('    "NeuroPetClient_00"', 1)
        assert '    "NeuroPetClient_00"' + suffix == panel(0, old_ns) + "}\n"
        if prefix is None:
            prefix = template
        assert template == prefix
        for name, value in data.items():
            if name.startswith("resource/" + old_ns + "/"):
                if name.endswith("/COVER-CREDITS.txt"):
                    value = cover_credits.encode("utf-8")
                if name.endswith("/MODIFICATIONS.txt"):
                    value += ("\nInteractive Duo Preview modifications:\n"
                              "The original 202 RGBA frames are retained byte-identically.\n"
                              "One fully transparent frame and 28 pixel-mirrored copies of\n"
                              "the original hug frames support both approach directions.\n"
                              "The original two-character hug clips now represent a coordinated\n"
                              "floor encounter or approach, with the receiver temporarily hidden.\n"
                              "Duo motion and interaction material logic independently written.\n").encode("ascii")
                files[name.replace(old_ns + "/", ns + "/", 1)] = value
        atlas = data[f"materials/vgui/{old_ns}/poses.vtf"]
        assert struct.unpack_from("<H", atlas, 24)[0] == 202 and len(atlas) == 80 + 202 * 256 * 256 * 4
        header = bytearray(atlas[:80])
        struct.pack_into("<H", header, 24, 231)
        frame_size = 256 * 256 * 4
        mirrored = bytearray()
        for frame in range(174, 202):
            source_frame = atlas[80 + frame * frame_size:80 + (frame + 1) * frame_size]
            for y in range(256):
                row = source_frame[y * 1024:(y + 1) * 1024]
                mirrored.extend(b"".join(row[x * 4:(x + 1) * 4] for x in range(255, -1, -1)))
        extended = bytes(header) + atlas[80:] + bytes(frame_size) + bytes(mirrored)
        assert extended[80:len(atlas)] == atlas[80:]
        files[f"materials/vgui/{ns}/poses.vtf"] = extended
        program = compile_pair(m["poses"], m["aspect"], actor)
        configure_scene(program, args.scenario, args.clock)
        # Native L4D2 rejects exactly 256 despite saying "more than 256".
        assert len(program.proxies) <= 255 and len(program.values) <= 128, program.meta
        material = material_text(program, ns).encode("ascii")
        path = f"materials/vgui/{ns}/behavior.vmt"
        files[path] = material
        assert len(ProxyVM(material.decode()).instructions) == len(program.proxies)
        pets.append({"actor": actor, "character": edition, "namespace": ns, "material": path,
                     "source_vpk": source.name, "source_sha256": m["sha256"], "poses": m["poses"],
                     "original_frames_byte_identical": 202, "frames": 231, "blank_frame": 202,
                     "mirrored_hug": {"frame_base": 203, "frames": 28, "source_base": 174},
                     "compiler": program.meta})
    files["scripts/hudlayout.res"] = (prefix + "".join(panel(i, pet["namespace"]).replace("NeuroPetClient_", "NeuroPetTogether_")
                                                    for i, pet in enumerate(pets)) + "}\n").encode("utf-8")
    files["addoninfo.txt"] = addoninfo_text(publication, "duo", VERSION).encode("utf-8")
    vpk = args.output_dir / args.vpk_name
    write_vpk(vpk, files)
    assert {name: read_entry(vpk, name) for name, _ in entries(vpk)} == files
    assert len(files) == 17
    (args.output_dir / "preview.jpg").write_bytes(preview)
    (args.output_dir / "cover.png").write_bytes(
        (PROJECT / publication["editions"]["duo"]["cover"]).read_bytes())
    manifest = {"version": VERSION, "vpk": vpk.name, "sha256": hashlib.sha256(vpk.read_bytes()).hexdigest(),
                "bytes": vpk.stat().st_size, "files": len(files), "aspect": m["aspect"],
                "diagnostic": args.scenario, "clock_offset": args.clock,
                "renderer": "two separate UnlitGeneric materials", "pets": pets,
                "publication": {"title": publication["editions"]["duo"]["title"],
                                "author": publication["maintainer"], "cover": cover_metadata},
                "interactions": {"chance": .6, "seek_seconds": "travel / selected speed", "hug_seconds": 4, "hug_art_seconds": 3.5,
                                 "approach_walk_speed": 30, "approach_run_speed": 60, "run_above_travel_units": 144,
                                 "minimum_break_after_hug": 45, "giver": "equal conditional lottery intervals, independent of position",
                                 "approach_directions": ["left", "right"],
                                 "floor_only": True, "receiver_hidden_during_original_two_character_clip": True}}
    (args.output_dir / "interactive-build-manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    (args.output_dir / "SHA256SUMS.txt").write_text(f'{manifest["sha256"]}  {vpk.name}\n', encoding="ascii")
    print(json.dumps({key: manifest[key] for key in ("vpk", "sha256", "bytes", "files", "diagnostic")}))


if __name__ == "__main__":
    main()
