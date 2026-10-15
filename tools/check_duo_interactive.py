"""Regression checks for unequal drawing rates and analytic client duo motion."""
from pathlib import Path
import argparse
import json
import sys

sys.dont_write_bytecode = True
WORK = Path(__file__).resolve().parent
PROJECT = WORK.parent
sys.path.insert(0, str(WORK))
from client_behavior import material_text
from check_client_behavior import ProxyVM
from duo_pair_graph import Graph
from duo_perimeter_behavior import compile_pair
from build_duo_interactive import configure_scene, SCENARIOS

parser = argparse.ArgumentParser()
parser.add_argument("--base-dist", type=Path, default=PROJECT / "dist")
parser.add_argument("--output", type=Path, default=PROJECT / "dist/interactive-behavior-checks.json")
args = parser.parse_args()
MANIFEST = json.loads((args.base_dist / "client-build-manifest.json").read_text(encoding="utf-8"))
SHARED = ("$np_previous_time", "$np_pair_start", "$np_pair_end", "$np_seek_duration", "$np_giver",
          "$np_pair_s0", "$np_pair_s1", "$np_dock", "$np_social_deadline", "$np_active_before", "$np_approach_right", "$np_approach_speed")
ACTOR = tuple(f"$np_a{i}_{key}" for i in (0, 1) for key in ("s", "goal_s", "mode", "random", "end", "start"))


def vm(actor, scene=None, compact=True):
    original = Graph.compact
    if not compact:
        Graph.compact = lambda self: 0
    try:
        p = compile_pair(MANIFEST["poses"], MANIFEST["aspect"], actor)
        configure_scene(p, scene)
        return ProxyVM(material_text(p)), p.meta
    finally:
        Graph.compact = original


def snapshot(machine):
    return tuple(machine.values[key] for key in SHARED + ACTOR)


def point(machine):
    return tuple(24-value*96 for value in machine.values["$np_translate"])


def hug_frame(frame):
    return 174 <= frame <= 201 or 203 <= frame <= 230


def original_hug_frame(frame):
    return frame - 29 if frame >= 203 else frame


def check_pair(machines, time):
    assert snapshot(machines[0]) == snapshot(machines[1]), (time, "Coordinator drift", snapshot(machines[0]), snapshot(machines[1]))
    for i, machine in enumerate(machines):
        frame = int(machine.values["$frame"])
        assert 0 <= frame <= 230
        x, y = point(machine)
        assert -10.1 <= x <= 480*MANIFEST["aspect"]-37.9 and -20.1 <= y <= 432.1, (time,i,x,y)
        if hug_frame(frame):
            assert int(machines[1-i].values["$frame"]) == 202, (time, "Hug ghost", [int(m.values["$frame"]) for m in machines])
            assert abs(point(machines[1-i])[1]-432) < .01


def scene_test(scene):
    machines = [vm(i, scene)[0] for i in (0,1)]
    reference = vm(0, scene, False)[0]
    giver = 0 if "neuro" in scene else 1
    frames, hugging, seen, previous = set(), [], False, None
    for step in range(660):
        t = step/30
        for machine in machines:
            machine.bind(t)
        reference.bind(t)
        check_pair(machines, t)
        assert snapshot(machines[0]) == snapshot(reference), (t,"Optimizer changed state")
        if hug_frame(int(machines[giver].values["$frame"])):
            frames.add(original_hug_frame(int(machines[giver].values["$frame"])))
            hugging.append(t)
            seen = True
        elif seen:
            assert all(int(m.values["$frame"]) != 202 for m in machines), "Receiver did not return"
        current = [point(m) for m in machines]
        if previous:
            assert max(abs(a-b) for p,q in zip(current,previous) for a,b in zip(p,q)) < 4, (scene,t,"Position jumped",current,previous)
        previous = current
    assert len(frames) == 28 and len(hugging) >= 119
    duration = machines[0].values["$np_seek_duration"]
    expected = 0 if scene.startswith("encounter") else 56/30 if scene.startswith("short") else 356/60
    assert abs(duration-expected) < .001, (scene,duration,expected)
    return {"scene":scene,"frames":28,"hug_seconds_observed":len(hugging)/30,"first_hug":hugging[0],"receiver_hidden_and_restored":True}


def skew_test(label, skipped=(), cadence=1, scene=None, seconds=300):
    machines = [vm(i,scene)[0] for i in (0,1)]
    previous_pair, hugs, comparisons = False, 0, 0
    for step in range(seconds*60):
        t=step/60
        machines[1].bind(t)
        if step in skipped or step%cadence:
            continue
        machines[0].bind(t)
        check_pair(machines,t)
        comparisons += 1
        pair=bool(machines[0].values["$np_active_before"])
        if pair and not previous_pair:
            hugs += 1
        previous_pair=pair
        if step%137 == 0:
            before=snapshot(machines[0])
            machines[0].bind(t)
            assert snapshot(machines[0]) == before, (label,t,"Extra bind changed state")
    assert hugs > 0, (label,"No interactions covered")
    return {"case":label,"seconds":seconds,"comparisons":comparisons,"joint_actions":hugs,"coordinator_and_hug_visibility":"passed"}


