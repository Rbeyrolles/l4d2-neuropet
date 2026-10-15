# L4D2 Neuropet

[English](README.md) | **简体中文**

Left 4 Dead 2 的粉丝自制屏幕小宠物。打僵尸的间隙，屏幕周围会有个小小的 Neuro-sama、小小的 Evil Neuro，或者两只一起：走路、攀爬、休息，偶尔绊一跤，或者停下来抱抱。

Neuropet 是一个项目，提供三款可选安装包：**Neuro-sama**、**Evil Neuro** 和 **Duo**。三款都在本仓库中维护，分别构建。

> **非官方粉丝作品。** 与 Vedal 无关联、未获其认可。只改变 HUD 上显示的画面，不影响游戏玩法。不包含 AI、聊天、语音或联网功能，仅使用角色形象。

| Neuro-sama | Evil Neuro | Duo |
| --- | --- | --- |
| ![Neuro-sama cover](assets/promotion/neuro-sama/cover.png) | ![Evil Neuro cover](assets/promotion/evil-neuro/cover.png) | ![Neuropet Duo cover](assets/promotion/duo/cover.png) |

所有封面均为 AI 辅助宣传插画，非实机截图。单宠封面基于原抱抱素材；Duo 封面基于角色素材及参考图。Duo 封面上的牵手只是封面构图，游戏里两只是抱抱。制作说明见 [封面署名](assets/promotion/CREDITS.md)。

