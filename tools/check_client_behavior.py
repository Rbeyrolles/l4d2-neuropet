"""Read the packaged VMT and exercise its scalar proxy pipeline.

This is a reference evaluator of Valve's documented proxies, not an engine
substitute. Native engine tests and manual observation separately verify loading
and rendering.
"""
from pathlib import Path
import argparse
import hashlib
import json
import math
import random
import re
import struct
from read_vpk import read_entry

ROOT = Path(__file__).resolve().parents[1]


def f32(value):
    return struct.unpack("<f", struct.pack("<f", value))[0]


class ProxyVM:
    def __init__(self, material, seed=1):
        header, body = material.split('"Proxies"', 1)
        self.values = {}
        for key, value in re.findall(r'"([^"\n]+)"\s+"([^"\n]+)"', header):
            if value.startswith("["):
                self.values[key] = [f32(float(n)) for n in value.strip("[]").split()]
            else:
                try:
                    self.values[key] = f32(float(value))
                except ValueError:
                    pass
        self.instructions = []
        self.rng = random.Random(seed)
        for name, block in re.findall(r'"(\w+)"\s*\{([^{}]*)\}', body):
            arguments = dict(re.findall(r'"([^"\n]+)"\s+"([^"\n]+)"', block))
            for key, value in arguments.items():
                if key in ("srcVar1", "srcVar2", "lessEqualVar", "greaterVar"):
                    assert value in self.values, (name, key, value)
            self.instructions.append((name, arguments))

    def get(self, text):
        return self.values[text] if text.startswith("$") else f32(float(text))

    def put(self, key, value):
        match = re.fullmatch(r"(.+)\[(\d+)\]", key)
        if match:
            self.values[match[1]][int(match[2])] = f32(value)
        else:
            self.values[key] = f32(value)

    def bind(self, seconds):
        time = f32(seconds)
        for name, args in self.instructions:
            if name == "TextureTransform":
                continue
            dest = args["resultVar"]
            if name == "LinearRamp":
                value = f32(self.get(args.get("rate", "1")) * time) + self.get(args.get("initialValue", "0"))
            elif name == "UniformNoise":
                value = self.rng.uniform(self.get(args.get("minVal", "0")), self.get(args.get("maxVal", "1")))
            elif name == "LessOrEqual":
                value = self.get(args["lessEqualVar"] if self.get(args["srcVar1"]) <= self.get(args["srcVar2"]) else args["greaterVar"])
            else:
                a = self.get(args["srcVar1"])
                b = self.get(args["srcVar2"]) if "srcVar2" in args else 0
                if name == "Equals":
                    value = a
                elif name == "Add":
                    value = a + b
                elif name == "Subtract":
                    value = a - b
                elif name == "Multiply":
                    value = a * b
                elif name == "Abs":
                    value = abs(a)
                elif name == "Divide":
                    value = a / b if b else a
                elif name == "Clamp":
                    value = min(self.get(args.get("max", "1")), max(self.get(args.get("min", "0")), a))
                elif name == "Frac":
                    value = a - int(a)
                elif name == "Int":
                    value = math.trunc(a)
                elif name == "WrapMinMax":
                    lo, hi = self.get(args.get("minVal", "0")), self.get(args.get("maxVal", "1"))
                    if hi <= lo:
                        value = lo
                    else:
                        unit = f32((a - lo) / (hi - lo))
                        unit -= int(unit) if unit >= 0 else int(unit) - 1
                        value = unit * (hi - lo) + lo
                else:
                    raise AssertionError("Unknown proxy: " + name)
            self.put(dest, value)
        return self.values


def scenario_vm(material, pick=0, style=0, gesture=4, **overrides):
    vm = ProxyVM(material)
    vm.bind(0)
    settings = {"pick": pick, "ground_style": style, "gesture_pick": gesture,
                "pace": 1, "pause": 3, "range": .8, "rest_pose": 0,
                "home_x": (24 - 200) / 96, "goal_raw": (24 - 650) / 96, "end": 1000}
    settings.update(overrides)
    for name, value in settings.items():
        vm.values["$np_" + name] = f32(value)
    vm.bind(0)
    return vm


