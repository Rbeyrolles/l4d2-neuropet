# GitHub 与创意工坊发布准备

发布状态更新于 2026-10-16（上一版 2026-10-15 为发布准备稿）。下面区分已经完成的本地产物整理、正式发布时的操作，以及素材与平台条款的待确认事项。

## 一个仓库，三款安装包

Neuropet 使用**一个源码仓库**，在同一条主分支维护三个构建目标：

| 安装包 | 当前版本 | VPK | 工坊条目 |
| --- | --- | --- | --- |
| Neuro-sama 单宠 | 0.5.2 | `l4d2_neuropet_client.vpk` | https://steamcommunity.com/sharedfiles/filedetails/?id=3820218016 |
| Evil Neuro 单宠 | 0.5.3 | `l4d2_neuropet_evil_client.vpk` | https://steamcommunity.com/sharedfiles/filedetails/?id=3820220066 |
| Duo 双宠 | 0.2.3 | `l4d2_neuropet_duo_interactive.vpk` | https://steamcommunity.com/sharedfiles/filedetails/?id=3820220607 |

GitHub 仓库和工坊条目是两个层面的安排：一个源码仓库对应三个独立的工坊条目。三款分别构建、分别上传，各自编号（单宠系列与 Duo 系列互不相关，见 [CHANGELOG](../CHANGELOG.md)）。

## GitHub

把整理后的仓库根目录内容提交到 GitHub；不要把原工作区的整个 `references/`、生成的图集、VPK、VTF、完整实机原始录像、个人实验目录、旧实验日志或历史 VPK 一并推送。仓库应包含共用的两套素材和许可、三款的构建入口、Duo 行为与验证工具、文档及必要的验证资料。

**当前状态：** 三款工坊条目均已发布；本仓库整合两款单宠及 Duo 的源码、封面、验证资料和已定稿文档。仓库地址与反馈地址如下，仓库可见性沿用拥有者当前设置：

- 源码仓库：https://github.com/Rbeyrolles/l4d2-neuropet
- 问题反馈：https://github.com/Rbeyrolles/l4d2-neuropet/issues

> 历史记录：2026-10-11 曾以 Private 可见性首次上传两款单宠，供发布者审阅。此处仅保留首次上传记录，不代表仓库当前可见性。

根 `LICENSE` 是 MIT，只适用于自写代码和项目文档。`NOTICE.md` 和两个素材包的许可说明了第三方内容的独立授权，Duo 追加的透明帧和抱抱镜像帧同样属于素材改编，沿用 CC BY-NC-SA 4.0。这样表述比「整个 Mod 都是 MIT、可随意商用」准确。GitHub 也建议开源项目提供明确许可，参见 [GitHub 许可文档](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository)。

### Releases

把三个 VPK 和校验文件放到 GitHub Releases，而不是提交进 Git 历史。三款可以分别发布，也可以在一次 Release 中附带多个文件；无论哪种方式，都要在 Release 说明里写清每个文件属于哪一款、哪个版本。

标签是发布者的选择，不要求三款统一版本号。为避免两个系列的版本号混淆，建议标签带上系列名，例如：

| 内容 | 标签候选 |
| --- | --- |
| 两款单宠（已有记录） | `client-2026-10-11` |
| Duo 0.2.3 | `duo-0.2.3`（未来创建 Duo Release 时可采用） |

以上只是命名建议，正式标签和下载地址在创建后回填，不要先把建议标签写成下载链接。

### 打包工具

`tools/package_publication.py` 目前只处理两款单宠，不会生成 Duo 的发布目录。如需三款统一打包，可在后续单独改造和验证。在此之前，Duo 的工坊上传文件从 Duo 构建输出中手动整理，见 [BUILDING.md](BUILDING.md)。

## 创意工坊条目安排

已建立 **Neuro-sama**、**Evil Neuro** 和 **Duo** 三个条目，在首屏写清「三款每次只启用一款；想要两只请选择 Duo」，并相互链接。它们是三选一的外观，不是互相依赖的模组；不应设置成必须同时订阅启用，也不要让 Duo 依赖两款单宠条目。

上传内容是对应的 VPK，不是源码目录或 source ZIP。本地 L4D2 工具中存在 Workshop Manager；实际提交方式、可选分类、图片要求及附加条款以正式上传界面为准，三款已由发布者实际上传；后续更新继续沿用各自条目。GitHub 手动 VPK 和工坊订阅版的重复安装也要在说明里提醒。

建议文案顺序：一句简短介绍 → 可见动作 → 三款选一款 → 客户端安装与只启用一款 → HUD 冲突／服务器限制 → 无游戏事件联动→ 素材署名及许可 → 源码和反馈链接。

已定稿文案（双语文件用于维护；上传时按语言分别填写）：

| 条目 | 上传稿 | 标题 |
| --- | --- | --- |
| Neuro-sama | `docs/workshop/workshop_neuro-sama_bilingual.txt` | Neuropet – Neuro-sama Screen Pet (Fan-made HUD Mascot) |
| Evil Neuro | `docs/workshop/workshop_evil-neuro_bilingual.txt` | Neuropet – Evil Neuro Screen Pet (Fan-made HUD Mascot) |
| Duo | `docs/workshop/workshop_duo_bilingual.txt` | Neuropet – Neuro-sama & Evil Neuro Screen Pets (Fan-made HUD Mascots) |

