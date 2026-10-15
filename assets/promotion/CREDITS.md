# 封面署名与制作说明

正式封面采用用户确认的左右呼应版本：Neuro-sama 封面的主角在左，Evil Neuro 封面的主角在右。两个 `cover.png` 保留所选图片原始字节。

角色原图由 **Paccha** 绘制：https://linktr.ee/paccha_ 。素材来自 CommentOut64/web-mascot 的 Neuron／Eviling 包，上游 qingchenyouforcc/NeurolingsCE-Qt。原图与改编继续按 **CC BY-NC-SA 4.0** 许可，完整许可位于 `assets/mascot_pack/`，也随 VPK 提供。

封面通过内置 imagegen 参考原抱抱图片，制作背景、装饰、文字和 AI 辅助放大重绘；Neuro-sama 版另对中央人物做了镜像编辑。整张封面不是 Paccha 绘制的原始高清画稿，也不是游戏截图。生成和编辑提示词保存在本目录。

**AI-assisted cover composition and mirrored edit based on original mascot artwork by Paccha (CC BY-NC-SA 4.0).**

游戏列表图标和工坊 JPEG 仅对所选封面做尺寸／格式导出，没有再次重绘。游戏内角色图集保持原样。对应修改说明随 VPK 的 `COVER-CREDITS.txt` 提供。

工坊 `preview.jpg` 为 1024×1024 JPEG，并检查低于 1 MB。Steam 的上传文档对预览图列出这一大小限制，参见 [SubmitItemUpdateResult_t](https://partner.steamgames.com/doc/api/ISteamUGC#SubmitItemUpdateResult_t)。原始 `cover.png` 用作高清保存与 GitHub 展示，不作为默认工坊上传预览文件。

## 双宠版 / Duo

双宠版使用用户在 2026-10-15 选定的牵手构图，保存在 `duo/cover.png`。所选 PNG 保留原始字节，SHA-256 为 `bae2161dc3361a0e7fca5260c941f9567aff2c23998f788c55713598a32f6f90`。这是参考原角色素材、既有封面风格与 Evil 表情制作的 AI 辅助宣传插画；牵手是封面构图，不代表游戏内新增了牵手行为。双宠的游戏图集与行为没有因封面而修改。

双宠封面的署名、来源和改编说明保存在 `duo/COVER-CREDITS.txt`，随 VPK 的两套角色资源共同提供；选定构图的提示词保存在 `duo/prompt.txt`。元数据与封面路径使用单独的 `publication-duo.json`，不改动两款单宠的发布配置。
