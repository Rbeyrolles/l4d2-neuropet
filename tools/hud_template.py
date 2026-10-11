"""Read the stock HUD layout from a user's local game installation."""
from pathlib import Path
import hashlib

from read_vpk import read_entry

STOCK_PATH = "scripts/hudlayout.res"
# Matches L4D2's stock gameinfo.txt mount precedence. Addons are not consulted.
GAME_FOLDERS = ("update", "left4dead2_dlc3", "left4dead2_dlc2", "left4dead2_dlc1", "left4dead2")


def load_hud_template(game_root=None, template_path=None):
    """Return the layout text and a portable description of its provenance."""
    if template_path is not None:
        path = Path(template_path)
        data, source = path.read_bytes(), path.name
    elif game_root is not None:
        root = Path(game_root).expanduser().resolve()
        if root.name.lower() == "left4dead2" and (root / "gameinfo.txt").is_file():
            root = root.parent
        for folder in GAME_FOLDERS:
            loose = root / folder / STOCK_PATH
            if loose.is_file():
                data, source = loose.read_bytes(), f"{folder}/{STOCK_PATH}"
                break
            archive = root / folder / "pak01_dir.vpk"
            if not archive.is_file():
                continue
            try:
                data = read_entry(archive, STOCK_PATH)
                source = f"{folder}/pak01_dir.vpk:{STOCK_PATH}"
                break
            except KeyError:
                continue
        else:
            raise FileNotFoundError("Stock scripts/hudlayout.res was not found in the selected L4D2 installation")
    else:
        raise ValueError("Pass --game-root pointing to your L4D2 installation, or --hud-template with a locally extracted stock layout")
    text = data.decode("utf-8-sig").replace("\r\n", "\n")
    if '"Resource/HudLayout.res"' not in text or text.rfind("}") < 0:
        raise ValueError("The selected file does not look like L4D2's stock HUD layout")
    if '"NeuroPetClient_' in text:
        raise ValueError("Use the stock HUD layout, rather than a previously generated pet layout")
    return text, {"source": source, "sha256": hashlib.sha256(data).hexdigest()}