**实机展示：**[Duo 创意工坊页面](https://steamcommunity.com/sharedfiles/filedetails/?id=3820220607)。演示为集中展示安排了位置和动作，速度保持原样；正式版随机选择。

## 选一款

| | Neuro-sama 单宠版 | Evil Neuro 单宠版 | Duo 双宠版 |
| --- | --- | --- | --- |
| 屏幕上 | 一只 Neuro-sama | 一只 Evil Neuro | 两只，各自活动 |
| 抱抱 | Evil 在抱抱动画里友情客串 | Neuro 在抱抱动画里友情客串 | 一只走过去或小跑过去找另一只，一起抱抱，再各自出发 |

**三款中选择并启用一款。** 想让两只一起出现，请选择 Duo；无需同时启用两款单宠。三款分别编号，Duo 0.2.3 不是从单宠 0.5.x 降级。

## 下载

> **HUD 兼容提示：** 不保证与第三方自定义 HUD Mod 兼容。修改同一份 HUD 布局时，可能导致宠物不显示或界面布局被覆盖。建议使用原版 HUD；遇到问题先停用其他 HUD Mod 并重启游戏。详见 [HUD 冲突与排障](docs/HUD_COMPATIBILITY.md)。

| 版本 | 版本号 | VPK 文件 | 下载 | 创意工坊 | 游戏内附加内容名称 |
| --- | --- | --- | --- | --- | --- |
| Neuro-sama 单宠版 | 0.5.2 | `l4d2_neuropet_client.vpk` | https://github.com/Rbeyrolles/l4d2-neuropet/releases/download/client-2026-10-11/l4d2_neuropet_client.vpk | https://steamcommunity.com/sharedfiles/filedetails/?id=3820218016 | Neuropet – Neuro-sama Screen Pet (Fan-made HUD Mascot) |
| Evil Neuro 单宠版 | 0.5.3 | `l4d2_neuropet_evil_client.vpk` | https://github.com/Rbeyrolles/l4d2-neuropet/releases/download/client-2026-10-11/l4d2_neuropet_evil_client.vpk | https://steamcommunity.com/sharedfiles/filedetails/?id=3820220066 | Neuropet – Evil Neuro Screen Pet (Fan-made HUD Mascot) |
| Duo 双宠版 | 0.2.3 | `l4d2_neuropet_duo_interactive.vpk` | [Workshop](https://steamcommunity.com/sharedfiles/filedetails/?id=3820220607) | https://steamcommunity.com/sharedfiles/filedetails/?id=3820220607 | Neuropet – Neuro-sama & Evil Neuro Screen Pets (Fan-made HUD Mascots) |

两款单宠的现成 VPK 与 SHA-256 校验文件见 [GitHub Releases](https://github.com/Rbeyrolles/l4d2-neuropet/releases)。Duo 可从创意工坊订阅，或按下方步骤从源码构建。三款都由本仓库构建；想自己构建，见[从源码构建](#从源码构建)。玩家不需要 Python 或任何构建工具。

## 她们会做什么

### 三款共有

- **到处走走：** 沿底边走路、小跑或慢慢趴着爬；攀爬左右边缘；沿顶部移动和悬挂；偶尔松手跌落；绊一跤再爬起来。
- **八种休息姿势：**

  | Neuro-sama | Evil Neuro |
  | --- | --- |
  | 站立眨眼 | 站立眨眼 |
  | 坐下眨眼 | 坐下眨眼 |
  | 趴下偷懒 | 趴下偷懒 |
  | 坐着抬头 | 坐着抬头 |
  | Wink | 等抱抱 |
  | 比心 | 趴着害羞 |
  | 站着害羞 | 站着害羞 |
  | 坐着害羞 | 坐着害羞 |

- **不是固定循环：** 路线、速度、休息时间、停留点和休息姿势都随机选择，每只都从上次停下的地方继续。

### 单宠版（Neuro-sama、Evil Neuro）

- **小插曲：** 绊倒再爬起来，以及一小段抱抱动画，她的双胞胎姐妹会友情客串。在单宠版里，另一个角色只是抱抱动画的一部分，不是第二只宠物。想要两只，请看下面的 Duo。
- **按段抽取：** 每一段随机抽取路线、速度、休息时间、目标位置、休息姿势和小插曲，并在这一段内保持不变。墙上、顶部的停留和跌落位置也会变化。

#### 随机权重（仅单宠版）

以下是每段的抽签权重，不是每分钟的概率。有些动作可能要等几分钟才出现。这些数字不适用于 Duo。

| 抽签 | 选项 |
| --- | --- |
| 地面移动 | 走路 60% · 小跑 20% · 慢爬 20% |
| 小插曲 | 绊倒 20% · 抱抱 20% · 无 60% |

- **绊倒** 只在走路或小跑时出现，慢爬、攀爬和休息时不会。基准时长约 3.5 秒：失衡 → 倒地约 1.5 秒 → 撑起 → 坐起 → 站稳。受本段速度系数影响，实际约 3–4.1 秒。
- **抱抱** 可在地面移动或休息时出现，每个适用的段落最多一次。基准约 3.5 秒，期间暂停移动，之后继续。
- **慢爬** 的时长随距离延长，避免小小的爬姿在屏幕上滑得太快。两张爬姿以 3 fps 交替。

### Duo 双宠版

- **两只，各走各的。** Neuro-sama 和 Evil Neuro 各自决定路线和停留点，可以在屏幕四周的不同位置活动，并不是一人占一半。
- **偶然相遇：** 两只都在底边、离得很近时，可能会停下来抱抱。
- **去找她：** 离得远时，也可能有一只主动去找另一只：近就走过去，远就小跑过去，从左边或右边靠近都可以。谁都可以先出发，跟谁站在左边无关。
- **抱抱** 使用原本就画着两位角色的原动画，约四秒。播放时两只合成同一段画面，结束后重新分开、各自活动，不会多出第三只。
- **耐心一点：** 抱完至少约 45 秒才可能再次互动，之后还要看位置和运气，所以没有固定的时间表。

实现、测试与限制见 [双宠互动版](docs/duo-interactions.md)。

### 她们都不会做的事

不能拖拽或点击，没有聊天、语音或 AI，没有完整的 Shimeji 行为系统、HUD 避让或实时二维碰撞物理。Duo 的互动只在底边发生：墙上和顶部不会抱抱，没有通用的碰撞避让，也没有牵手或跟随。

她们也**不会读取或响应游戏事件**（倒地、救援、Tank、Witch、尸潮、安全屋）。跌落来自随机的动画片段。如果刚好在 Tank 出现时掉下来，那只是时机太巧啦。

## 安装

**创意工坊：** 订阅**一款** Neuropet 条目后启动游戏。进入关卡后，宠物会出现在 HUD 上；主菜单里看不到是正常的。已订阅的条目由 Steam 自动更新，更新后重启游戏。

**手动安装：**

1. 把**一款** Neuropet VPK 放进游戏目录下的 `left4dead2/addons/`。
2. 在主菜单的**附加内容**中启用。
3. 重启游戏，正常进入关卡。

**升级（手动）：** 用同名新版 VPK 替换旧版，然后重启。
**切换：** 取消订阅或移除当前这一款，再订阅或放入另一款，然后重启。始终只保留一款 Neuropet 启用。
**卸载：** 取消订阅，或从 `addons/` 删除 VPK，然后重启。

同一款不要同时保留手动副本和工坊订阅。

每一款都作为普通的仅客户端附加内容在你自己的电脑上运行。服务器无需安装任何东西，你也不需要 SourceMod、VSLib、Python、外部程序、浏览器或任何控制台命令。Python 只在从源码构建时使用。

## 兼容性与已知限制

- **HUD 插件：** 不保证与第三方自定义 HUD Mod 兼容。三款都会替换 `scripts/hudlayout.res`；其他修改同一文件的插件可能使宠物不显示，或覆盖另一方的界面布局。其他第三方自定义 HUD Mod 也可能包含此文件。Neuropet 不会扫描、合并其他 HUD 或调整加载顺序；即使本机能同时显示，也不能视为兼容保证。请先停用其他 HUD Mod 并重启；见 [排障指南](docs/HUD_COMPATIBILITY.md)。
- **屏幕边缘：** 底边没有为血条预留空间，宠物可能与 HUD 重叠，也可能被部分遮住。在两侧和顶部，身体可能有一部分越出屏幕，像是抓着屏幕边缘。
- **服务器：** 有些服务器不允许使用自定义的客户端附加内容，本项目也无法绕过这类设置。设计上不需要服务器安装任何东西，但尚未在远程服务器上测试。
- **屏幕比例：** 默认按 16:9 制作。单宠版可以用源码参数为其他比例重新构建，但尚未验证；Duo 尚未检查其他比例。
- **目前已测试：** 三款均在 Windows、本地合作模式、1280×720 下测试；Duo 宣传视频另在 1920×1080 下实机录制。分屏、感染者视角、对抗、清道夫、其他比例和远程服务器均未测试。
- **Duo 同步：** 短暂漏帧、不同绘制频率和抱完恢复都已检查。若其中一只长时间停止绘制、错过整个互动发起阶段，或只重新加载了两份材质中的一份，仍可能不同步。两只看起来不同步时，请完整重启游戏。
- **性能：** 尚无正式的性能测试，因此不做任何性能承诺。Duo 的材质计算量比单宠多。
- **认证：** 未经 Valve 审核或认证。
- **大小：** 目前每个单宠 VPK 约 50.6 MiB，因为帧图集以未压缩的 RGBA8888 保存；Duo VPK 约 115.7 MiB。以后的版本可能会变化。

## 实现原理

一切都通过游戏自带的 HUD 和材质系统运行：

- 客户端 **VGUI ImagePanel** 负责绘制宠物。
- **VMT 材质代理** 在游戏内计算时间、随机选择、动画帧和位置。
- **多帧 VTF** 保存帧图集。

| | 单宠版 | Duo |
| --- | --- | --- |
| 面板 | 1 个 | 2 个（每位角色一个） |
| 图集帧数 | 202 | 每位角色 231：原 202 帧、1 张透明帧和 28 张抱抱镜像帧 |
| 材质代理 | 255 | 每份材质 254 |
| 自定义参数 | 154 | 每份材质 106 |

Duo 的两份材质都会计算两只共同的状态，各自绘制自己的角色，因此两边对位置和抱抱时机的判断一致。所有运行包内都不含 Squirrel/VScript、mutation、SourceMod 插件、DLL 或外部程序。

**Python 只在构建时使用。** 构建器读取原动作帧、生成图集、编译材质逻辑、从*你自己的* L4D2 安装中读取原版 HUD 布局模板，然后写出 VPK。

### 从源码构建

需要 Python 3.10+、Pillow，以及本机安装的 Left 4 Dead 2（构建器会从中读取原版 HUD 模板）。

```powershell
python -m pip install -r requirements.txt

# 单宠：按需构建；构建 Duo 前需要先完成这两款。
python -B tools/build_client.py --character neuron --game-root "C:\Games\Left 4 Dead 2"
python -B tools/build_client.py --character evil --game-root "C:\Games\Left 4 Dead 2"

# Duo：复用上面生成的两款单宠包及其构建清单。
python -B tools/build_duo_interactive.py
python -B tools/check_duo_interactive.py
```

把示例路径换成自己的游戏目录。输出位于 `dist/`。完整步骤、检查与选项见 [docs/BUILDING.md](docs/BUILDING.md)。生成的图集、中间目录和 VPK 不提交到仓库；正式构建附在 Releases 中。

### 同一个仓库，三个构建目标

三款都在同一条主分支上维护。这里的「款」或「版本」指可选的安装内容，不是另开的 Git 分支。Duo 复用角色素材、纹理处理、构建与验证工具和许可文件，并有自己的互动逻辑和构建入口。

| 安装包 | 构建入口 | 发布配置 |
| --- | --- | --- |
| Neuro-sama | `tools/build_client.py --character neuron` | `publication.json` |
| Evil Neuro | `tools/build_client.py --character evil` | `publication.json` |
| Duo | `tools/build_duo_interactive.py`（需要先构建两款单宠） | `publication-duo.json` |

### 仓库内容

```text
assets/mascot_pack/     shared Neuron / Eviling artwork and their original licenses
assets/promotion/       covers and how they were made (Duo cover in duo/)
tools/                  builders, Duo behavior compiler, validation and packaging
docs/                   behavior, building, Duo notes, tests and Workshop copy
research/               historical server-side VScript prototype
publication.json        single-pet titles, descriptions, credits and covers
publication-duo.json    the same for Duo
```

- `tools/build_client.py`：构建两款单宠。
- `tools/build_duo_interactive.py`：以两款单宠为输入构建 Duo。
- `tools/duo_pair_graph.py`、`tools/duo_perimeter_behavior.py`：Duo 的材质代理编译，以及移动与互动逻辑。
- `tools/check_duo_interactive.py`：Duo 行为验证。
- 许可文件、文档和少量验证记录。
- `research/`：早期的服务端 VScript 研究原型，探索过状态机、物理和游戏事件。**它不属于三款客户端安装包中的任何一款，也不随任何 Release 发布。**

不包含：生成的 VPK 与 VTF、完整实机原始录像、原始 references 目录、Valve 游戏资源副本、SDK 二进制文件、个人实验目录、私人路径或配置。

### 与 web-mascot 的关系

本项目**不是** [web-mascot](https://github.com/CommentOut64/web-mascot) 的移植版，没有移植它的 TypeScript/DOM/XML 引擎。本项目使用其单独许可的原素材与动作帧作参考，行为和移动轨迹另行实现。也没有接入 Neuro SDK。

### Evil Neuro 0.5.3 白边修复

Evil Neuro 的深色边缘周围曾出现浅色描边。原因是原 PNG 中全透明像素保存了白色 RGB，纹理过滤时可能被混入边缘。修复方法是把附近原画颜色延伸到四个像素步长内的全透明像素，所有透明度和所有可见 RGBA 像素保持不变。Duo 使用同样修复后的帧。

全部 202 帧均已检查，尺寸、锚点、可见细节、材质和 HUD 布局都保持原样。实机测试中白边明显减轻或已看不到。我们不保证在所有分辨率或环境下都完全没有边缘差异。

仓库中的修复前后对比图是数值采样模型的局部放大，不是实机截图。模型中的误差下降数据只描述该模型，不代表玩家画面的改善百分比。

<details>
<summary><b>测试记录</b></summary>

所有测试：Windows、1280×720、本地合作模式。

- **Neuro-sama 0.5.2：** 75 秒测试，另有 120 秒固定慢爬演示。确认爬行节奏舒服。
- **Evil Neuro 0.5.3：** 150 秒测试。确认白边减轻。
- **Duo 0.2.2-preview 行为（0.2.3 原样沿用）：** 五个指定互动场景加一分钟普通随机活动，连续录制约 121 秒。测试者确认走路、抱抱和恢复正常，没有看到闪烁或错位。指定初始位置只用于检查动作，不代表正式版的互动频率。模拟检查覆盖每份材质 18,000 次绑定、漏帧、15 FPS 与 60 FPS 不同绘制频率，以及接收方隐藏后暂停更新。详见 [双宠互动版](docs/duo-interactions.md)。

以上测试中游戏均正常退出，未发现宠物材质错误。

单宠测试准备阶段，我们曾临时使用游戏内调试命令（例如暂停 AI Director、保护测试玩家），观察宠物时关闭，最后短暂打开以查询服务端根表，确认没有服务端 NeuroPet 状态机。插件本身不需要、也不提供这些命令。

**公开源码构建：** 单宠动作材质此前每版通过了 18,000 次模拟绑定。正式待发布包已重新构建并校验 CRC，补齐代码／封面说明和附加内容图标，并更新名称与署名。运行图集、动作材质和 HUD 布局与已验证版本逐字节相同；元数据变化使包的 SHA-256 不同。此品牌信息版本没有另做完整实机测试。同样，Duo 0.2.3 相对已测试的 0.2.2-preview 只改动了元数据、附加内容图标和封面来源说明。

</details>

## 我们的碎碎念

我们也知道，在一个本该时刻提防 Hunter 的游戏里，放一个挂在屏幕顶上的小家伙，好像有点奇怪。但她实在太可爱了，所以我们还是做了。后来姐妹也想一起来，于是现在有两只了。

我们计划把源码公开，是希望如果你也想做自己的小宠物，不用从零开始。（代码采用 MIT，角色图片沿用各自的许可，见下方。）

## 许可

本项目使用两种许可：

- **自写代码：** [MIT](https://choosealicense.com/licenses/mit/)。见 [LICENSE](LICENSE)。
- **角色图片、动作／行为配置及其改编**（包括 Duo 的抱抱镜像帧）：[CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)。见 [NOTICE](NOTICE.md) 和 `assets/mascot_pack/`。

MIT 许可**不适用于**这些图片。分享或改编图片与配置时，必须保留许可与署名、标明修改、仅限非商业用途，并以相同许可共享。

Valve 原版 HUD 模板从你自己的 L4D2 安装中读取，不以 MIT 重新授权。VSLib、SourceMod 社区实现和 Source SDK 2013 仅作为机制参考，均未包含在本项目中。

## 署名

- 项目制作：**Daisy, Shannon & Sol**
- 角色图片：**Paccha** – https://linktr.ee/paccha_
- 原动作与行为配置：**@promote.**（https://z.ne1.co 、https://neuro.us.to）和 **@dalekcraft**
- 原包打包与元数据：**qingchenyouforcc**
- 素材来源：**CommentOut64/web-mascot** – https://github.com/CommentOut64/web-mascot
- 素材上游：**NeurolingsCE-Qt** – https://github.com/qingchenyouforcc/NeurolingsCE-Qt

**本项目所做修改：** PNG 转换为带透明边框的 RGBA8888 VTF；按方向镜像；重新采样和排列动作时间；抱抱锚点归一；加入绊倒的停留与恢复；调整爬行节奏与移动限速；Evil Neuro 版将颜色延伸到全透明像素。Duo 在每套图集末尾追加一张全透明帧和原抱抱帧的像素镜像副本。原 PNG 文件未经改写。

封面和 Duo 视频片尾为基于角色素材及参考图的 AI 辅助插画，并非 Paccha 绘制的原始高清画稿。

Neuro-sama 和 Evil Neuro 是 Vedal 创作的 AI VTuber，Evil Neuro 是 Neuro-sama 的双胞胎姐妹。官方网站：https://vedal.ai/ · 直播：https://www.twitch.tv/vedal987 。本项目仅使用角色形象，不主张对角色的任何所有权，没有接入她们的 AI 或直播系统，与 Vedal 无关联、未获其认可。

## 反馈与贡献

欢迎报告问题和分享想法：[GitHub Issues（问题反馈）](https://github.com/Rbeyrolles/l4d2-neuropet/issues)。请注明使用的是哪一款及版本号。

参与贡献时，代码修改以 MIT 许可接受；图片或配置的修改须遵守 CC BY-NC-SA 4.0。

维护者：Daisy, Shannon & Sol
