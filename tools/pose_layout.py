"""Original pose names, source frames and timings shared by the builders."""

POSES = [
    ("idle_left", ["shime1"] * 40 + ["shime1w"] * 2, 8, False),
    ("idle_right", ["shime1"] * 40 + ["shime1w"] * 2, 8, True),
    ("walk_left", ["shime1a", "shime2", "shime1b", "shime3"], 8, False),
    ("walk_right", ["shime1a", "shime2", "shime1b", "shime3"], 8, True),
    ("climb_left", ["shime14", "shime12", "shime13", "shime12"], 5, False),
    ("climb_right", ["shime14", "shime12", "shime13", "shime12"], 5, True),
    ("ceiling_left", ["shime23", "shime24", "shime23", "shime25"], 5, False),
    ("ceiling_right", ["shime23", "shime24", "shime23", "shime25"], 5, True),
    ("fall_left", ["shime4"], 1, False),
    ("fall_right", ["shime4"], 1, True),
    ("land_left", ["shime18"], 1, False),
    ("land_right", ["shime18"], 1, True),
    ("sit", ["shime11"] * 40 + ["shime11w"] * 2, 8, False),
    ("cheer", ["shime1pat", "shime1", "shime1pat", "shime1"], 4, False),
]