三个条目的互链已补齐。完整单语言稿位于 `docs/workshop/localized/`，每份分别填写工坊对应语言栏，不把双语母稿拼进同一栏；修改后重新检查 UTF-8 字节数（[Steam 文档](https://partner.steamgames.com/doc/api/ISteamRemoteStorage#Constants)：说明上限 8,000 字节，标题缓冲区 128+1 字节）。

## 素材与平台授权

本地素材包声明的 CC BY-NC-SA 4.0 允许遵守条件的分享与改编。除了署名，还要保留许可、标明修改、遵守非商业及相同方式共享条件。不能把原素材改成 MIT，也不能把代码 MIT 许可解释成图片可以商用。[CC 官方说明](https://creativecommons.org/licenses/by-nc-sa/4.0/)

Steam 上传条款第 6 节要求向 Valve 授予相应的使用、修改、分发等权利，并要求上传者具备足够的权利。是否免费只是其中一个因素；不能仅凭「写上作者」和「免费下载」就推定所有上传授权已满足。具体游戏页面还可能有附加条款。[Steam Subscriber Agreement](https://store.steampowered.com/subscriber_agreement/#6)

这里没有认定 CC 素材一定不能上工坊，也没有认定它自动满足工坊条款。正式上传前应核对适用条款；如范围不明确，向素材权利人确认免费 L4D2 工坊上传、转换动画、宣传图展示和平台所需授权是否获准，并保留确认记录。角色身份／名称的相关权利也与具体图片许可不同。Neuro 官方链接只是背景与署名信息，不是本项目得到官方背书或额外许可的证据。

## 宣传素材

| 素材 | 状态 |
| --- | --- |
| 单宠封面 ×2 | 已确认 |
| Duo 牵手封面 | 已选定；原始 PNG 1254×1254，另有 1024×1024 工坊 JPEG 和包内 256×256 图标 |
| Duo 宣传视频 `neuropet-duo-bilingual.mp4` | 已完成：141.7 秒（02:21），1920×1080，30 fps，无配乐或旁白，中英文提示在同一支视频内；发布展示通过工坊页面整理；此处不预填独立视频地址 |
| Duo 截图 ×3 | 已完成：底边、两侧攀爬、抱抱；均直接取自视频，1920×1080 JPEG，各小于 1 MB |

宣传时请保持以下说明：

- 视频为集中展示安排了初始位置、动作和互动机会，速度与动画帧率保持原值；发布版仍随机选择，视频不是固定循环路线的承诺。
- 封面的牵手和片尾的挥手是 AI 辅助宣传插画，不是游戏新增行为或实机截图；游戏内互动是抱抱。
- 不能把整张宣传图说成 Paccha 绘制的原始高清画稿。
- 仓库里的白边对比图是采样模型的局部放大，不是游戏截图；不得标成实机宣传图。旧固定版的历史截图也不能冒充最新包的完整实测。
- 不展示游戏事件恰好同时发生的画面来暗示事件联动；不把实际没有加入的音频、AI 对话或完整 Shimeji 交互画成可用功能。

## 当前发布记录与后续验证

| 项目 | 目前状态 |
| --- | --- |
| GitHub 仓库地址与公开状态 | https://github.com/Rbeyrolles/l4d2-neuropet；三款同库维护，可见性沿用拥有者设置 |
| Release 标签与下载地址 | 单宠：client-2026-10-11；Duo 当前从工坊订阅，未在本次源码同步中创建新 Release |
| 项目制作署名、反馈渠道 | Daisy, Shannon & Sol；https://github.com/Rbeyrolles/l4d2-neuropet/issues |
| 三个工坊条目地址与 ID、相互链接 | 三个地址已填入上表，语言稿互链已补齐 |
| 宣传视频平台、链接、发布日期 | 展示入口见 Duo 工坊页面；不设置独立视频待填链接 |
| 工坊上传授权是否覆盖 | 按实际条款核对，必要时获得补充确认 |
| Duo VPK 大小 | 115.7 MiB；正式包 121,324,135 字节，以随包校验记录为准 |
| 远程服务器测试 | 未完成，不写「所有服务器可用」 |
| 其他模式、宽高比、性能基准 | 未完成，不提前承诺 |

正式链接和署名已填入；远程服务器、其他模式、宽高比及性能测试仍保留实际验证范围，不提前承诺。

## 发布目录

单宠：打包器默认生成 `github/` 源码目录、两个 `workshop/` 上传目录和一份首次发布说明。每角色使用 VPK、`preview.jpg`、`TITLE.txt` 与说明 TXT。历史文件名 `description-bilingual.txt` 继续保留，但当前默认上传内容为英文；其他语言分别取自 `docs/workshop/localized/`，双语母稿在 `docs/workshop/` 保留用于维护。

Duo：从构建输出单独整理 VPK、1024×1024 `preview.jpg`、标题与对应语言 TXT；不重复创建条目，继续更新现有 Duo 工坊条目。
