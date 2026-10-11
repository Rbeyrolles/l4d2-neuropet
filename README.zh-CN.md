# L4D2 Neuropet

[English](README.md) | **简体中文**

Left 4 Dead 2 的粉丝自制屏幕小宠物。打僵尸的间隙，屏幕周围会有个小小的 Neuro-sama 或 Evil Neuro：走路、攀爬、休息，偶尔绊一跤，或者停下来抱抱。

> **非官方粉丝作品。** 与 Vedal 无关联、未获其认可。只改变 HUD 上显示的画面，不影响游戏玩法。不包含 AI、聊天、语音或联网功能，仅使用角色形象。

| Neuro-sama | Evil Neuro |
| --- | --- |
| ![Neuro-sama cover](assets/promotion/neuro-sama/cover.png) | ![Evil Neuro cover](assets/promotion/evil-neuro/cover.png) |

封面为基于原抱抱素材的 AI 辅助设计，非实机截图。制作说明见 [封面署名](assets/promotion/CREDITS.md)。

## 下载

两个角色分别打包。**二选一**，每次只启用一个。

> **HUD 兼容提示：** 不保证与第三方 HUD Mod 兼容。修改同一份 HUD 布局时，可能导致宠物不显示或界面布局被覆盖。建议使用原版 HUD；遇到问题先停用其他 HUD Mod 并重启游戏。详见 [HUD 冲突与排障](docs/HUD_COMPATIBILITY.md)。

