"""A compact, persistent client behavior within L4D2's 255-proxy budget.

Random values are held for a whole excursion. Five reusable motion phases
cover short floor walks, partial wall climbs, ceiling drops and perimeter tours.
Excursions finish at a held random floor point, which starts the next one.
"""
SIZE, HEIGHT, SPAN = 48, 480, 96
# 155 custom parameters worked in release 0.4.0; use that as a conservative
# build budget, rather than treating it as the engine's documented hard limit.
TESTED_PARAMETER_BUDGET = 155
CREEP_SPEED = 8.0  # VGUI units per second before the held pace multiplier
CREEP_MIN_DURATION = 20.0


def random_routes():
    return [{"name": name, "weight": 2 if name == "rest" else 1, "stages": []} for name in (
        "stroll_left", "stroll_right", "explore_left_wall", "explore_right_wall",
        "ceiling_from_left", "ceiling_from_right", "perimeter_left", "perimeter_right", "rest")]


def point(position, width):
    def coordinate(token, dimension):
        return dimension / 2 + float(token[1:]) if token.startswith("c") else dimension - float(token[1:]) if token.startswith("r") else float(token)
    x, y = position.split()
    return coordinate(x, width), coordinate(y, HEIGHT)


class Program:
    def __init__(self):
        self.values, self.proxies = {}, []

    def var(self, name, value=0.0):
        key = "$np_" + name
        self.values[key] = value
        return key

    def emit(self, name, **values):
        self.proxies.append({"name": name, "values": values})

    def op(self, name, a, b, dest):
        self.emit(name, srcVar1=a, srcVar2=b, resultVar=dest)

    def copy(self, source, dest):
        self.emit("Equals", srcVar1=source, resultVar=dest)

    def select(self, a, b, yes, no, dest):
        self.emit("LessOrEqual", srcVar1=a, srcVar2=b, lessEqualVar=yes, greaterVar=no, resultVar=dest)

    def deduplicate_constants(self):
        """Share read-only values; keep every value written by a proxy distinct."""
        written = {item["values"]["resultVar"].split("[", 1)[0] for item in self.proxies}
        canonical, aliases = {}, {}
        for key, value in list(self.values.items()):
            if key not in written:
                source = canonical.setdefault(value, key)
                if source != key:
                    aliases[key] = source
                    del self.values[key]
        for item in self.proxies:
            item["values"] = {key: aliases.get(value, value) for key, value in item["values"].items()}


