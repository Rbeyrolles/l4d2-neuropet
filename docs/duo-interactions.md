# 双宠互动版 / Interactive Duo

这是与两款单宠在同一仓库、同一主分支维护的客户端双宠构建目标。当前发布版为 `0.2.3`，沿用已测试的 `0.2.2-preview` 行为。Neuro-sama 与 Evil Neuro 分别活动，能在底边相遇时偶尔抱抱，也能偶尔主动走向另一只。两款单宠的构建入口和已发布 VPK 保持原样。

## 0.2.3 封面与简介

本次使用用户选定的牵手封面，插件列表简介采用英文、中文两段，署名为 Daisy, Shannon & Sol。发布配置保存在 `publication-duo.json`，封面原图、制作提示词和来源说明位于 `assets/promotion/duo/`。构建时导出 256×256 插件图标、1024×1024 工坊 JPEG 和原始 PNG。

本次不改动行为。对照已测试的 0.2.2-preview 包，只有插件元数据、列表图标及两份封面来源说明发生变化；HUD、两份行为材质、两套图集以及原画与代码许可保持逐字节相同。打包检查记录见 [0.2.3 包校验](evidence/duo-0.2.3/package-validation.json)。牵手是封面构图，游戏内互动仍是抱抱。

## 0.2.2 发起者与靠近动作

旧版始终由位于右侧的角色发起。使用已交付的 0.2.1 材质模拟四小时，Evil 发起 49 次、Neuro 47 次，长期数量接近；但开局前十分钟三次全是 Evil。初始位置和观察时长都会影响体感，旧版没有专门偏好 Evil 的角色规则。

新版把成功机会的伪随机区间 `[0, 0.6]` 分成等长的两半，分别选择 Neuro 与 Evil，不再由左右位置决定。相同四小时模拟得到 Neuro 59 次、Evil 54 次；这是确定性样本记录，不承诺每局次数相等，也不强制轮流。

靠近不再固定八秒。扣除 24 个 VGUI 单位的抱抱间距后，路程不超过 144 单位时用走路姿势，以 30 单位/秒、8 FPS 接近；更远时用小跑姿势，以 60 单位/秒、12 FPS 接近。相距约 25 单位以内仍可以直接抱抱。例如相距 80 单位时走约 1.87 秒，相距 380 单位时小跑约 5.93 秒。

抱抱朝向由本次两只的相对位置固定下来。从左边走近时使用各自原抱抱的像素镜像副本，不穿过等待者再绕到右边。每套图集保留原 202 帧与第 202 号透明帧，追加 28 帧镜像抱抱（203–230）；原画与 Evil 的边缘修复未重新绘制。

靠近时长可以是小数。双方仍在共同的整数秒时钟上发起互动，并保存相同的精确开始、结束时间与位置；后续阶段从共同结束点计算。这个变化继续通过不同绘制频率、漏帧和抱完恢复检查。

## 0.2.1 同步修复

0.2.0 的两份材质各自累积位置，并以实际绘制时刻确定下一阶段的结束时间。模拟中只让 Neuro 在第 3 秒的切换点少更新一帧，下一阶段的结束时间便相差约 16.7 毫秒；后续随机取样和位置越来越不同，到约第 199 秒复现了 Evil 正在抱抱、Neuro 却独自在爬墙的情况。此前同一时刻绑定两份材质的检查没有覆盖这个问题。

0.2.1 把行为决定固定在共同的整数秒时钟上，下一阶段从既定边界开始，位置由阶段起点、速度和当前时间直接计算。画面位置与动画仍使用连续时间，决策时钟不会把移动降成每秒一帧。抱抱期间两只使用共同的开始、结束和停靠位置；恢复活动时从共同的停靠位置重新建立阶段，不依赖各自最后一次绘制的坐标。

代理优化也保留标量到向量的最后复制，防止把向量分量重新用于不支持分量输入的数学代理。

## 行为

- 两只都能沿底边走路、小跑、慢爬，爬左右侧、沿顶部移动、休息和跌落。路线与停留点分别决定，不固定各占半边屏幕。
- 相遇抱抱会检查共同决策时刻的模拟位置：都在底边、处于普通移动或休息阶段、距离约 25 个 VGUI 单位以内，而且互动冷却已结束时，进行概率判断。经过对方也可能继续各自活动。
- 两只都在底边且相距更远时，可以主动寻找。对方停下来等待，寻找者根据距离走路或小跑靠近，再播放约 4 秒抱抱。
- 两只都可以发起，分别使用原素材中属于自己的 `HugAction`。发起者独立于左右位置选择；从左侧靠近时使用该角色自己的镜像抱抱。
- 原抱抱图已经包含两位角色。抱抱期间接收方使用透明帧，结束后恢复独立显示与活动，避免看起来多出第三位。
- 抱完至少休息 45 秒才可再次互动。通过冷却和位置条件后，概率阈值是 60%；一次未触发的机会后等待约 24 秒再尝试，不表示每隔固定时间必定抱抱。
- 原抱抱和绊倒的 28 帧仍按 8 FPS 播放，最后一帧多停约半秒，统一在四秒阶段末尾恢复活动。