def check_ground_actions(material, poses):
    travel = {}
    for label, style in (("walk", 0), ("run", 3), ("creep", 4)):
        vm = scenario_vm(material, style=style)
        start = vm.bind(3)["$np_output_x"]
        v = vm.bind(4)
        travel[label] = abs(v["$np_output_x"] - start) * 96
        pose = poses[label + "_left"]
        assert pose["frame_base"] <= v["$frame"] < pose["frame_base"] + pose["frames"], label
    assert travel["run"] > travel["walk"] * 1.8 and travel["creep"] < travel["walk"] * .6, travel
    cases = []
    for pick, style, gesture, expected in (
        (0, 0, 0, "trip_left"), (1, 3, 0, "trip_right"),
        (0, 4, 0, None), (1, 0, 1, "hug"),
        (8, 4, 1, "hug"), (8, 0, 0, None),
    ):
        vm = scenario_vm(material, pick, style, gesture)
        bursts, previous_active, event_frames, event_x = 0, False, set(), []
        ground_samples, image_changes = 0, []
        for step in range(2400):
            v = vm.bind(step / 30)
            if not v["$np_moving_mode"]:
                assert abs(24 - v["$np_output_x"] * 96 - 200) < .01 and abs(24 - v["$np_output_y"] * 96 - 432) < .01, "Nonmoving route escaped its floor point"
            active = bool(v["$np_gesture_active"])
            if active and not previous_active:
                bursts += 1
            if active:
                assert expected, "A resting or crawling pet must not use the upright trip"
                pose = poses[expected]
                index = int(v["$frame"] - pose["frame_base"])
                assert 0 <= index < pose["frames"], (expected, index)
                assert abs(24 - v["$np_output_y"] * 96 - 432) < .01, "Gesture above the floor"
                event_frames.add(index)
                event_x.append(v["$np_output_x"])
                if expected.startswith("trip"):
                    image = pose["images"][index]
                    if not image_changes or image_changes[-1] != image:
                        image_changes.append(image)
                    if image == "trip2.png":
                        ground_samples += 1
            previous_active = active
        assert bursts == (1 if expected else 0), "Gesture repeated"
        if expected:
            assert len(event_frames) == poses[expected]["frames"], "One-shot frames skipped"
            assert max(event_x) - min(event_x) < .001, "Pet moved during the one-shot"
            rest = poses["rest_pool"]
            assert rest["frame_base"] <= v["$frame"] < rest["frame_base"] + rest["frames"], "Pet did not resume normal rest"
            target = 650 if pick < 8 else 200
            assert abs(24 - v["$np_output_x"] * 96 - target) < .01, "Pet did not finish the ground journey"
            if pick < 8:
                assert abs(v["$np_output_x"] - event_x[-1]) > .01, "Movement did not resume"
            if expected.startswith("trip"):
                assert ground_samples / 30 >= 1, "Ground contact too brief"
                assert image_changes == ["trip1.png", "trip2.png", "trip3.png", "shime11.png", "shime1.png"], "Recovery missing intermediate poses"
        cases.append({"pick": pick, "style": style, "gesture": expected,
                      "bursts": bursts, "frames_observed": len(event_frames),
                      "on_ground_seconds": ground_samples / 30, "recovery_images": image_changes})
    return {"relative_speeds": "passed", "travel_units_per_second": travel,
            "one_shot_and_resume": "passed", "cases": cases}


