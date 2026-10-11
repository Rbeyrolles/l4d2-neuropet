# 构建和验证

源码仓库包含当前客户端版的构建器、两套原素材和素材许可。无需把开发者的 `references/`、Steam 游戏文件或 SDK 工具复制进仓库。

## 环境

Python 3.10+，Pillow，以及本机拥有并安装的 Left 4 Dead 2。当前整理测试使用 Windows、Python 3.12 和 Pillow 12.3。玩家安装现成 VPK 不需要这些构建依赖。

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe tools/build_client.py --character neuron --game-root "C:\Games\Left 4 Dead 2"
.\.venv\Scripts\python.exe tools/build_client.py --character evil --game-root "C:\Games\Left 4 Dead 2"
```

`C:\Games\Left 4 Dead 2` 只是示例，换成自己的游戏安装根目录。构建器按原版挂载优先级查找 `update`、三个 DLC 和 `left4dead2` 的原版 `scripts/hudlayout.res`，支持读取 VPK 分卷和 CRC，不读取 addons 中可能被修改的模板。

也可用 `--hud-template "本地提取的hudlayout.res"` 提供自己提取的原版文件。构建记录保存模板来源的相对描述和 SHA-256，不写入使用者的完整本机路径。仓库不提供 Valve 原版模板副本。

## 输出

| 输出 | 内容 |
| --- | --- |
| `dist/l4d2_neuropet_client.vpk` | Neuron 客户端版 |
| `dist/l4d2_neuropet_evil_client.vpk` | Evil 客户端版，带透明边缘处理 |
| `dist/*client-build-manifest.json` | 包身份、素材指纹、姿势、参数及模板来源 |
| `client-only/`、`client-only-evil/` | 对应 addon 的中间目录 |

正式名称、署名、游戏内双语简介和封面由根目录 `publication.json` 管理。`maintainer` 当前为 `Daisy, Shannon & Sol`，每个角色的 `addon_description` 包含 `en` 与 `zh-CN` 两段；构建时以实际换行写入 UTF-8 的 `addonDescription`。附加内容列表的创作者栏只显示项目署名，原画及配置作者的完整署名仍保留在 NOTICE、素材许可、包内说明和工坊文案中。确定 GitHub 地址后，在配置和实际页面文案中同步填写。

当前待发布 VPK 每包有 **10 个文件**：包括 `CODE-LICENSE.txt`、`COVER-CREDITS.txt` 和附加内容列表使用的 `addonimage.jpg`。原 PNG 保存在 `assets/promotion/`；构建时只做尺寸／格式导出，工坊用的 `dist/branding/<角色>/preview.jpg` 为 1024×1024 JPEG，低于 1 MB。角色图集、动作材质与 HUD 布局与已验证版本保持相同。

不同游戏更新可能改变 HUD 模板。记录实际构建清单及包 SHA-256，不承诺不同游戏版本或不同平台字节级相同的输出。

## 检查

```powershell
python tools/check_release.py --manifest dist/client-build-manifest.json
python tools/check_release.py --manifest dist/evil-client-build-manifest.json
python tools/check_client_behavior.py --manifest dist/client-build-manifest.json
python tools/check_client_behavior.py --manifest dist/evil-client-build-manifest.json
```

第一组读回实际 VPK，校验 CRC、包内容、许可、纹理头、帧数、透明边框和代理数量。第二组对实际材质进行 float32 语义模拟，检查状态保持、地面连续性、姿势边界、墙／顶部跌落、绊倒／抱抱恢复和爬行限速。模拟不能代替游戏内渲染验证。

`--aspect 1.6` 可为 16:10 重建角色比例；这不是已经完成全部宽高比游戏测试的声明。发布时默认 `--speed 1`；`--speed 4`、`--preview-trip`、`--preview-creep` 是开发诊断选项，不能混入正常发布包。`--fixed` 只读取未随公开仓库提供的历史归档，不是当前发布流程。

`tools/client_lab.py` 是可选的本机 netconsole 开发驱动，主动加载测试地图并在结束时退出游戏；运行前先了解其命令。它不会被打包到 addon，也不是玩家运行宠物的依赖。

完成检查后可运行 `python tools/package_publication.py --output "发布文件夹"`，在一个新的空目录中生成 `github/` 干净源码、按角色分类的 `workshop/` 和一份首次发布说明。每个角色目录只有 VPK、工坊 JPEG、TITLE.txt 与精简双语上传稿。`workshop_publish_description` 指向上传稿，保留动作、兼容提示和完整署名；原长稿继续保留在 `docs/workshop/`，不作为默认上传稿。

工具会检查标题和说明的 UTF-8 字节长度；[Steam 接口](https://partner.steamgames.com/doc/api/ISteamRemoteStorage#Constants) 的标题缓冲区为 128+1 字节，说明上限为 8,000 字节。中文会占多个字节，因此不能只看字符数量。需要旧式源码与安装 ZIP 时可显式指定 `--layout archives`。此工具只整理本地文件，不连接 GitHub 或 Steam，也不提交工坊内容。
