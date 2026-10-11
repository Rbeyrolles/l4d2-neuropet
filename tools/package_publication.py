"""Package source and player releases locally, without publishing to a service."""
from pathlib import Path
import argparse
import hashlib
import json
import zipfile
from promotion_assets import load_publication
from addon_metadata import addon_description

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED = {".git", ".venv", "venv", "__pycache__", "dist", "build", "client-only",
            "client-only-evil", "experiments", "publication"}


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


FOLDER_GUIDE = '''# Neuropet 发布文件夹：先看这里

项目制作署名：**Daisy, Shannon & Sol**。游戏内简介已改成英文＋中文，原画和配置作者的完整署名与许可保留在源码、工坊文案和 VPK 内。

## 这三个位置怎么用

| 位置 | 用途 |
| --- | --- |
| [github/](github/README.zh-CN.md) | 作为 GitHub 仓库根目录；上传其中的源码、素材、文档与许可，包括隐藏的 .gitignore 和 .gitattributes |
| workshop/neuro-sama/ | Neuro-sama 的独立工坊条目 |
| workshop/evil-neuro/ | Evil Neuro 的独立工坊条目 |

每个角色的工坊目录只有四个文件：VPK 是 Mod 内容，preview.jpg 是封面预览，TITLE.txt 是完整标题，description-bilingual.txt 是可粘贴的双语说明。两个角色无需互相依赖，每次只启用一版。

## 第一次发创意工坊

1. 登录准备发布的 Steam 账号，打开 Left 4 Dead 2 Authoring Tools 中的 Workshop Manager。工具文件为游戏安装目录下 bin/l4d2_workshop_manager.exe。[Valve 工具公告](https://store.steampowered.com/oldnews/9759)
2. 选择 Publish New Add-on，为一个角色创建独立条目。
3. 内容文件选该目录的 .vpk，Preview Image 选 preview.jpg。VPK 已经打包完成，无需重新打包。
4. 标题粘贴 TITLE.txt，说明粘贴 description-bilingual.txt。按界面现有选项选择与 HUD / UI 对应的分类。
5. 阅读上传界面条款，检查页面内容后由你提交。若工具提供可见性选择，可以先用私密状态检查页面再公开。
6. 保存生成的工坊地址，再发布另一角色。两者都发布后补上互相链接；另一角色不设为必需订阅项。

若工具打不开，可在 Steam 库的“工具”中更新／安装 Left 4 Dead 2 Authoring Tools。具体按钮与可选分类以当前工具界面为准。本次只准备本地文件，没有提交上传。

## GitHub

建立仓库后，把 github/ **里面的内容**放到仓库根目录，保留 LICENSE、NOTICE.md 和素材许可。源码中两份 README 的地址仍有待填项：填入真实网址后再公开。两个 VPK 可以另外作为 GitHub Releases 附件，不需要放进源码仓库。

上传稿已省略尚未确定的 GitHub、反馈和另一角色地址；这些链接可以发布后加到工坊说明。完整长稿保留在 github/docs/workshop/。上传使用精简稿，已按 UTF-8 字节检查，低于 Steam 接口的 8,000 字节说明上限。[Steam 文档](https://partner.steamgames.com/doc/api/ISteamRemoteStorage#Constants)

工坊条目归实际发布的 Steam 账号所有；游戏内创作者栏显示 Daisy, Shannon & Sol，工坊文案也保留这份项目署名。[Steam 条目所有者字段](https://partner.steamgames.com/doc/api/ISteamUGC#SteamUGCDetails_t)

## 使用提醒

不保证与第三方 HUD Mod 兼容，建议使用原版 HUD；宠物不显示时先停用其他 HUD Mod 并重启。只启用一个角色，避免手动安装和工坊订阅重复。更多内容见 [HUD 排障](github/docs/HUD_COMPATIBILITY.md) 和 [许可与素材署名](github/NOTICE.md)。

本次只更新游戏内简介与项目署名，动作材质、图集、HUD 布局、白边修复和封面保持上一版的字节内容。完整校验记录见 [源码验证记录](github/docs/RELEASE_CHECKS.md)。
'''


