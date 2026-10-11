"""Read mascot action data and adapt a small floor-animation pool."""
from pathlib import Path
import xml.etree.ElementTree as ET

NS = {"m": "http://www.group-finity.com/Mascot"}
REST_CLIP_FRAMES = 8
REST_FPS = 4
TRIP_RECOVERY = (
    ("lose_balance", "trip1.png", 3),
    ("on_ground", "trip2.png", 12),
    ("push_up", "trip3.png", 5),
    ("sit_up", "shime11.png", 4),
    ("stand_ready", "shime1.png", 4),
)
TRIP_RECOVERY_FRAMES = sum(stage[2] for stage in TRIP_RECOVERY)
REST_ACTIONS = [
    ("Stand", "站立眨眼", True),
    ("Sit", "坐下眨眼", True),
    ("Sprawl", "趴下偷懒", True),
    ("SitAndLookUp", "坐着抬头", False),
    ("Wink", "俏皮 Wink", False),
    ("HeartHeartHeartAction", "比心", False),
    ("StandingBlush", "站着害羞", False),
    ("SitBlush", "坐着害羞", False),
]
EVIL_REST_ACTIONS = [
    ("Stand", "站立眨眼", True),
    ("Sit", "坐下眨眼", True),
    ("Sprawl", "趴下偷懒", True),
    ("SitAndLookUp", "坐着抬头", False),
    ("SitAffordance", "等抱抱", True),
    ("SprawlActionBlush", "趴着害羞", False),
    ("StandingBlush", "站着害羞", False),
    ("SitBlush", "坐着害羞", False),
]
CATALOG = [(name, label, "已加入", "地面休息") for name, label, _ in REST_ACTIONS] + [
    ("Run", "小跑", "已加入", "随机地面移动，比走路更快"),
    ("Creep", "趴着爬", "已加入", "按距离延长时间并限速，两张原姿势交替"),
    ("SitAndDangleLegs", "晃腿", "候选", "原锚点位于坐姿边沿，需单独适配"),
    ("Tripping", "绊倒与恢复", "已加入", "失衡、倒地停留、慢慢起身，再继续移动"),
    ("SitAffordance", "等待抱抱", "候选", "可复用姿势，原多角色互动不移植"),
    ("HugAction", "抱抱动作", "已加入", "偶尔播放一次原抱抱画面，再恢复原动作"),
]


def read_actions(pack):
    root = ET.parse(Path(pack) / "actions.xml").getroot()
    result = {}
    for action in root.findall(".//m:Action", NS):
        name = action.get("Name")
        animations = action.findall("m:Animation", NS)
        if not name or not animations:
            continue
        frames = []
        for pose in animations[0].findall("m:Pose", NS):
            image = pose.get("Image", "").lstrip("/")
            if image:
                frames.append({"image": image, "duration": max(1, int(pose.get("Duration", "1"))),
                               "anchor": pose.get("ImageAnchor", "64,128")})
        if frames:
            result[name] = {"name": name, "type": action.get("Type", ""),
                            "border": action.get("BorderType", ""), "frames": frames}
    return result


def sample_poses(source, count):
    """Resample source duration weights while retaining each frame's anchor."""
    total = sum(frame["duration"] for frame in source)
    samples = []
    for slot in range(count):
        position = (slot + .5) * total / count
        cursor = 0
        for frame in source:
            cursor += frame["duration"]
            if position < cursor:
                samples.append(frame)
                break
    assert len(samples) == count
    return samples


def action_clip(pack, name, count, mirror=False, source=None):
    """Pack an original action around the common 64,128 foot anchor."""
    from PIL import Image, ImageOps
    if source is None:
        source = read_actions(pack)[name]["frames"]
    samples = sample_poses(source, count)
    frames = []
    for pose in samples:
        with Image.open(Path(pack) / "img" / pose["image"]) as image:
            frame = image.convert("RGBA")
        ax, ay = (int(value) for value in pose["anchor"].split(","))
        if mirror:
            frame = ImageOps.mirror(frame)
            ax = frame.width - ax
        x, y = 128 - ax, 192 - ay
        assert x >= 0 and y >= 0 and x + frame.width <= 256 and y + frame.height <= 256, name
        padded = Image.new("RGBA", (256, 256))
        padded.paste(frame, (x, y))
        frames.append(padded)
    return frames, [pose["image"] for pose in samples]


def rest_pool(pack, pad_frame, actions_spec=REST_ACTIONS):
    from PIL import Image
    actions = read_actions(pack)
    frames, clips = [], []
    for action_name, label, blink in actions_spec:
        source = actions[action_name]["frames"]
        if blink:
            names = list(dict.fromkeys(f["image"] for f in source))
            images = [names[0]] * 7 + [names[1]]
        else:
            images = [frame["image"] for frame in sample_poses(source, REST_CLIP_FRAMES)]
        assert len(images) == REST_CLIP_FRAMES
        for image_name in images:
            with Image.open(Path(pack) / "img" / image_name) as image:
                frames.append(pad_frame(image.convert("RGBA")))
        clips.append({"action": action_name, "label": label, "images": images,
                      "block": len(clips), "fps": REST_FPS})
    return frames, clips