普通活动与互动使用共享的确定性伪随机计算。本版已针对短暂漏帧和不同绘制频率检查状态一致性。这个系统没有完整移植 web-mascot 的行为引擎，也没有使用服务端 VScript。

## 实现与范围

两个 VGUI `ImagePanel` 分别使用自己的 `UnlitGeneric` 材质、图集与命名空间。每份材质都计算两只的位置和互动状态；它们输出不同角色的画面。素材原来的 202 帧保持逐字节相同，包括 Evil 的透明边缘修复；图集末尾追加一张全透明帧和 28 张原抱抱的镜像副本。

每份材质使用 254 个代理、106 个自定义参数。本机 L4D2 对正好 256 个代理也报 `has more than 256 proxies` 并放弃加载，因此构建入口限制为最多 255。材质输出向量属于可观察的结果，编译优化只回收编号临时变量，不再误删位置向量分量。普通动作选择合并了地面与其他边缘的低概率分支，以容纳新逻辑；各类动作的概率权重保持原值。

代理处理标量与材质变量的机制可以参照 [Valve 的 functionproxy.cpp](https://github.com/ValveSoftware/source-sdk-2013/blob/master/src/game/client/functionproxy.cpp) 和 [mathproxy.cpp](https://github.com/ValveSoftware/source-sdk-2013/blob/master/src/game/client/mathproxy.cpp)。本版数量边界来自 L4D2 实机日志；其他 Source 游戏的限制不能直接套用。

互动目前只发生在底边。没有墙面或顶部抱抱、碰撞避让、鼠标拖拽和游戏事件反应。未触发互动时仍允许两只重叠。双宠的材质计算与绘制开销高于单宠，尚未做 FPS 差异测量。

这是普通客户端 addon，不需要 SourceMod、服务器安装或外部运行程序。服务器仍需允许客户端 HUD addons。包内覆盖 `scripts/hudlayout.res`，仍可能与第三方 HUD mod 冲突；启用本版时应停用单宠、旧双宠及 VScript 研究版。

## 验证记录（2026-10-12）

| 验证 | 结果与边界 |
| --- | --- |
| 每份材质 18,000 次模拟绑定（10 分钟） | 两份协调状态一致，显示坐标和帧处于允许范围；地图时钟回退后仍一致 |
| 十二种指定初始位置 | Neuro / Evil 分别从左右两边进行远距离寻找、短距离靠近、相遇抱抱，完整 28 帧；接收方隐藏后恢复 |
| 少更新一帧、连续漏几帧、移动中漏帧 | 每种检查五分钟，不再出现抱抱时接收方独立显示的问题 |
| 一只按 15 FPS、另一只按 60 FPS 更新 | 五分钟内协调状态一致 |
| 接收方在隐藏后暂停更新 | 四秒后重新绑定，仍从同一互动阶段恢复 |
| 底边速度 | 走路约 30、小跑约 60、慢爬约 8 VGUI 单位/秒 |
| 十八组距离与方向 | 实际位移速度与走路／小跑姿势匹配，包含 144 单位路程阈值两侧 |
| 角色选择与四小时样本 | 成功概率区间的两半分别对应两个发起者；样本 59 次 Neuro、54 次 Evil |
| Windows、1280×720、本地 coop 实机 | 五个指定互动场景与一分钟普通随机活动；连续录像约 120.76 秒，无宠物材质加载错误 |
| 人工观察 | 测试者确认“走路、抱抱和恢复正常，没有看到闪烁或错位” |
| 测试恢复与安装 | 插件列表及四个游戏配置文件逐字节恢复，临时包和材质移除；普通随机版随后更新到本机，旧版已备份 |

指定初始位置用于检查动作，不代表正式版的互动频率。录像与原始日志保存在本地实验目录，未作为源码依赖加入仓库。交付包使用普通初始状态，无演示场景或测试时钟偏移。VPK 已回读校验各条目；本轮启动时加载生产材质，后续场景仅修改初始状态、角色选择取样或测试时钟偏移。详见 [0.2.2 验证记录](evidence/duo-0.2.2-preview/validation.json)；上一轮同步修复记录保存在 [0.2.1 验证记录](evidence/duo-0.2.1-preview/validation.json)。

已验证的环境仍限于上述本机配置，没有据此承诺所有服务器、分辨率或 HUD 组合都可使用。材质没有完整的历史事件重放机制：单独长时间停止绘制、漏过整个互动发起窗口或仅重载其中一份材质，仍可能破坏同步，需要重启游戏重新加载两份材质。本轮覆盖的是短暂漏帧、不同绘制频率和互动已开始后的隐藏停更。

## 从源码构建

先按主 README 的步骤安装 Python 依赖，并从自己的游戏安装提取 HUD 模板，构建两款普通单宠：

```powershell
python -B tools/build_client.py --character neuron --game-root "你的 Left 4 Dead 2 安装目录"
python -B tools/build_client.py --character evil --game-root "你的 Left 4 Dead 2 安装目录"
python -B tools/build_duo_interactive.py
python -B tools/check_duo_interactive.py
```

输出为 `dist/l4d2_neuropet_duo_interactive.vpk`、构建清单、校验值与行为检查记录。已有两款单宠 VPK 和 JSON 构建清单时，也可以使用 `--base-dist` 指向它们所在的目录；用 `--output-dir` 设置新的输出目录。诊断场景和时钟选项仅用于开发测试。

主要源码：`tools/duo_pair_graph.py`（代理编译与优化）、`tools/duo_perimeter_behavior.py`（移动与互动）、`tools/build_duo_interactive.py`（打包）、`tools/check_duo_interactive.py`（验证）。

自写代码继续使用 MIT。两套原画及衍生图集继续使用 CC BY-NC-SA 4.0；两位角色的许可、Paccha 与原项目贡献者的署名均保留在包内。项目署名 Daisy, Shannon & Sol。非官方粉丝作品。

## English

The `0.2.3` package adds the selected hand-in-hand cover and bilingual addon text, retaining the tested `0.2.2-preview` behavior. HUD, materials, atlases and original licenses are byte-identical to that build; only metadata, the addon icon and two cover-credit files change. Hand-holding is promotional artwork, not an added in-game behavior.

The client duo chooses the initiator independently of screen position, using equal halves of the successful shared lottery interval. Either character can approach from either side; original hug frames are mirrored for left-side approaches. A four-hour deterministic simulation produced 59 Neuro-initiated and 54 Evil-initiated interactions; individual sessions need not have equal counts.

Approach duration follows travel distance. After allowing a 24-unit meeting gap, travel up to 144 VGUI units uses walking at 30 units/second and 8 FPS; longer travel uses trotting at 60 units/second and 12 FPS. Nearby encounters can hug immediately. Hugs last about four seconds, including a half-second final hold. The clip already depicts both characters, so the receiver becomes transparent during it and returns afterward. At least 45 seconds must pass before another interaction is eligible.

Each pet has a separate material and texture. Both compute the same coordination state and render their respective character, using 254 proxies and 106 custom parameters. All original 202 atlas frames remain byte-identical, followed by a blank frame and 28 pixel-mirrored hug frames. Shared decision timing and analytic motion retain the 0.2.1 synchronization fix; fractional approach end times are shared exactly.

Regression checks cover twelve interaction scenes, eighteen distance/direction cases, missed bindings, 15 FPS versus 60 FPS, a receiver paused after becoming hidden, floor speeds and clock rollback. Native local co-op testing at 1280×720 covered five directed interactions and a minute of ordinary movement, recorded over 120.76 seconds. The tester confirmed normal walking, hugs and recovery without visible flicker or mismatch. Settings were restored, temporary files removed, and the normal build installed with the previous version backed up. These checks do not establish compatibility with every server or display configuration, or arbitrary long interruptions of one material.

Interactions take place on the floor, with approaches from either direction. There is no wall/ceiling hugging, collision avoidance, mouse interaction or game-event feedback. Disable single-pet editions and other duo editions when using this package. Conflicting third-party HUD mods remain unsupported; servers must allow client HUD addons. No SourceMod, server installation or external runtime is required.

Build both normal single-pet editions first, then run `python -B tools/build_duo_interactive.py` and `python -B tools/check_duo_interactive.py`. Both accept `--base-dist` for an existing pair of VPKs and manifests. The original single-pet release packages remain unchanged. Code is MIT; artwork and derived textures retain CC BY-NC-SA 4.0 and all original credits.