def check_creep_speed(material, manifest):
    width = manifest["aspect"] * 480
    limit = manifest["ground_styles"]["creep"]["speed_limit"]
    samples = []
    for pick, home, goal in ((0, width - 64, 16), (1, 16, width - 64),
                             (2, width - 64, width - 64), (3, 16, 16),
                             (4, width - 64, width - 64), (5, 16, 16),
                             (6, width - 64, 16), (7, 16, width - 64)):
        for pace in (.85, 1.15):
            vm = scenario_vm(material, pick=pick, style=4, pace=pace,
                             home_x=(24 - home) / 96, goal_raw=(24 - goal) / 96)
            v = vm.bind(0)
            intervals = [(0, v["$np_d1"])]
            if not v["$np_is_ceiling"]:
                intervals.append((v["$np_boundary4"], v["$np_d5"]))
            for begin, duration in intervals:
                seconds = 3 + (begin + duration * .5) / pace
                a = vm.bind(seconds)["$np_output_x"]
                v = vm.bind(seconds + 1 / 30)
                speed = abs(v["$np_output_x"] - a) * 96 * 30
                assert speed <= limit * pace + .03, (pick, pace, begin, speed)
                assert abs(24 - v["$np_output_y"] * 96 - 432) < .01
                is_left = v["$np_output_x"] > a
                pose = manifest["poses"]["creep_left" if is_left else "creep_right"]
                assert pose["frame_base"] <= v["$frame"] < pose["frame_base"] + pose["frames"], "Crawl facing differs from movement"
                samples.append({"route": pick, "pace": pace, "leg": "outbound" if begin == 0 else "return",
                                "duration": duration, "speed": speed})
    return {"speed_bound": "passed", "both_legs": "passed", "facing": "passed",
            "maximum_observed_speed": max(sample["speed"] for sample in samples),
            "base_limit": limit, "samples": samples}


