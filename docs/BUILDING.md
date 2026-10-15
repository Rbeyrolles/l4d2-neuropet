# 构建和验证 / Building and validation

[中文](#中文) · [English](#english)

---

## 中文

本仓库在同一条主分支上维护三个构建目标：Neuro-sama 单宠、Evil Neuro 单宠和 Duo 双宠。三款共用角色素材、纹理处理、构建与验证工具及许可文件，成品分别构建、分别发布。

**玩家不需要读这一页。** 安装现成 VPK 不需要 Python 或任何构建依赖，见主 README 的「安装」。

### 先分清三样东西

| | 是什么 | 在哪里 |
| --- | --- | --- |
| **源码** | 构建器、Duo 行为编译器、验证工具、原始素材与许可、文档和少量验证记录 | 本仓库 |
| **成品 VPK** | 构建后玩家安装的客户端包，每款一个 | `dist/`（本地生成，不提交）；正式版附在 GitHub Releases，并分别上传到三个工坊条目 |
| **研究原型** | 早期服务端 VScript 实验，探索过状态机、物理和游戏事件 | `research/`；不属于任何一款客户端包，不参与构建，也不随 Release 发布 |

不要把整个源码目录当作 addon 放进游戏；玩家只需要对应的那一个 VPK。

### 三个构建目标

| 安装包 | 构建入口 | 发布配置 | 默认输出 |
| --- | --- | --- | --- |
| Neuro-sama 单宠 | `tools/build_client.py --character neuron` | `publication.json` | `dist/l4d2_neuropet_client.vpk` |
| Evil Neuro 单宠 | `tools/build_client.py --character evil` | `publication.json` | `dist/l4d2_neuropet_evil_client.vpk` |
| Duo 双宠 | `tools/build_duo_interactive.py` | `publication-duo.json` | `dist/l4d2_neuropet_duo_interactive.vpk` |

**Duo 依赖两款单宠的构建输出**：它读取两款正常单宠 VPK 及其 JSON 构建清单作为输入，因此要先构建两款单宠，再构建 Duo。素材和原画不需要为 Duo 另外复制一份。

### 环境

Python 3.10+、Pillow（见 `requirements.txt`），以及本机拥有并安装的 Left 4 Dead 2。当前整理测试使用 Windows、Python 3.12 和 Pillow 12.3。

以下命令都在仓库根目录运行。建议使用虚拟环境：

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 第一步：构建单宠

```powershell
.\.venv\Scripts\python.exe -B tools/build_client.py --character neuron --game-root "C:\Games\Left 4 Dead 2"
.\.venv\Scripts\python.exe -B tools/build_client.py --character evil --game-root "C:\Games\Left 4 Dead 2"
```

只需要其中一款时，运行对应的一行即可；准备构建 Duo 时，两行都要运行。

`C:\Games\Left 4 Dead 2` 只是示例，换成自己的游戏安装根目录。构建器按原版挂载优先级查找 `update`、三个 DLC 和 `left4dead2` 的原版 `scripts/hudlayout.res`，支持读取 VPK 分卷和 CRC，不读取 addons 中可能被修改的模板。

也可用 `--hud-template "本地提取的hudlayout.res"` 提供自己提取的原版文件。构建记录保存模板来源的相对描述和 SHA-256，不写入使用者的完整本机路径。仓库不提供 Valve 原版模板副本。

### 第二步：构建 Duo

```powershell
.\.venv\Scripts\python.exe -B tools/build_duo_interactive.py
.\.venv\Scripts\python.exe -B tools/check_duo_interactive.py
```

默认从 `dist/` 读取第一步生成的两款单宠 VPK 及构建清单。

- `--base-dist <目录>`：两款单宠 VPK 和 JSON 构建清单放在其他目录时，用它指定。构建与检查两条命令都接受此参数。
- `--output-dir <目录>`：指定 Duo 的输出目录。
- 作为 Duo 输入的单宠包应使用正常发布参数构建，不要使用下文的诊断选项。
- Duo 构建器另有诊断场景和时钟选项，只用于开发测试，不能混入发布包。

`check_duo_interactive.py` 是 Duo 的行为验证入口，检查两份材质的协调状态、互动场景、漏帧和不同绘制频率等。说明见 [双宠互动版](duo-interactions.md)。

### 输出

| 输出 | 内容 |
| --- | --- |
| `dist/l4d2_neuropet_client.vpk` | Neuro-sama 单宠客户端包 |
| `dist/l4d2_neuropet_evil_client.vpk` | Evil Neuro 单宠客户端包，带透明边缘处理 |
| `dist/client-build-manifest.json`、`dist/evil-client-build-manifest.json` | 单宠包身份、素材指纹、姿势、参数及模板来源 |
| `client-only/`、`client-only-evil/` | 单宠对应的 addon 中间目录 |
| `dist/branding/<角色>/preview.jpg` | 单宠工坊封面，1024×1024 JPEG，低于 1 MB |
| `dist/l4d2_neuropet_duo_interactive.vpk` | Duo 双宠客户端包 |
| `dist/interactive-build-manifest.json` | Duo 构建清单 |
| `dist/SHA256SUMS.txt` | 本次 Duo VPK 的 SHA-256 校验值 |
| `dist/interactive-behavior-checks.json` | Duo 行为模拟检查记录，检查工具的默认输出 |
| `dist/preview.jpg`、`dist/cover.png` | Duo 工坊 JPEG 和原始封面；256×256 图标位于 VPK 内 |

当前单宠 VPK 每包有 **10 个文件**，包括 `CODE-LICENSE.txt`、`COVER-CREDITS.txt` 和附加内容列表使用的 `addonimage.jpg`。原 PNG 封面保存在 `assets/promotion/`（Duo 封面在 `assets/promotion/duo/`），构建时只做尺寸／格式导出。

不同游戏更新可能改变 HUD 模板。请记录实际构建清单及包 SHA-256，不承诺不同游戏版本或不同平台字节级相同的输出。

### 检查

单宠：

```powershell
.\.venv\Scripts\python.exe tools/check_release.py --manifest dist/client-build-manifest.json
.\.venv\Scripts\python.exe tools/check_release.py --manifest dist/evil-client-build-manifest.json
.\.venv\Scripts\python.exe tools/check_client_behavior.py --manifest dist/client-build-manifest.json
.\.venv\Scripts\python.exe tools/check_client_behavior.py --manifest dist/evil-client-build-manifest.json
```

第一组读回实际 VPK，校验 CRC、包内容、许可、纹理头、帧数、透明边框和代理数量。第二组对实际材质进行 float32 语义模拟，检查状态保持、地面连续性、姿势边界、墙／顶部跌落、绊倒／抱抱恢复和爬行限速。

Duo：运行上文的 `python -B tools/check_duo_interactive.py`。

模拟不能代替游戏内渲染验证。

### 选项与开发工具

- `--aspect 1.6` 可为 16:10 重建单宠角色比例；这不是已经完成全部宽高比游戏测试的声明。Duo 尚未检查其他比例。
- 发布时默认 `--speed 1`；`--speed 4`、`--preview-trip`、`--preview-creep` 是开发诊断选项，不能混入正常发布包，也不能作为 Duo 的输入。
- `--fixed` 只读取未随公开仓库提供的历史归档，不是当前发布流程。
- `tools/client_lab.py` 是可选的本机 netconsole 开发驱动，会主动加载测试地图并在结束时退出游戏；运行前先了解其命令。它不会被打包到 addon，也不是玩家运行宠物的依赖。

### 发布配置

正式名称、署名、游戏内双语简介和封面由根目录的两份配置管理：

- `publication.json`：两款单宠。
- `publication-duo.json`：Duo。

`maintainer` 为 `Daisy, Shannon & Sol`；`addon_description` 包含 `en` 与 `zh-CN` 两段，构建时以实际换行写入 UTF-8 的 `addonDescription`。附加内容列表的创作者栏只显示项目署名，原画及配置作者的完整署名保留在 NOTICE、素材许可、包内说明和工坊文案中。确定公开的 GitHub 地址后，在配置和实际页面文案中同步填写。

### 整理发布文件

> **注意：** `tools/package_publication.py` 目前**只处理两款单宠**，运行它不会生成 Duo 的发布目录。三款统一的打包流程尚在整理中。

单宠：完成检查后运行

```powershell
.\.venv\Scripts\python.exe tools/package_publication.py --output "发布文件夹"
```

它在一个新的空目录中生成 `github/` 干净源码、按角色分类的 `workshop/` 和一份首次发布说明。每个角色目录只有 VPK、工坊 JPEG、`TITLE.txt` 与精简双语上传稿。原长稿保留在 `docs/workshop/`，不作为默认上传稿。需要旧式源码与安装 ZIP 时可显式指定 `--layout archives`。

Duo：目前需要手动从 Duo 构建输出中整理工坊上传文件，即 VPK、1024×1024 工坊 JPEG、`TITLE.txt` 与精简双语上传稿。上传前请自行检查标题和说明的 UTF-8 字节数。

[Steam 接口](https://partner.steamgames.com/doc/api/ISteamRemoteStorage#Constants) 的标题缓冲区为 128+1 字节，说明上限为 8,000 字节。中文会占多个字节，因此不能只看字符数量。打包工具只整理本地文件，不连接 GitHub 或 Steam，也不提交工坊内容。


### Duo 检查与输出路径的补充

`--output-dir` 是构建器的选项；行为检查器使用 `--output` 指定检查 JSON，默认仍写入 `dist/interactive-behavior-checks.json`。两者的 `--base-dist` 都指向单宠构建输入，不是让检查器读取 Duo VPK。

例如，把 Duo 单独归档到一个子目录：

```powershell
.\.venv\Scripts\python.exe -B tools/build_duo_interactive.py --base-dist dist --output-dir dist/duo
.\.venv\Scripts\python.exe -B tools/check_duo_interactive.py --base-dist dist --output dist/duo/interactive-behavior-checks.json
```

`check_duo_interactive.py` 会从姿势资料重新编译行为图进行 float32 模拟，覆盖协调状态、十二种互动场景、漏帧、不同绘制频率、接收方隐藏停更、方向与速度、时钟回退等；它不直接读取 Duo VPK。构建器写包后会回读并比对全部 17 个条目。当前 `check_release.py` 仅适用于 10 文件的单宠包，不能用于 Duo 清单。

两款单宠输入应采用相同宽高比（默认 16:9）。Duo 从输入清单读取比例，没有独立的 `--aspect` 参数；其他比例尚无实机验证。将三个成品分别归档时，也分别保留对应清单与校验值；这里的 Duo `SHA256SUMS.txt` 只列本次 Duo 包。

### 不提交到仓库的内容

生成的 VPK、VTF 和图集，中间目录，完整实机原始录像，个人实验目录，游戏资源副本和私人配置。成品 VPK 作为 Release 附件发布，三个工坊条目各上传自己的包。

---

## English

This repository maintains three build targets on the same main branch: the Neuro-sama single pet, the Evil Neuro single pet and the Duo. They share character assets, texture processing, build and validation tools and license files; each package is built and published separately.

**Players don't need this page.** Installing a ready-made VPK needs no Python or build tools; see "Install" in the main README.

### Three different things

| | What it is | Where |
| --- | --- | --- |
| **Source code** | Builders, the Duo behavior compiler, validation tools, original assets and licenses, docs and a few validation records | This repository |
| **Built VPKs** | The client packages players install, one per edition | `dist/` (generated locally, not committed); release builds are attached to GitHub Releases and uploaded to three separate Workshop items |
| **Research prototype** | An early server-side VScript experiment exploring a state machine, physics and game events | `research/`; not part of any client package, not used by the builders, not shipped in any release |

Don't put the source folder into the game as an addon; players only need the one VPK they chose.

### Three build targets

| Package | Build entry | Publication config | Default output |
| --- | --- | --- | --- |
| Neuro-sama | `tools/build_client.py --character neuron` | `publication.json` | `dist/l4d2_neuropet_client.vpk` |
| Evil Neuro | `tools/build_client.py --character evil` | `publication.json` | `dist/l4d2_neuropet_evil_client.vpk` |
| Duo | `tools/build_duo_interactive.py` | `publication-duo.json` | `dist/l4d2_neuropet_duo_interactive.vpk` |

**Duo depends on the single-pet build outputs.** It takes the two normal single-pet VPKs and their JSON build manifests as input, so build both single pets first, then Duo. The artwork doesn't need to be copied again for Duo.

### Requirements

Python 3.10+, Pillow (see `requirements.txt`), and a Left 4 Dead 2 install that you own. Current builds were checked on Windows with Python 3.12 and Pillow 12.3.

Run all commands from the repository root. A virtual environment is recommended:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### Step 1: single-pet packages

```powershell
.\.venv\Scripts\python.exe -B tools/build_client.py --character neuron --game-root "C:\Games\Left 4 Dead 2"
.\.venv\Scripts\python.exe -B tools/build_client.py --character evil --game-root "C:\Games\Left 4 Dead 2"
```

Run just one line if you only need one package; run both if you're going to build Duo.

`C:\Games\Left 4 Dead 2` is only an example; use your own game root. The builder looks for the stock `scripts/hudlayout.res` in `update`, the three DLCs and `left4dead2`, following the game's mount priority. It can read split VPKs and CRCs, and it doesn't read templates from `addons`, which may have been modified.

You can also pass `--hud-template "path/to/extracted/hudlayout.res"` with a stock file you extracted yourself. The build record stores a relative description of the template source and its SHA-256, not your full local path. The repository doesn't ship a copy of Valve's template.

### Step 2: Duo

```powershell
.\.venv\Scripts\python.exe -B tools/build_duo_interactive.py
.\.venv\Scripts\python.exe -B tools/check_duo_interactive.py
```

By default it reads the two single-pet VPKs and build manifests from `dist/`.

- `--base-dist <dir>`: use single-pet VPKs and JSON manifests from another folder. Both the build and the check command accept it.
- `--output-dir <dir>`: write Duo's output somewhere else.
- The single-pet packages used as input should be built with normal release options, not the diagnostic options below.
- The Duo builder also has diagnostic scene and clock options. They're for development testing only and must not end up in a release package.

`check_duo_interactive.py` is Duo's behavior check: coordination between the two materials, interaction scenes, missed frames, different draw rates and more. See [Interactive Duo](duo-interactions.md).

### Outputs

| Output | Contents |
| --- | --- |
| `dist/l4d2_neuropet_client.vpk` | Neuro-sama client package |
| `dist/l4d2_neuropet_evil_client.vpk` | Evil Neuro client package, with transparent-edge correction |
| `dist/client-build-manifest.json`, `dist/evil-client-build-manifest.json` | Single-pet package identity, asset fingerprints, poses, parameters and template source |
| `client-only/`, `client-only-evil/` | Single-pet intermediate addon folders |
| `dist/branding/<character>/preview.jpg` | Single-pet Workshop cover, 1024×1024 JPEG under 1 MB |
| `dist/l4d2_neuropet_duo_interactive.vpk` | Duo client package |
| `dist/interactive-build-manifest.json` | Duo build manifest |
| `dist/SHA256SUMS.txt` | SHA-256 checksum for this Duo VPK |
| `dist/interactive-behavior-checks.json` | Default output of the Duo behavior simulation checker |
| `dist/preview.jpg`, `dist/cover.png` | Duo Workshop JPEG and original cover; the 256×256 icon is inside the VPK |

Each single-pet VPK currently contains **10 files**, including `CODE-LICENSE.txt`, `COVER-CREDITS.txt` and the `addonimage.jpg` used in the addon list. Original PNG covers live in `assets/promotion/` (Duo's in `assets/promotion/duo/`); the build only resizes and converts them.

Game updates may change the HUD template. Keep the actual build manifests and package SHA-256 values; byte-identical output across game versions or platforms is not promised.

### Checks

Single pets:

```powershell
.\.venv\Scripts\python.exe tools/check_release.py --manifest dist/client-build-manifest.json
.\.venv\Scripts\python.exe tools/check_release.py --manifest dist/evil-client-build-manifest.json
.\.venv\Scripts\python.exe tools/check_client_behavior.py --manifest dist/client-build-manifest.json
.\.venv\Scripts\python.exe tools/check_client_behavior.py --manifest dist/evil-client-build-manifest.json
```

The first pair reads back the actual VPKs and checks CRCs, contents, licenses, texture headers, frame counts, transparent padding and proxy counts. The second pair simulates the real materials with float32 semantics and checks state persistence, ground continuity, pose bounds, wall/top falls, trip/hug recovery and crawl speed limits.

Duo: run `python -B tools/check_duo_interactive.py` as above.

Simulation doesn't replace in-game rendering tests.

### Options and development tools

- `--aspect 1.6` rebuilds the single-pet character proportions for 16:10. This is not a claim that every aspect ratio has been tested in game. Duo hasn't been checked at other ratios.
- Releases use `--speed 1` by default. `--speed 4`, `--preview-trip` and `--preview-creep` are development diagnostics; they must not go into a release package or be used as Duo input.
- `--fixed` only reads a historical archive that isn't included in the public repository; it isn't part of the current release flow.
- `tools/client_lab.py` is an optional local netconsole driver for development. It loads a test map and quits the game when done, so read its commands before running it. It isn't packaged into any addon and players don't need it.

### Publication configs

Titles, credits, the bilingual in-game descriptions and covers are managed by two files in the repository root:

- `publication.json`: the two single pets.
- `publication-duo.json`: Duo.

`maintainer` is `Daisy, Shannon & Sol`. `addon_description` has `en` and `zh-CN` parts, written into the UTF-8 `addonDescription` with real line breaks. The addon list's author field only shows the project credit; full credits for the artwork and config authors remain in NOTICE, the asset licenses, the in-package notes and the Workshop text. Once the public GitHub address is final, fill it in both the configs and the published pages.

### Preparing release files

> **Note:** `tools/package_publication.py` currently **handles only the two single pets**. Running it does not produce a Duo release folder. A unified three-package flow is still being worked on.

Single pets: after the checks, run

```powershell
.\.venv\Scripts\python.exe tools/package_publication.py --output "release-folder"
```

In a new empty folder it creates a clean `github/` source tree, a per-character `workshop/` folder and first-release notes. Each character folder holds only the VPK, the Workshop JPEG, `TITLE.txt` and the short bilingual upload text. The longer drafts stay in `docs/workshop/` and aren't used by default. Pass `--layout archives` for the older source and install ZIPs.

Duo: for now, collect the Workshop upload files from the Duo build output by hand: the VPK, the 1024×1024 Workshop JPEG, `TITLE.txt` and the short bilingual upload text. Check the UTF-8 byte length of the title and description yourself before uploading.

The [Steam API](https://partner.steamgames.com/doc/api/ISteamRemoteStorage#Constants) allows a 128+1-byte title buffer and an 8,000-byte description. Chinese characters take several bytes each, so counting characters isn't enough. The packaging tool only arranges local files; it doesn't connect to GitHub or Steam or submit anything to the Workshop.

### Not committed

Generated VPKs, VTFs and atlases, intermediate folders, full raw gameplay recordings, personal experiment folders, copies of game files and private configs. Built VPKs are published as Release attachments, and each of the three Workshop items gets its own package.


### Duo checks and output paths

The builder accepts `--output-dir`; the checker uses `--output` for its JSON report, defaulting to `dist/interactive-behavior-checks.json`. Both tools' `--base-dist` refers to single-pet build inputs. The checker recompiles the graph from pose data for float32 simulation; it does not read the Duo VPK. The builder reads back and compares all 17 package entries. `check_release.py` currently supports only the ten-file single-pet packages.

Use matching input aspect ratios (16:9 by default). Duo reads each input manifest's aspect and has no separate `--aspect` option. Other ratios have not been checked in game. Keep separate manifests and checksums when archiving all three editions; the Duo `SHA256SUMS.txt` lists only that Duo VPK.