def package_folder(output, source_files, publication):
    if any(output.iterdir()):
        raise ValueError("Choose an empty output folder so existing release files are preserved")
    releases = []
    for stem, character in (("client", "neuron"), ("evil-client", "evil")):
        manifest_path = ROOT / "dist" / f"{stem}-build-manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        edition = publication["editions"][character]
        vpk = manifest_path.parent / manifest["vpk"]
        preview = ROOT / "dist/branding" / character / "preview.jpg"
        description = ROOT / edition["workshop_publish_description"]
        assert sha256(vpk) == manifest["sha256"]
        assert manifest["speed"] == 1 and manifest["diagnostic"] is None
        assert manifest["maintainer"] == publication["maintainer"]
        assert sha256(preview) == manifest["branding"]["workshop_preview_sha256"]
        assert preview.stat().st_size < 1_000_000
        assert len(edition["title"].encode("utf-8")) < 128
        assert len(description.read_bytes()) < 8000
        assert "待填" not in description.read_text(encoding="utf-8")
        target = output / "workshop" / edition["slug"]
        target.mkdir(parents=True)
        for source, name in ((vpk, vpk.name), (preview, "preview.jpg"), (description, "description-bilingual.txt")):
            (target / name).write_bytes(source.read_bytes())
        (target / "TITLE.txt").write_text(edition["title"] + "\n", encoding="utf-8")
        releases.append({"character": character, "vpk": f"workshop/{edition['slug']}/{vpk.name}",
                         "sha256": manifest["sha256"], "description_bytes": description.stat().st_size})
    for source in source_files:
        target = output / "github" / source.relative_to(ROOT)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(source.read_bytes())
    (output / "先看这里.zh-CN.md").write_text(FOLDER_GUIDE, encoding="utf-8")
    print(json.dumps({"layout": "folder", "output": str(output), "source_files": len(source_files), "releases": releases}))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=ROOT / "publication")
    parser.add_argument("--layout", choices=("folder", "archives"), default="folder",
                        help="Default: clean GitHub folder and two Workshop uploads; archives retains the old ZIP layout")
    args = parser.parse_args()
    output = args.output.expanduser().resolve()
    if output == ROOT:
        parser.error("Choose a separate output directory")
    output.mkdir(parents=True, exist_ok=True)
    source_zip = output / "l4d2-neuropet-source.zip"
    publication = load_publication(ROOT)
    source_files = []
    for path in sorted(ROOT.rglob("*")):
        relative = path.relative_to(ROOT)
        if not path.is_file() or path.is_symlink() or any(part in EXCLUDED for part in relative.parts):
            continue
        if path.is_relative_to(output) or path.suffix.lower() in (".pyc", ".vpk", ".vtf", ".log"):
            continue
        source_files.append(path)
    if args.layout == "folder":
        package_folder(output, source_files, publication)
        return
    releases = []
    for stem, character in (("client", "neuron"), ("evil-client", "evil")):
        manifest_path = ROOT / "dist" / f"{stem}-build-manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        vpk = manifest_path.parent / manifest["vpk"]
        assert sha256(vpk) == manifest["sha256"]
        assert manifest["speed"] == 1 and manifest["diagnostic"] is None
        release_zip = output / f"l4d2-neuropet-{character}-{manifest['version']}.zip"
        edition = publication["editions"][character]
        preview = ROOT / "dist/branding" / character / "preview.jpg"
        cover = ROOT / edition["cover"]
        assert sha256(preview) == manifest["branding"]["workshop_preview_sha256"]
        assert sha256(cover) == edition["cover_sha256"]
        title = edition["title"] + "\n"
        addon_intro = addon_description(publication, character) + "\n"
        description = ROOT / edition["workshop_description"]
        credits = ROOT / "assets/promotion/CREDITS.md"
        install = (f"{edition['title']} / version {manifest['version']}\n\n"
                   f"Project creators / 项目制作: {publication['maintainer']}\n\n"
                   "Place the VPK in Left 4 Dead 2/left4dead2/addons and enable it in Add-ons.\n"
                   "Enable only one pet edition. Restart the game after switching editions.\n"
                   "Compatibility with third-party HUD mods is not guaranteed; the stock HUD is recommended.\n"
                   "Both pet editions replace scripts/hudlayout.res. Conflicting HUDs may hide the pet or override HUD layout.\n"
                   "If the pet is missing, disable other HUD mods and restart L4D2; test in a local co-op map.\n"
                   "See docs/HUD_COMPATIBILITY.md for troubleshooting. No automatic HUD merging is included.\n"
                   "Servers may restrict client addons. No precise game-event reactions.\n\n"
                   "安装：将一个 VPK 放入 Left 4 Dead 2/left4dead2/addons，在附加内容列表中启用。\n"
                   "每次只启用一版宠物；切换角色后重启游戏，避免手动安装与工坊订阅重复。\n"
                   "不保证与第三方 HUD Mod 兼容，建议使用原版 HUD。宠物不显示时先停用其他 HUD Mod 并重启。\n"
                   "排障见 docs/HUD_COMPATIBILITY.md；当前版本不自动合并 HUD，也不提供精确的游戏事件联动。\n\n"
                   "Project code: MIT. Artwork and adaptations: CC BY-NC-SA 4.0.\n"
                   "Read NOTICE.md and the licenses embedded in the VPK.\n"
                   "Unofficial fan project. Character site: https://vedal.ai/\n")
        with zipfile.ZipFile(release_zip, "w", zipfile.ZIP_DEFLATED) as archive:
            archive.write(vpk, vpk.name)
            archive.write(ROOT / "LICENSE", "LICENSE")
            archive.write(ROOT / "NOTICE.md", "NOTICE.md")
            archive.write(ROOT / "docs/PUBLISHING.md", "docs/PUBLISHING.md")
            archive.write(ROOT / "docs/HUD_COMPATIBILITY.md", "docs/HUD_COMPATIBILITY.md")
            archive.write(cover, "cover.png")
            archive.write(preview, "workshop-preview.jpg")
            archive.write(description, "workshop-description-bilingual.txt")
            archive.write(credits, "COVER-CREDITS.md")
            archive.writestr("TITLE.txt", title)
            archive.writestr("ADDON_DESCRIPTION.txt", addon_intro)
            archive.write(manifest_path, manifest_path.name)
            archive.writestr("INSTALL.txt", install)
        workshop = output / "workshop" / edition["slug"]
        workshop.mkdir(parents=True, exist_ok=True)
        for source, name in ((vpk, vpk.name), (preview, "preview.jpg"), (cover, "cover.png"),
                             (description, "description-bilingual.txt"), (credits, "COVER-CREDITS.md")):
            (workshop / name).write_bytes(source.read_bytes())
        (workshop / "TITLE.txt").write_text(title, encoding="utf-8")
        (workshop / "addon-description-bilingual.txt").write_text(addon_intro, encoding="utf-8")
        releases.append({"character": character, "version": manifest["version"], "zip": release_zip.name,
                         "title": edition["title"], "maintainer": publication["maintainer"],
                         "addon_description": addon_intro.rstrip("\n"), "workshop_folder": f"workshop/{edition['slug']}",
                         "zip_sha256": sha256(release_zip), "vpk": vpk.name,
                         "vpk_sha256": manifest["sha256"], "zip_bytes": release_zip.stat().st_size,
                         "cover_sha256": sha256(cover), "preview_sha256": sha256(preview),
                         "preview_bytes": preview.stat().st_size})
    with zipfile.ZipFile(source_zip, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in source_files:
            archive.write(path, "l4d2-neuropet/" + path.relative_to(ROOT).as_posix())
    for path in [source_zip] + [output / release["zip"] for release in releases]:
        with zipfile.ZipFile(path) as archive:
            assert archive.testzip() is None
    sums = [f"{sha256(source_zip)}  {source_zip.name}"]
    sums.extend(f"{r['zip_sha256']}  {r['zip']}" for r in releases)
    sums.extend(f"{r['vpk_sha256']}  {r['workshop_folder']}/{r['vpk']}" for r in releases)
    sums.extend(f"{r['preview_sha256']}  {r['workshop_folder']}/preview.jpg" for r in releases)
    sums.extend(f"{r['cover_sha256']}  {r['workshop_folder']}/cover.png" for r in releases)
    (output / "SHA256SUMS.txt").write_text("\n".join(sums) + "\n", encoding="ascii")
    result = {"source_zip": source_zip.name, "source_sha256": sha256(source_zip),
              "source_files": len(source_files), "source_bytes": source_zip.stat().st_size,
              "zip_crc": "passed", "releases": releases}
    (output / "publication-manifest.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result))


if __name__ == "__main__":
    main()