def speeds_and_reset():
    speeds={}
    for name,u in (("walk",.4),("run",.7),("creep",.9)):
        machine=vm(0)[0]
        for i in (0,1):
            for key,val in {"s":4.0,"goal_s":4.0,"mode":1.0,"random":u,"start":0.0,"end":100000.0}.items():
                machine.values[f"$np_a{i}_{key}"]=val
        machine.values["$np_social_deadline"]=1000000.0
        machine.bind(0)
        start=point(machine)
        machine.bind(1)
        speeds[name]=abs(point(machine)[0]-start[0])
    assert abs(speeds["creep"]-8)<.01 and abs(speeds["walk"]-30)<.01 and abs(speeds["run"]-60)<.01
    machines=[vm(i)[0] for i in (0,1)]
    for step in range(18000):
        t=step/30
        for machine in machines:
            machine.bind(t)
        check_pair(machines,t)
    for t in (0,.033,.066,1,3):
        for machine in machines:
            machine.bind(t)
        check_pair(machines,t)
    return {"floor_units_per_second":speeds,"ten_minute_paired_states_and_clock_reset":"passed"}


def approaches_and_roles():
    cases, roles = [], []
    for left in (False, True):
        for gap in (10,25,26,36,55,80,167.9,168,168.1,380,700):
            scene="short-neuro-left" if left else "short-evil"
            machines=[vm(i,scene)[0] for i in (0,1)]
            giver=0 if left else 1
            positions=[50.0,50.0+gap]
            for machine in machines:
                for i,x in enumerate(positions):
                    machine.values[f"$np_a{i}_s"]=(x+10)/96
                    machine.values[f"$np_a{i}_goal_s"]=(x+10)/96
                machine.bind(0)
                machine.bind(1)
            check_pair(machines,1)
            duration=machines[0].values["$np_seek_duration"]
            if gap <= 25:
                assert duration == 0 and hug_frame(int(machines[giver].values["$frame"])), (gap,left,duration,[m.values["$frame"] for m in machines])
                continue
            speed=30 if gap-24 <= 144 else 60
            assert abs(duration-(gap-24)/speed)<.001
            start=point(machines[giver])
            delta=min(.02,duration/4)
            for machine in machines:
                machine.bind(1+delta)
            check_pair(machines,1+delta)
            end=point(machines[giver])
            measured=abs(end[0]-start[0])/delta
            assert abs(measured-speed)<.08,(gap,left,measured,speed)
            assert (end[0]>start[0]) == left, (gap,left,start,end)
            base=(4 if speed==30 else 38)+(4 if left else 0)
            frame=int(machines[giver].values["$frame"])
            assert base <= frame < base+4,(gap,left,frame,base)
            cases.append({"gap":gap,"from":"left" if left else "right","speed":measured,
                          "seconds":duration,"animation":"walk" if speed==30 else "run"})
    # Successful lottery interval [0,.6] is divided into equal halves. Both
    # roles are selectable with either physical ordering of the two pets.
    for sample in (.05,.15,.25,.35,.45,.55):
        program=compile_pair(MANIFEST["poses"],MANIFEST["aspect"],0)
        configure_scene(program,"short-neuro-left")
        salt=next(key for key,value in program.values.items() if value == .369)
        program.values[salt]=32+sample-31.731
        machine=ProxyVM(material_text(program))
        machine.bind(0)
        machine.bind(1)
        assert machine.values["$np_active_before"]
        roles.append(int(machine.values["$np_giver"]))
    assert roles == [0,0,0,1,1,1]
    # This is deterministic simulation, not an empirical probability guarantee.
    machine=vm(0)[0]
    counts=[0,0]
    active=False
    opening=[]
    for second in range(14400):
        machine.bind(second)
        current=bool(machine.values["$np_active_before"])
        if current and not active:
            giver=int(machine.values["$np_giver"])
            counts[giver]+=1
            if second<600:
                opening.append({"second":second,"giver":giver})
        active=current
    assert all(counts), counts
    return {"distance_speed_animation_cases":cases,"conditional_role_intervals":roles,
            "four_hour_simulation_initiators":{"neuro":counts[0],"evil":counts[1]},
            "first_ten_minutes":opening}


def main():
    record={"compiler":[vm(i)[1] for i in (0,1)],
            "scenes":[scene_test(s) for s in SCENARIOS],
            "unequal_bindings":[skew_test("miss one binding at first transition",{180}),
                               skew_test("miss ten bindings at first transition",range(180,190)),
                               skew_test("miss bindings during floor movement",range(650,666)),
                               skew_test("15 fps versus 60 fps",cadence=4),
                               skew_test("receiver not updated during hidden hug",range(430,650),scene="seek-evil",seconds=22)],
            "motion":speeds_and_reset(),"approaches":approaches_and_roles()}
    assert all(item["proxies"] <= 255 and item["parameters"] <= 128 for item in record["compiler"])
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps(record,ensure_ascii=False))


if __name__ == "__main__":
    main()