def check_surface_drops(material):
    """Force both surfaces so duration tweaks cannot make coverage stochastic."""
    samples = []
    for pick, wall in ((2, True), (5, False)):
        vm = scenario_vm(material, pick=pick)
        points = []
        for step in range(2400):
            v = vm.bind(step / 30)
            if v["$np_boundary3"] <= v["$np_age"] < v["$np_boundary4"]:
                assert v["$np_drop"] and bool(v["$np_wall_drop"]) == wall, "Surface release missing"
                x, y = 24 - v["$np_output_x"] * 96, 24 - v["$np_output_y"] * 96
                points.append((x, y))
                samples.append({"x": x, "wall": wall})
        assert points and points[-1][1] - points[0][1] > 100, "No downward motion after release"
    return samples


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=ROOT / "dist/client-build-manifest.json")
    args = parser.parse_args()
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    pack = args.manifest.parent / manifest["vpk"]
    assert hashlib.sha256(pack.read_bytes()).hexdigest() == manifest["sha256"], "Manifest identifies a different package"
    material = read_entry(pack, manifest.get("material", "materials/vgui/neuropet_client/behavior.vmt")).decode()
    vm = ProxyVM(material, seed=126)
    width = manifest["aspect"] * 480
    total_frames = sum(p["frames"] for p in manifest["poses"].values())
    episodes, picks, last = [], set(), None
    rests, drops, rest_clips = [], [], set()
    last_point = None
    ground_styles, gestures = set(), set()
    gesture_bursts, previous_gesture = {}, False
    hold_names = ("$np_pick", "$np_pace", "$np_pause", "$np_range", "$np_rest_pose", "$np_end",
                  "$np_goal_raw", "$np_goal_x", "$np_home_x", "$np_ground_style", "$np_gesture_pick")
    for step in range(18000):
        v = vm.bind(step / 30)
        boundaries = [0] + [v[f"$np_boundary{i}"] for i in range(1, 6)]
        active_count = sum(a <= v["$np_age"] < b for a, b in zip(boundaries, boundaries[1:])) * v["$np_moving_mode"]
        assert active_count in (0, 1), "Overlapping stages"
        assert 0 <= v["$frame"] < total_frames, "Invalid atlas frame"
        x, y = 24 - v["$np_output_x"] * 96, 24 - v["$np_output_y"] * 96
        assert -25 <= x <= width and -21 <= y <= 433, (step, x, y)
        current = (v["$np_start"], tuple(v[n] for n in hold_names))
        if last and current[0] == last[0]:
            assert current[1] == last[1], "Random selection changed mid-episode"
        else:
            assert abs(x - (24 - v["$np_home_x"] * 96)) < .01 and abs(y - 432) < .01, "Episode boundary teleported"
            if last_point:
                assert abs(v["$np_home_x"] - last_point["goal"]) < .001, "Previous landing point not retained"
            episodes.append({"start": current[0], "pick": v["$np_pick"], "pace": v["$np_pace"],
                             "pause": v["$np_pause"], "range": v["$np_range"],
                             "home_x": x, "goal_x": 24 - v["$np_goal_x"] * 96})
            picks.add(v["$np_pick"])
        last = current
        stage = next((i for i in range(5) if boundaries[i] <= v["$np_age"] < boundaries[i + 1]), None)
        if last_point and last_point["episode"] == current[0] and stage == last_point["stage"]:
            max_dx = (width + 48) * 1.15 / (5 * 30) + .1
            assert abs(x - last_point["x"]) < max_dx and abs(y - last_point["y"]) < 35, "Intra-stage position jitter"
        last_point = {"episode": current[0], "stage": stage, "x": x, "y": y, "goal": v["$np_goal_x"]}
        rest_base = manifest["poses"]["rest_pool"]["frame_base"]
        if abs(y - 432) < .01 and rest_base <= v["$frame"] < rest_base + manifest["poses"]["rest_pool"]["frames"]:
            rests.append(x)
            rest_clips.add(int((v["$frame"] - manifest["poses"]["rest_pool"]["frame_base"]) / 8))
        if stage == 3 and v["$np_drop"] and -10 < y < 420:
            drops.append({"x": x, "wall": bool(v["$np_wall_drop"])})
        ground_styles.add("walk" if v["$np_ground_style"] <= 2 else "run" if v["$np_ground_style"] == 3 else "creep")
        active_gesture = bool(v["$np_gesture_active"])
        if active_gesture:
            assert abs(y - 432) < .01 and (not v["$np_moving_mode"] or stage == 0), "Gesture interrupted climbing"
            gestures.add("trip" if v["$np_gesture_pick"] == 0 else "hug")
            if not previous_gesture:
                gesture_bursts[current[0]] = gesture_bursts.get(current[0], 0) + 1
                assert gesture_bursts[current[0]] == 1, "Gesture played twice in one episode"
        previous_gesture = active_gesture
    # Multiple binds at the same timestamp must not resample the held behavior.
    before = tuple(vm.values[n] for n in hold_names)
    for _ in range(10):
        vm.bind(17999 / 30)
        assert tuple(vm.values[n] for n in hold_names) == before
    # Map time reset and returning after a long absence restart at the floor hub.
    for time in (0, 10000, 0):
        v = vm.bind(time)
        assert v["$np_renew"] == 1
        assert abs(24 - v["$np_output_y"] * 96 - 432) < .01
    assert len(episodes) > 5 and len(picks) > 2, "Insufficient runtime variety"
    assert len(rest_clips) >= 5, "Insufficient rest animation variety"
    assert max(rests) - min(rests) > width * .25, "Rest locations did not vary"
    forced_drops = check_surface_drops(material)
    all_drops = drops + forced_drops
    assert any(d["wall"] for d in all_drops) and any(not d["wall"] for d in all_drops), "Both wall and ceiling drops required"
    assert max(d["x"] for d in all_drops) - min(d["x"] for d in all_drops) > width * .25, "Drop positions did not vary"
    ground_checks = check_ground_actions(material, manifest["poses"])
    creep_checks = check_creep_speed(material, manifest)
    result = {"vpk": pack.name, "sha256": manifest["sha256"], "character": manifest.get("character", "neuron"),
              "proxy_evaluator": "Valve scalar semantics with float32 results",
              "bindings": 18000, "episodes": len(episodes), "distinct_picks": sorted(picks),
              "held_choice": "passed", "single_stage": "passed", "atlas_frames": "passed",
              "boundary_continuity": "passed", "clock_reset": "passed", "intra_stage_jitter": "passed",
              "rest_clips": sorted(rest_clips), "rest_x_range": [min(rests), max(rests)],
              "wall_and_ceiling_drops": "passed", "drop_x_range": [min(d["x"] for d in all_drops), max(d["x"] for d in all_drops)],
              "sampled_drop_types": sorted({"wall" if d["wall"] else "ceiling" for d in drops}),
              "forced_drop_types": ["wall", "ceiling"],
              "ground_styles": sorted(ground_styles), "gestures": sorted(gestures), "ground_actions": ground_checks,
              "creep_motion": creep_checks,
              "episode_sample": episodes[:12]}
    output = args.manifest.with_name(args.manifest.name.replace("build-manifest", "behavior-checks"))
    assert output != args.manifest, "Expected a *build-manifest*.json filename"
    output.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps({k: v for k, v in result.items() if k != "episode_sample"}))


if __name__ == "__main__":
    main()
