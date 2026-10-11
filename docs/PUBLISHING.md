# GitHub 与创意工坊发布准备

资料核对日期：2026-10-09。下面区分已经完成的本地产物整理、正式发布时的操作，以及素材与平台条款的待确认事项。

## GitHub

把整理后的仓库根目录内容提交到 GitHub；不要把原工作区的整个 `references/`、生成的图集、旧实验日志或历史 VPK 一并推送。当前仓库已经包含构建所需的两套素材和许可、构建器、文档及验证资料。

根 `LICENSE` 是 MIT，只适用于自写代码和项目文档。`NOTICE.md` 和两个素材包的许可说明了第三方内容的独立授权。这样表述比“整个 Mod 都是 MIT、可随意商用”准确。GitHub 也建议开源项目提供明确许可，参见 [GitHub 许可文档](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository)。

建议把两个 VPK 和校验文件放到 GitHub Releases，而不是提交进 Git 历史。首次公开发行可写为“客户端观赏版：Neuron 0.5.2 / Evil 0.5.3”；仓库 release 标签是发布者的选择，并不要求把两角色版本强行改成同一个版本号。

项目制作署名已确定为 Daisy, Shannon & Sol。源码仓库为 [https://github.com/Rbeyrolles/l4d2-neuropet](https://github.com/Rbeyrolles/l4d2-neuropet)，问题反馈使用 [GitHub Issues](https://github.com/Rbeyrolles/l4d2-neuropet/issues)。2026-10-11 的首次上传采用 Private 可见性，供发布者审阅；源码尚未公开，工坊尚未上传。仓库链接在改为公开之前仅授权账号可访问，公开工坊文案中的源码链接应在仓库公开后使用。

## 创意工坊条目安排

推荐分别建立 **Neuron** 和 **Evil Neuro** 两个条目，在首屏写清“两个版本每次只启用一个”，并相互链接。它们是二选一外观，不是互相依赖的模组；不应设置成必须同时订阅启用。

上传内容是对应的 VPK，不是源码目录或 source ZIP。本地 L4D2 工具中存在 Workshop Manager；实际提交方式、可选分类、图片要求及附加条款以正式上传界面为准，本次没有实测上传。GitHub 手动 VPK 和工坊订阅版的重复安装也要在说明里提醒。

建议文案顺序：一句简短介绍 → 可见动作 → 客户端安装与只启用一版 → HUD 冲突／服务器限制 → 无游戏事件联动 → 素材署名及许可 → 源码和反馈链接。

## 素材与平台授权

本地素材包声明的 CC BY-NC-SA 4.0 允许遵守条件的分享与改编。除了署名，还要保留许可、标明修改、遵守非商业及相同方式共享条件。不能把原素材改成 MIT，也不能把代码 MIT 许可解释成图片可以商用。[CC 官方说明](https://creativecommons.org/licenses/by-nc-sa/4.0/)

Steam 上传条款第 6 节要求向 Valve 授予相应的使用、修改、分发等权利，并要求上传者具备足够的权利。是否免费只是其中一个因素；不能仅凭“写上作者”和“免费下载”就推定所有上传授权已满足。具体游戏页面还可能有附加条款。[Steam Subscriber Agreement](https://store.steampowered.com/subscriber_agreement/#6)

这里没有认定 CC 素材一定不能上工坊，也没有认定它自动满足工坊条款。正式上传前应核对适用条款；如范围不明确，向素材权利人确认免费 L4D2 工坊上传、转换动画、宣传图展示和平台所需授权是否获准，并保留确认记录。角色身份／名称的相关权利也与具体图片许可不同。Neuro 官方链接只是背景与署名信息，不是本项目得到官方背书或额外许可的证据。

## 宣传素材

建议准备简短实机片段，展示底部走路与慢爬、墙边攀爬、顶部悬挂、绊倒停留与起身、偶尔抱抱。真实随机抱抱可能等较久，可用诊断版录制特定动作，但需注明“动作演示”，最终发布包恢复默认随机行为。

当前仓库里的白边对比图是采样模型的局部放大，不是游戏截图；不得标成实机宣传图。旧固定版的历史截图也不能冒充最新包的完整实测。没有必要展示游戏事件恰好同时发生的画面来暗示事件联动。

如果做封面，使用有权使用的角色素材，保留必要署名与许可信息；不要把实际没有加入的音频、AI 对话或完整 Shimeji 交互画成可用功能。

## 正式提交时待填写

| 项目 | 目前状态 |
| --- | --- |
| GitHub 仓库地址／发布标签 | https://github.com/Rbeyrolles/l4d2-neuropet（首次上传为 Private）；发布标签待确定 |
| 项目制作署名、反馈渠道 | Daisy, Shannon & Sol；https://github.com/Rbeyrolles/l4d2-neuropet/issues |
| 两个工坊条目地址与 ID | 创建后填写 |
| 工坊上传授权是否覆盖 | 按实际条款核对，必要时获得补充确认 |
| 封面、最新版实机截图／短视频 | 封面已确认；宣传用实机片段仍可后续准备 |
| 远程服务器测试 | 未完成，不写“所有服务器可用” |
| 其他模式、宽高比、性能基准 | 未完成，不提前承诺 |

代码、素材、构建和文案事实资料已可供本地审阅。表中外部地址和授权确认属于正式发布者需要补齐的信息，不能由文案工具编造。

## 简洁发布目录

当前打包器默认生成 github/ 源码目录、两个 workshop/ 上传目录和一份首次发布说明。工坊每角色使用 VPK、preview.jpg、TITLE.txt 与 description-bilingual.txt。上传稿保留中英文介绍、功能边界和完整署名，已按 UTF-8 字节检查；[Steam 文档](https://partner.steamgames.com/doc/api/ISteamRemoteStorage#Constants) 对说明的上限为 8,000 字节。原长稿在 docs/workshop/ 保留为参考。