| 角色 | 版本 | 创意工坊 | Release 文件 | 游戏内附加内容名称 |
| --- | --- | --- | --- | --- |
| Neuro-sama | 0.5.2 | 【待填：工坊链接】 | [l4d2_neuropet_client.vpk](https://github.com/Rbeyrolles/l4d2-neuropet/releases/download/client-2026-10-11/l4d2_neuropet_client.vpk) | Neuropet – Neuro-sama Screen Pet (Fan-made HUD Mascot) |
| Evil Neuro | 0.5.3 | 【待填：工坊链接】 | [l4d2_neuropet_evil_client.vpk](https://github.com/Rbeyrolles/l4d2-neuropet/releases/download/client-2026-10-11/l4d2_neuropet_evil_client.vpk) | Neuropet – Evil Neuro Screen Pet (Fan-made HUD Mascot) |

最终 VPK 和 SHA-256 校验文件已附在 [GitHub Release client-2026-10-11](https://github.com/Rbeyrolles/l4d2-neuropet/releases/tag/client-2026-10-11)。仓库当前为 Private，授权账号可以审阅与下载。

## 她会做什么

- **到处走走：** 沿底边走路、小跑或慢慢趴着爬；攀爬左右边缘；沿顶部移动和悬挂；偶尔松手跌落。
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

- **小插曲：** 绊倒再爬起来，以及一小段抱抱动画，她的双胞胎姐妹会友情客串。另一个角色只是抱抱动画的一部分，不是第二只宠物。
- **不是固定循环：** 每一段随机抽取路线、速度、休息时间、目标位置、休息姿势和小插曲，并在这一段内保持不变。底部停留点会变化，下一段从上次停下的地方继续；墙上、顶部的停留和跌落位置也会变化。

### 随机权重

以下是每段的抽签权重，不是每分钟的概率。有些动作可能要等几分钟才出现。

| 抽签 | 选项 |
| --- | --- |
| 地面移动 | 走路 60% · 小跑 20% · 慢爬 20% |
| 小插曲 | 绊倒 20% · 抱抱 20% · 无 60% |

- **绊倒** 只在走路或小跑时出现，慢爬、攀爬和休息时不会。基准时长约 3.5 秒：失衡 → 倒地约 1.5 秒 → 撑起 → 坐起 → 站稳。受本段速度系数影响，实际约 3–4.1 秒。
- **抱抱** 可在地面移动或休息时出现，每个适用的段落最多一次。基准约 3.5 秒，期间暂停移动，之后继续。
- **慢爬** 的时长随距离延长，避免小小的爬姿在屏幕上滑得太快。两张爬姿以 3 fps 交替。

### 她不会做的事

不能拖拽或点击，没有聊天、语音或 AI，没有完整的 Shimeji 行为系统、多宠物互动、HUD 避让或实时二维碰撞物理。

她也**不会读取或响应游戏事件**（倒地、救援、Tank、Witch、尸潮、安全屋）。跌落来自随机的动画片段。如果她刚好在 Tank 出现时掉下来，那只是时机太巧啦。

## 安装

**创意工坊：** 订阅两个条目中的一个。想换角色时，取消订阅一个、订阅另一个，然后重启游戏。

**手动安装：**

1. 把**一个** VPK 放进游戏目录下的 `left4dead2/addons/`。
2. 在主菜单的**附加内容**中启用，等它加载完成。
3. 正常进入游戏。

切换角色时替换 VPK 并重启；卸载时删除 VPK 并重启。如果之后通过创意工坊订阅了相同版本，请删除手动安装的副本，避免重复加载。

它作为普通客户端附加内容在你自己的电脑上运行。服务器无需安装任何东西，你也不需要 SourceMod、VSLib、Python、外部程序、浏览器或任何控制台命令。

## 兼容性与已知限制

- **HUD 插件：** 不保证与第三方 HUD Mod 兼容。两个版本都会替换 `scripts/hudlayout.res`；其他修改同一文件的插件可能使宠物不显示，或覆盖另一方的界面布局。B4B Modified HUD & UI（3041458606）也包含此文件。即使本机能同时显示，也不能视为兼容保证。请先停用其他 HUD Mod 并重启；见 [排障指南](docs/HUD_COMPATIBILITY.md)。
- **她会沿着底边走过。** 底边没有为血条预留空间；根据 HUD 的绘制顺序，她可能与控件重叠，也可能被部分遮住。
- **服务器：** 有些服务器不允许使用自定义的客户端附加内容。设计上不需要服务器安装任何东西，但尚未在远程服务器上测试。
- **屏幕比例：** 默认按 16:9 制作。其他比例可以用源码参数重新构建，但尚未验证。
- **目前已测试：** Windows、本地合作模式、1280×720。分屏、感染者视角、对抗、清道夫、其他比例和远程服务器均未测试。
- **性能：** 尚无正式的性能测试，因此不做任何性能承诺。
- **认证：** 未经 Valve 审核或认证。
- **大小：** 目前每个 VPK 约 50.6 MiB，因为帧图集以未压缩的 RGBA8888 保存。以后的版本可能会变化。

## 实现原理

一切都通过游戏自带的 HUD 和材质系统运行：

- 客户端 **VGUI ImagePanel** 负责绘制宠物。
- **VMT 材质代理** 在游戏内计算时间、随机选择、动画帧和位置。
- **多帧 VTF** 保存帧图集。

目前每个包有 1 个面板、202 帧图集、255 个材质代理和 154 个自定义参数。运行包内不含 Squirrel/VScript、mutation、SourceMod 插件、DLL 或外部程序。

**Python 只在构建时使用。** 构建器读取原动作帧、生成图集、编译材质逻辑、从*你自己的* L4D2 安装中读取原版 HUD 布局模板，然后写出 VPK。

### 从源码构建

需要：

- Python 3.10+ 和 Pillow
- 本机安装的 Left 4 Dead 2（构建器会从中读取原版 HUD 模板）

```
python -m pip install -r requirements.txt
python tools/build_client.py --character neuron --game-root "C:\Games\Left 4 Dead 2"
python tools/build_client.py --character evil --game-root "C:\Games\Left 4 Dead 2"
```

如需构建其他屏幕比例，请设置 `--aspect`。生成的图集、中间目录和 VPK 不提交到仓库；正式构建附在 Releases 中。

### 仓库内容

```text
assets/       mascot packs, covers and licenses
tools/        build, validation and packaging
docs/         behavior, tests and Workshop copy
research/     historical server-side VScript prototype
publication.json  titles, maintainer and accepted covers
```

- 构建器
- 两个角色的素材
- 许可文件
- 文档和少量验证记录
- `research/`：早期的服务端 VScript 研究原型，探索过状态机、物理和游戏事件。**它不属于当前的客户端插件，也不随任何 Release 发布。**

不包含：完整的原始 references 目录、Valve 游戏资源副本、SDK 二进制文件、私人路径或实验日志。

### 与 web-mascot 的关系

本项目**不是** [web-mascot](https://github.com/CommentOut64/web-mascot) 的移植版，没有移植它的 TypeScript/DOM/XML 引擎。本项目使用其单独许可的原素材与动作帧作参考，行为和移动轨迹另行实现。也没有接入 Neuro SDK。

### Evil Neuro 0.5.3 白边修复

Evil Neuro 的深色边缘周围曾出现浅色描边。原因是原 PNG 中全透明像素保存了白色 RGB，纹理过滤时可能被混入边缘。修复方法是把附近原画颜色延伸到四个像素步长内的全透明像素，所有透明度和所有可见 RGBA 像素保持不变。

全部 202 帧均已检查，尺寸、锚点、可见细节、材质和 HUD 布局都保持原样。实机测试中白边明显减轻或已看不到。我们不保证在所有分辨率或环境下都完全没有边缘差异。

仓库中的修复前后对比图是数值采样模型的局部放大，不是实机截图。模型中的误差下降数据只描述该模型，不代表玩家画面的改善百分比。

<details>
<summary><b>测试记录</b></summary>

所有测试：Windows、1280×720、本地合作模式。

- **Neuro-sama 0.5.2：** 75 秒测试，另有 120 秒固定慢爬演示。确认爬行节奏舒服。
- **Evil Neuro 0.5.3：** 150 秒测试。确认白边减轻。

两者游戏均正常退出，未发现宠物材质错误。

测试准备阶段，我们曾临时使用游戏内调试命令（例如暂停 AI Director、保护测试玩家），观察宠物时关闭，最后短暂打开以查询服务端根表，确认没有服务端 NeuroPet 状态机。插件本身不需要、也不提供这些命令。

**公开源码构建：** 动作材质此前每版通过了 18,000 次模拟绑定。正式待发布包已重新构建并校验 CRC，补齐代码／封面说明和附加内容图标，并更新名称与署名。运行图集、动作材质和 HUD 布局与已验证版本逐字节相同；元数据变化使包的 SHA-256 不同。此品牌信息版本没有另做完整实机测试。

</details>

## 我们的碎碎念

我们也知道，在一个本该时刻提防 Hunter 的游戏里，放一个挂在屏幕顶上的小家伙，好像有点奇怪。但她实在太可爱了，所以我们还是做了。

我们把源码公开，是希望如果你也想做自己的小宠物，不用从零开始。（代码采用 MIT，角色图片沿用各自的许可，见下方。）

## 许可

本项目使用两种许可：

- **自写代码：** [MIT](https://choosealicense.com/licenses/mit/)。见 [LICENSE](LICENSE)。
- **角色图片、动作／行为配置及其改编：** [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)。见 [NOTICE](NOTICE.md) 和 `assets/mascot_pack/`。

MIT 许可**不适用于**这些图片。分享或改编图片与配置时，必须保留许可与署名、标明修改、仅限非商业用途，并以相同许可共享。

Valve 原版 HUD 模板从你自己的 L4D2 安装中读取，不以 MIT 重新授权。VSLib、SourceMod 社区实现和 Source SDK 2013 仅作为机制参考，均未包含在本项目中。

## 署名

- 角色图片：**Paccha** – https://linktr.ee/paccha_
- 原动作与行为配置：**@promote.**（https://z.ne1.co 、https://neuro.us.to）和 **@dalekcraft**
- 原包打包与元数据：**qingchenyouforcc**
- 素材来源：**CommentOut64/web-mascot** – https://github.com/CommentOut64/web-mascot
- 素材上游：**NeurolingsCE-Qt** – https://github.com/qingchenyouforcc/NeurolingsCE-Qt

**本项目所做修改：** PNG 转换为带透明边框的 RGBA8888 VTF；按方向镜像；重新采样和排列动作时间；抱抱锚点归一；加入绊倒的停留与恢复；调整爬行节奏与移动限速；Evil Neuro 版将颜色延伸到全透明像素。原 PNG 文件未经改写。

Neuro-sama 和 Evil Neuro 是 AI VTuber，Evil Neuro 是 Neuro-sama 的双胞胎姐妹。官方网站：https://vedal.ai/ · 直播：https://www.twitch.tv/vedal987 。本项目仅使用角色形象，不主张对角色的任何所有权，与 Vedal 无关联、未获其认可。

## 反馈与贡献

欢迎报告问题和分享想法：[GitHub Issues（问题反馈）](https://github.com/Rbeyrolles/l4d2-neuropet/issues)

参与贡献时，代码修改以 MIT 许可接受；图片或配置的修改须遵守 CC BY-NC-SA 4.0。

维护者：Daisy, Shannon & Sol
