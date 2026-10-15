"""Analytic motion and a shared decision clock for the client duo."""
from duo_pair_graph import Graph, FLOOR, TOP, SPAN


def compile_pair(poses, aspect, render_actor, diagnostic=None):
    g = Graph()
    z, one = g.c(0), g.c(1)
    width = 480 * aspect
    length, height = (width - 28) / SPAN, (FLOOR - TOP) / SPAN
    perimeter = 2 * (length + height)
    raw = g.keep("time")
    g.emit("LinearRamp", rate=1, initialValue=0, resultVar=raw)
    clock = g.calc("Int", raw)
    previous = g.keep("previous_time", -1)
    backwards = g.choose(previous, clock, z, one)
    end, start = g.keep("pair_end", -1), g.keep("pair_start")
    giver, duration = g.keep("giver"), g.keep("seek_duration", 1)
    approach_right = g.keep("approach_right")
    approach_speed = g.keep("approach_speed", 30 / SPAN)
    pair_s = [g.keep("pair_s" + str(i)) for i in (0, 1)]
    dock = g.keep("dock")
    social = g.keep("social_deadline", 18)
    active_before = g.keep("active_before")
    g.select(backwards, z, end, g.c(-1), end)
    g.select(backwards, z, social, g.c(18), social)
    active = g.le(raw, end)
    ordinary = g.sub(one, active)
    resumed = g.mul(active_before, ordinary)

    def fold(s):
        horizontal = g.sub(g.clamp(s, 0, length), g.clamp(g.sub(s, g.c(length + height)), 0, length))
        x = g.sub(g.c(34 / SPAN), horizontal)
        y = g.add(g.c(-4.25), g.sub(g.clamp(g.sub(s, g.c(length)), 0, height),
                                    g.clamp(g.sub(s, g.c(2 * length + height)), 0, height)))
        return x, y

    actors = []
    for i, fraction in enumerate((.3, .7)):
        initial_s = (width * fraction - 14) / SPAN
        a = {key: g.keep(f"a{i}_{key}", value) for key, value in {
            "s": initial_s, "goal_s": initial_s,
            "mode": 0, "random": .5, "end": 3, "start": 0}.items()}
        due = g.mul(g.le(a["end"], clock), ordinary)
        renew = g.choose(due, z, g.choose(resumed, z, backwards, one), one)
        joint_end_s = g.choose(giver, z, dock if i == 0 else pair_s[1], pair_s[0] if i == 0 else dock)
        g.select(due, z, a["s"], a["goal_s"], a["s"])
        g.select(resumed, z, a["s"], joint_end_s, a["s"])
        g.select(backwards, z, a["s"], g.c(initial_s), a["s"])
        anchor = g.choose(resumed, z, a["end"], end)
        anchor = g.choose(backwards, z, anchor, z)
        sample = g.noise(clock, anchor, .371 + i * .413)
        g.select(renew, z, a["random"], sample, a["random"])
        u = a["random"]
        v = g.calc("Frac", g.mul(u, g.c(97.131)))
        a["direction"] = g.choose(v, g.c(.5), g.c(-1), one)
        a["style"] = u
        a["rest"] = g.calc("Int", g.mul(v, g.c(7.9999)))
        origin_floor = g.le(a["s"], g.c(length))
        # Share the rare-action branch across surfaces to stay below the native
        # proxy budget. Weights remain floor 5% trip / 15% rest / 80% move,
        # and other surfaces 5% fall / 10% rest / 85% move.
        special = g.choose(origin_floor, z, g.c(3), g.c(2))
        rest_limit = g.choose(origin_floor, z, g.c(.15), g.c(.2))
        mode = g.choose(u, g.c(.05), special, g.choose(u, rest_limit, z, one))
        # Decisions share the same clock and scheduled phase origins. A resumed
        # phase may start at an exact fractional approach-end time.
        period = g.calc("Int", g.add(g.c(6), g.mul(u, g.c(14))))
        period = g.choose(mode, one, period, g.c(4))
        g.select(renew, z, a["mode"], mode, a["mode"])
        g.select(renew, z, a["start"], anchor, a["start"])
        g.select(renew, z, a["end"], g.add(anchor, period), a["end"])
        moving = g.choose(a["mode"], one, a["mode"], z)
        a["fall"] = g.choose(a["mode"], g.c(2), z, one)
        speed = g.choose(u, g.c(.6), g.c(30 / SPAN), g.choose(u, g.c(.8), g.c(60 / SPAN), g.c(8 / SPAN)))
        speed = g.choose(origin_floor, z, g.c(25 / SPAN), speed)
        signed = g.mul(g.mul(a["direction"], moving), speed)
        span = g.sub(a["end"], a["start"])

        def at(elapsed):
            return g.calc("WrapMinMax", g.add(a["s"], g.mul(signed, elapsed)), minVal=0, maxVal=perimeter)

        future_s = at(span)
        # A falling phase ends on the floor below its exact phase origin.
        landing_s = g.sub(g.clamp(a["s"], 0, length), g.clamp(g.sub(a["s"], g.c(length + height)), 0, length))
        g.copy(g.choose(a["fall"], z, future_s, landing_s), a["goal_s"])
        a["age"] = g.sub(clock, a["start"])
        sample_s = at(g.clamp(a["age"], 0, span))
        a["sample_s"] = sample_s
        a["floor"] = g.mul(g.le(sample_s, g.c(length)), g.le(a["mode"], one))
        a["floor"] = g.mul(a["floor"], g.le(clock, a["end"]))
        a["raw_age"] = g.sub(raw, a["start"])
        if i == render_actor:
            a["render_s"] = at(g.clamp(a["raw_age"], 0, span))
        actors.append(a)

    both_floor = g.mul(actors[0]["floor"], actors[1]["floor"])
    separation = g.absolute(g.sub(actors[0]["sample_s"], actors[1]["sample_s"]))
    ready = g.mul(ordinary, g.le(social, clock))
    eligible = g.mul(ready, both_floor)
    lottery = g.noise(clock, clock, .817)
    trigger = g.mul(eligible, g.le(lottery, g.c(.6)))
    travel = g.sub(separation, g.c(24 / SPAN))
    seek_speed = g.choose(travel, g.c(144 / SPAN), g.c(30 / SPAN), g.c(60 / SPAN))
    # A tiny tolerance keeps exactly 25 units inside the encounter range after
    # float32 coordinate subtraction in the native material pipeline.
    seek_time = g.choose(separation, g.c(25.01 / SPAN), z, g.calc("Divide", travel, seek_speed))
    # A rejected opportunity waits before trying again, even if pets remain close.
    g.select(eligible, z, social, g.add(clock, g.c(24)), social)
    # The trigger accepts [0, .6]; divide that interval evenly between pets.
    # Selecting a role from positions used to favor the initial right-hand pet.
    role = g.choose(lottery, g.c(.3), z, one)
    g.select(trigger, z, giver, role, giver)
    source_s = g.choose(giver, z, actors[0]["sample_s"], actors[1]["sample_s"])
    receiver_s = g.choose(giver, z, actors[1]["sample_s"], actors[0]["sample_s"])
    g.select(trigger, z, approach_right, g.le(source_s, receiver_s), approach_right)
    g.select(trigger, z, approach_speed, seek_speed, approach_speed)
    offset = g.choose(approach_right, z, g.c(24 / SPAN), g.c(-24 / SPAN))
    goal = g.choose(seek_time, z, source_s, g.add(receiver_s, offset))
    for key, value in ((duration, seek_time), (dock, goal), (pair_s[0], actors[0]["sample_s"]),
                       (pair_s[1], actors[1]["sample_s"]), (start, clock),
                       (end, g.add(clock, g.add(seek_time, g.c(4))))):
        g.select(trigger, z, key, value, key)
    g.select(trigger, z, social, g.add(end, g.c(45)), social)
    pair_age = g.sub(raw, start)
    final_active = g.le(raw, end)
    progress = g.clamp(g.calc("Divide", pair_age, duration))
    original_s = g.choose(giver, z, pair_s[0], pair_s[1])
    journey = g.sub(dock, original_s)
    seeker_s = g.add(original_s, g.mul(journey, progress))
    hugging = g.mul(final_active, g.le(duration, pair_age))
    seeking = g.sub(final_active, hugging)
    g.copy(final_active, active_before)
    g.copy(clock, previous)

    a = actors[render_actor]
    x, y = fold(a["render_s"])
    falling_progress = g.clamp(g.calc("Divide", a["raw_age"], g.c(1.4)))
    falling_y = g.add(y, g.mul(g.sub(g.c(-4.25), y), g.mul(falling_progress, falling_progress)))
    y = g.choose(a["fall"], z, y, falling_y)
    joint_s = g.choose(giver, z, seeker_s if render_actor == 0 else pair_s[1],
                       pair_s[0] if render_actor == 0 else seeker_s)
    joint_x = g.sub(g.c(34 / SPAN), joint_s)
    x = g.choose(final_active, z, x, joint_x)
    y = g.choose(final_active, z, y, g.c(-4.25))
    facing = g.le(z, a["direction"])
    ceiling = g.le(g.c((24 - TOP - .1) / SPAN), y)
    facing = g.choose(ceiling, z, facing, g.sub(one, facing))
    facing = g.choose(seeking, z, facing, approach_right)
    side = g.le(x, g.c((48 - width / 2) / SPAN))
    on_floor = g.le(y, g.c(-4.249))
    seek_style = g.choose(approach_speed, g.c(30 / SPAN), g.c(.4), g.c(.7))
    style = g.choose(seeking, z, a["style"], seek_style)
    rate = g.choose(style, g.c(.6), g.c(8), g.choose(style, g.c(.8), g.c(12), g.c(3)))
    rate = g.choose(on_floor, z, g.c(5), rate)
    phase = g.calc("WrapMinMax", g.mul(raw, rate), minVal=0, maxVal=4)
    rest_phase = g.calc("WrapMinMax", g.mul(raw, g.c(4)), minVal=0, maxVal=8)
    ground_base = g.choose(style, g.c(.6), g.c(4), g.choose(style, g.c(.8), g.c(38), g.c(46)))
    ground_base = g.add(ground_base, g.mul(facing, g.c(4)))
    wall_base = g.add(g.c(12), g.mul(side, g.c(4)))
    top_base = g.add(g.c(20), g.mul(facing, g.c(4)))
    motion_base = g.choose(ceiling, z, wall_base, top_base)
    motion = g.add(g.choose(on_floor, z, motion_base, ground_base), phase)
    rest = g.add(g.add(g.c(54), g.mul(a["rest"], g.c(8))), rest_phase)
    stationary = g.choose(ceiling, z, g.add(g.c(36), side), g.add(g.c(34), facing))
    stationary = g.choose(on_floor, z, stationary, rest)
    trip = g.add(g.add(g.c(118), g.mul(facing, g.c(28))), g.clamp(g.mul(a["raw_age"], g.c(8)), 0, 27))
    fall = g.choose(a["raw_age"], g.c(1.4), g.add(g.c(28), facing),
                    g.choose(a["raw_age"], g.c(1.9), g.add(g.c(30), facing), rest))
    frame = g.choose(a["mode"], g.c(2), trip, fall)
    frame = g.choose(a["mode"], one, motion, frame)
    frame = g.choose(a["mode"], z, stationary, frame)
    seeking_frame = g.choose(giver, z, motion if render_actor == 0 else rest, rest if render_actor == 0 else motion)
    frame = g.choose(seeking, z, frame, seeking_frame)
    hug_phase = g.clamp(g.mul(g.sub(pair_age, duration), g.c(8)), 0, 27)
    # Mirrored copies follow the unchanged blank frame at index 202.
    hug_frame = g.add(g.choose(approach_right, z, g.c(174), g.c(203)), hug_phase)
    own_hug = g.choose(giver, z, hug_frame if render_actor == 0 else g.c(202),
                        g.c(202) if render_actor == 0 else hug_frame)
    g.copy(g.choose(hugging, z, frame, own_hug), "$frame")
    translate = g.keep("translate", "[0 0]")
    g.copy(x, translate + "[0]")
    g.copy(y, translate + "[1]")
    g.emit("TextureTransform", centerVar=g.keep("center", "[0 0]"),
           scaleVar=g.keep("scale", f"[{width/SPAN} 5]"), translateVar=translate,
           resultVar="$basetexturetransform")
    scratch = g.compact()
    g.meta = {"proxies": len(g.proxies), "parameters": len(g.values), "scratch_registers": scratch,
              "coordinator": "analytic motion with shared integer decision clock"}
    return g