def compile_behavior(routes, poses, aspect, test_speed=1, fixed=False, preview_trip=False, preview_creep=False):
    if fixed:
        raise ValueError("Use the archived 0.2.0 VPK for the original fixed loop")
    p = Program()
    width = HEIGHT * aspect
    hx = p.var("home_x", (48 - width / 2) / SPAN)
    goal_x = p.var("goal_x", (48 - width / 2) / SPAN)
    z, one, two = p.var("zero"), p.var("one", 1.0), p.var("two", 2.0)
    time = p.var("time")
    p.emit("LinearRamp", rate=test_speed, initialValue=0, resultVar=time)
    start, end, previous = p.var("start"), p.var("end"), p.var("previous_time")
    expired, backward, diff, renew = [p.var(n) for n in ("expired", "backwards", "time_diff", "renew")]
    p.select(end, time, one, z, expired)
    p.op("Subtract", previous, time, diff)
    p.select(diff, z, z, one, backward)
    p.op("Add", expired, backward, renew)
    p.emit("Clamp", srcVar1=renew, min=0, max=1, resultVar=renew)
    p.select(renew, z, start, time, start)
    # Preserve the previous landing point before sampling the next destination.
    p.select(renew, z, hx, goal_x, hx)
    held = {}
    preview_values = {"pick": 0, "pace": 1, "pause": 3, "range": .8,
                      "rest_pose": 0, "ground_style": 3, "gesture_pick": 0} if preview_trip else {}
    if preview_creep:
        preview_values = {"pick": 0, "pace": 1, "pause": 3, "range": 1.2,
                          "rest_pose": 2, "ground_style": 4, "gesture_pick": 4,
                          "goal_raw": (88 - width) / SPAN}
    for name, lo, hi in (("pick", 0, 9.9999), ("pace", .85, 1.15),
                         ("pause", 3, 18), ("range", .55, 1.2), ("rest_pose", 0, 7.9999),
                         ("ground_style", 0, 4.9999), ("gesture_pick", 0, 4.9999),
                         ("goal_raw", (88 - width) / SPAN, 8 / SPAN)):
        if name in preview_values:
            lo = hi = preview_values[name]
        # The time comparison is finished; this scratch slot can sample each
        # held value in turn without keeping eight unused material parameters.
        sample, value = diff, p.var(name)
        p.emit("UniformNoise", minVal=lo, maxVal=hi, resultVar=sample)
        if name in ("pick", "rest_pose", "ground_style", "gesture_pick"):
            p.emit("Int", srcVar1=sample, resultVar=sample)
        p.select(renew, z, value, sample, value)
        held[name] = value
    mode, side = p.var("mode"), p.var("side")
    half = parity = diff
    p.op("Divide", held["pick"], two, half)
    p.emit("Int", srcVar1=half, resultVar=mode)
    p.op("Multiply", mode, two, parity)
    p.op("Subtract", held["pick"], parity, side)
    flags = {}
    scratch = square = diff
    for index, name in enumerate(("floor", "wall", "ceiling", "perimeter")):
        constant, flag = p.var("mode_" + name, float(index)), p.var("is_" + name)
        p.op("Subtract", mode, constant, scratch)
        p.op("Multiply", scratch, scratch, square)
        p.select(square, z, one, z, flag)
        flags[name] = flag
    move = p.var("moving_mode")
    p.select(mode, p.var("mode_last", 3.0), one, z, move)
    p.select(move, z, hx, held["goal_raw"], goal_x)
    wall_drop, drop = p.var("wall_drop"), p.var("drop")
    p.select(held["range"], p.var("drop_threshold", .9), one, z, wall_drop)
    p.op("Multiply", wall_drop, flags["wall"], wall_drop)
    p.op("Add", wall_drop, flags["ceiling"], drop)

    # Endpoints must be known before choosing distance-based ground durations.
    gy = p.var("home_y", -4.25)
    wx, other_x, top_x, target_x, upper_y, stage3x, stage3y, stage4x = [p.var(n) for n in (
        "wall_x", "other_wall_x", "top_x", "target_x", "upper_y", "stage3_x", "stage3_y", "stage4_x")]
    lx, rx = p.var("left_x", 34 / SPAN), p.var("right_x", (62 - width) / SPAN)
    p.select(side, z, lx, rx, wx)
    p.select(side, z, rx, lx, other_x)
    p.select(side, z, p.var("left_top_x", .5), p.var("right_top_x", (48 - width) / SPAN), top_x)
    distance = p.var("floor_distance")
    p.op("Multiply", held["range"], p.var("floor_distance_fraction", .55), diff)
    p.select(flags["floor"], z, one, diff, diff)
    p.op("Subtract", wx, hx, distance)
    p.op("Multiply", distance, diff, distance)
    p.op("Add", hx, distance, target_x)
    p.op("Multiply", p.var("wall_height", 2.25), held["range"], upper_y)
    p.op("Add", gy, upper_y, upper_y)
    p.select(flags["wall"], z, p.var("wall_top_y", .25), upper_y, upper_y)
    p.select(flags["floor"], z, upper_y, gy, upper_y)
    p.select(flags["perimeter"], z, goal_x, other_x, stage3x)
    p.select(flags["wall"], z, stage3x, wx, stage3x)
    p.select(flags["wall"], z, p.var("ceiling_y", 44 / SPAN), upper_y, stage3y)
    p.select(flags["floor"], z, stage3y, gy, stage3y)
    p.select(flags["perimeter"], z, wx, other_x, stage4x)
    p.select(flags["ceiling"], z, stage4x, goal_x, stage4x)
    climb_top_x = p.var("climb_top_x")
    p.select(flags["wall"], z, top_x, wx, climb_top_x)
    p.select(flags["floor"], z, climb_top_x, target_x, climb_top_x)
    p.select(flags["floor"], z, stage4x, target_x, stage4x)
    fall_end_x, wall_drift = p.var("fall_end_x"), p.var("wall_drift")
    p.op("Subtract", p.var("center_x", (48 - width / 2) / SPAN), stage4x, wall_drift)
    p.op("Multiply", wall_drift, p.var("wall_drift_scale", .12), wall_drift)
    p.op("Add", stage4x, wall_drift, fall_end_x)
    p.select(wall_drop, z, stage4x, fall_end_x, fall_end_x)

    # Select durations for the same five phases rather than compiling nine copies.
    d1, d2, d3, d4, d5 = [p.var("d" + str(i), 10.0) for i in range(1, 6)]
    ground_duration, fixed_duration = p.var("ground_duration"), p.var("fixed_ground_duration")
    style_walk, style_run = p.var("style_walk_last", 2.0), p.var("style_run_last", 3.0)
    p.select(held["ground_style"], style_walk, p.var("walk_duration", 10.0), p.var("run_duration", 5.0), fixed_duration)
    rate_left, rate_right = p.var("creep_rate_left", CREEP_SPEED / SPAN), p.var("creep_rate_right", -CREEP_SPEED / SPAN)
    p.select(side, z, rate_left, rate_right, diff)
    p.op("Divide", distance, diff, ground_duration)
    p.emit("Clamp", srcVar1=ground_duration, min=CREEP_MIN_DURATION, max=1_000_000, resultVar=ground_duration)
    p.select(held["ground_style"], style_run, fixed_duration, ground_duration, ground_duration)
    p.op("Subtract", goal_x, fall_end_x, distance)
    p.select(goal_x, fall_end_x, rate_right, rate_left, diff)
    p.op("Divide", distance, diff, d5)
    p.emit("Clamp", srcVar1=d5, min=CREEP_MIN_DURATION, max=1_000_000, resultVar=d5)
    p.select(held["ground_style"], style_run, fixed_duration, d5, d5)
    # A gesture inserts a single pause in the first ground leg. A resting route
    # can hug in place; trips require actual ground movement.
    trip_duration, gesture_duration = p.var("trip_duration"), p.var("gesture_duration")
    p.select(move, z, z, p.var("trip_seconds", poses["trip_left"]["frames"] / poses["trip_left"]["fps"]), trip_duration)
    p.select(held["ground_style"], style_run, trip_duration, z, trip_duration)
    p.select(held["gesture_pick"], one, p.var("hug_seconds", poses["hug"]["frames"] / poses["hug"]["fps"]), z, gesture_duration)
    p.select(held["gesture_pick"], z, trip_duration, gesture_duration, gesture_duration)
    gesture_start, gesture_end = p.var("gesture_start"), p.var("gesture_end")
    p.op("Multiply", held["range"], p.var("gesture_fraction", .5), gesture_start)
    p.select(move, z, p.var("rest_gesture_span", 16.0), ground_duration, diff)
    p.op("Multiply", gesture_start, diff, gesture_start)
    p.op("Add", gesture_start, gesture_duration, gesture_end)
    p.op("Add", ground_duration, gesture_duration, d1)
    p.select(flags["floor"], z, p.var("climb_duration", 10.0), p.var("floor_pause", 3.0), d2)
    wall_pause = p.var("wall_pause")
    p.op("Multiply", held["pause"], p.var("wall_pause_scale", .5), wall_pause)
    p.select(flags["perimeter"], z, wall_pause, p.var("ceiling_cross", 18.0), d3)
    p.select(flags["ceiling"], z, d3, p.var("ceiling_half", 13.0), d3)
    p.select(flags["floor"], z, d3, z, d3)
    p.select(drop, z, p.var("descent_duration", 10.0), p.var("fall_duration", 1.4), d4)
    p.select(flags["floor"], z, d4, z, d4)
    p.select(flags["ceiling"], z, d5, p.var("landing_duration", .5), d5)
    boundaries = [z]
    for index, duration in enumerate((d1, d2, d3, d4, d5), 1):
        boundary = p.var("boundary" + str(index))
        p.op("Add", boundaries[-1], duration, boundary)
        boundaries.append(boundary)
    route_duration, scaled, new_end = p.var("route_duration"), p.var("scaled_duration"), p.var("new_end")
    p.select(move, z, p.var("rest_duration", 16.0), boundaries[-1], route_duration)
    p.op("Divide", route_duration, held["pace"], scaled)
    p.op("Add", start, held["pause"], new_end)
    p.op("Add", new_end, scaled, new_end)
    p.select(renew, z, end, new_end, end)
    age = p.var("age")
    p.op("Subtract", time, start, age)
    p.op("Subtract", age, held["pause"], age)
    p.op("Multiply", age, held["pace"], age)
    # new_end has already been copied into the persistent end variable.
    motion_age, gesture_active = new_end, p.var("gesture_active")
    p.op("Subtract", age, gesture_duration, motion_age)
    p.select(gesture_end, age, motion_age, gesture_start, motion_age)
    p.select(gesture_start, age, motion_age, age, motion_age)
    p.select(gesture_start, age, one, z, gesture_active)
    p.select(gesture_end, age, z, gesture_active, gesture_active)

    # Moving poses share four clocks; floor rests use a separate clip pool.
    phases = {}
    for fps in (3, 5, 8, 12):
        clock, phase = p.var(f"clock{fps}"), p.var(f"phase{fps}")
        p.emit("LinearRamp", rate=fps, initialValue=0, resultVar=clock)
        p.emit("WrapMinMax", srcVar1=clock, minVal=0, maxVal=4, resultVar=phase)
        p.emit("Int", srcVar1=phase, resultVar=phase)
        phases[fps] = phase
    frames = {}
    for name, pose in poses.items():
        if name in ("idle_left", "idle_right", "sit", "rest_pool") or pose.get("oneshot"):
            continue
        frame = p.var("frame_" + name, float(pose["frame_base"]))
        frames[name] = frame
        if pose["frames"] > 1:
            base = p.var("base_" + name, float(pose["frame_base"]))
            phase = phases[pose["fps"]]
            p.op("Add", base, phase, frame)
    ground_left, ground_right = p.var("ground_left_frame"), p.var("ground_right_frame")
    for dest, suffix in ((ground_left, "left"), (ground_right, "right")):
        p.select(held["ground_style"], style_run, frames["run_" + suffix], frames["creep_" + suffix], dest)
        p.select(held["ground_style"], style_walk, frames["walk_" + suffix], dest, dest)
    rest = p.var("rest_frame")
    pool_clock, pool_phase, pool_block = p.var("pool_clock"), p.var("pool_phase"), p.var("pool_block")
    p.op("Subtract", time, start, pool_clock)
    p.op("Multiply", pool_clock, p.var("pool_fps", 4.0), pool_clock)
    p.emit("WrapMinMax", srcVar1=pool_clock, minVal=0, maxVal=8, resultVar=pool_phase)
    p.emit("Int", srcVar1=pool_phase, resultVar=pool_phase)
    p.op("Multiply", held["rest_pose"], p.var("pool_clip_size", 8.0), pool_block)
    p.op("Add", pool_block, p.var("pool_base", float(poses["rest_pool"]["frame_base"])), rest)
    p.op("Add", rest, pool_phase, rest)
    outward, wall_frame, ceiling_frame, hold_frame, fall_frame, land_frame = [p.var(n) for n in (
        "outward_frame", "wall_frame", "ceiling_frame", "hold_frame", "fall_frame", "land_frame")]
    p.select(side, z, ground_left, ground_right, outward)
    for dest, left, right in (
        (wall_frame, "climb_left", "climb_right"), (ceiling_frame, "ceiling_right", "ceiling_left"),
        (hold_frame, "wall_hold_left", "wall_hold_right"), (fall_frame, "fall_right", "fall_left"),
        (land_frame, "land_right", "land_left")):
        p.select(side, z, frames[left], frames[right], dest)
    f2, f3, f4, f5, other_wall = [p.var(n) for n in ("f2", "f3", "f4", "f5", "other_wall_frame")]
    p.select(side, z, frames["climb_right"], frames["climb_left"], other_wall)
    p.select(flags["floor"], z, wall_frame, rest, f2)
    p.select(flags["wall"], z, ceiling_frame, hold_frame, f3)
    p.select(flags["perimeter"], z, wall_frame, other_wall, f4)
    p.select(drop, z, f4, fall_frame, f4)
    hang_frame = p.var("hang_frame")
    p.select(side, z, frames["hang_right"], frames["hang_left"], hang_frame)

    x, y, frame = p.var("output_x"), p.var("output_y"), p.var("output_frame")
    p.select(boundaries[-1], age, goal_x, hx, x)
    p.copy(gy, y)
    p.copy(rest, frame)
    p.select(goal_x, fall_end_x, ground_right, ground_left, f5)
    p.select(flags["ceiling"], z, f5, land_frame, f5)
    phases_geometry = (
        ((hx, gy), (target_x, gy), outward),
        ((target_x, gy), (target_x, upper_y), f2),
        ((climb_top_x, stage3y), (stage3x, stage3y), f3),
        ((stage4x, stage3y), (fall_end_x, gy), f4),
        ((fall_end_x, gy), (goal_x, gy), f5),
    )
    scratch1, scratch2, active = [p.var(n) for n in ("stage_a", "stage_b", "stage_active")]
    # Stage flags are consumed before interpolation; reuse their scratch slots
    # for progress and arithmetic. Keep active and both coordinates separate.
    progress = scratch1
    curve = value = delta = fast_progress = hang_progress = scratch2
    top_pose = f3
    for index, (begin, finish, pose) in enumerate(phases_geometry):
        t0, t1 = boundaries[index:index + 2]
        p.select(t0, age, one, z, scratch1)
        p.select(t1, age, z, one, scratch2)
        p.op("Multiply", scratch1, scratch2, active)
        p.op("Subtract", motion_age if index == 0 else age, t0, progress)
        duration = (d1, d2, d3, d4, d5)[index]
        if index == 0:
            duration = ground_duration
        p.op("Divide", progress, duration, progress)
        p.emit("Clamp", srcVar1=progress, min=0, max=1, resultVar=progress)
        if index == 2:
            # Ceiling trips reach the sampled point and hang for the last quarter.
            p.op("Multiply", progress, p.var("top_travel_rate", 4 / 3), fast_progress)
            p.select(flags["ceiling"], z, progress, fast_progress, progress)
            p.emit("Clamp", srcVar1=progress, min=0, max=1, resultVar=progress)
            p.select(flags["ceiling"], z, z, progress, hang_progress)
            p.select(hang_progress, p.var("hang_threshold", .999), f3, hang_frame, top_pose)
            pose = top_pose
        if index == 3:
            p.op("Multiply", progress, progress, curve)
            p.select(drop, z, progress, curve, progress)
        for out, a, b in ((x, begin[0], finish[0]), (y, begin[1], finish[1])):
            if a == b:
                p.select(active, z, out, a, out)
            else:
                p.op("Subtract", b, a, delta)
                p.op("Multiply", delta, progress, value)
                p.op("Add", a, value, value)
                p.select(active, z, out, value, out)
        p.select(active, z, frame, pose, frame)
    # Nonmoving routes share one final mask rather than five stage masks.
    p.select(move, z, hx, x, x)
    p.select(move, z, gy, y, y)
    p.select(move, z, rest, frame, frame)
    # One-shot frames use age relative to their window, so they neither repeat
    # through a whole rest nor interrupt wall climbing or ceiling motion.
    gesture_frame, gesture_phase = scratch2, scratch1
    p.select(side, z, p.var("trip_left_base", float(poses["trip_left"]["frame_base"])),
             p.var("trip_right_base", float(poses["trip_right"]["frame_base"])), gesture_frame)
    p.select(held["gesture_pick"], z, gesture_frame,
             p.var("hug_base", float(poses["hug"]["frame_base"])), gesture_frame)
    p.op("Subtract", age, gesture_start, gesture_phase)
    p.op("Multiply", gesture_phase, p.var("gesture_fps", 8.0), gesture_phase)
    clip_last = max(poses[name]["frames"] for name in ("trip_left", "trip_right", "hug")) - 1
    p.emit("Clamp", srcVar1=gesture_phase, min=0, max=clip_last, resultVar=gesture_phase)
    p.emit("Int", srcVar1=gesture_phase, resultVar=gesture_phase)
    p.op("Add", gesture_frame, gesture_phase, gesture_frame)
    p.select(gesture_active, z, frame, gesture_frame, frame)
    center, scale, translate = p.var("center", "[0 0]"), p.var("scale", f"[{width / SPAN} {HEIGHT / SPAN}]"), p.var("translate", "[0 0]")
    p.copy(x, translate + "[0]")
    p.copy(y, translate + "[1]")
    p.copy(frame, "$frame")
    p.emit("TextureTransform", centerVar=center, scaleVar=scale, translateVar=translate, resultVar="$basetexturetransform")
    p.copy(time, previous)
    p.deduplicate_constants()
    # Native L4D2 also rejects exactly 256 proxies (2026-10-12 duo check).
    assert len(p.proxies) <= 255, len(p.proxies)
    assert len(p.values) <= TESTED_PARAMETER_BUDGET, ("Compact material parameters before shipping", len(p.values))
    return p


def material_text(program, namespace="neuropet_client"):
    settings = "\n".join(f'    "{key}" "{value}"' for key, value in program.values.items())
    blocks = []
    for item in program.proxies:
        values = "\n".join(f'            "{key}" "{value}"' for key, value in item["values"].items())
        blocks.append(f'        "{item["name"]}"\n        {{\n{values}\n        }}')
    return f'''"UnlitGeneric"
{{
    "$basetexture" "vgui/{namespace}/poses"
    "$translucent" "1"
    "$vertexcolor" "1"
    "$vertexalpha" "1"
    "$ignorez" "1"
    "$nolod" "1"
    "$alpha" "1"
    "$frame" "0"
{settings}
    "Proxies"
    {{
{chr(10).join(blocks)}
    }}
}}
'''
