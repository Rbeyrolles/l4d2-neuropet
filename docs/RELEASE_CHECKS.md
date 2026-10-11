# 正式发布文件检查

2026-10-09：游戏内简介与项目署名更新，发布资料采用简洁目录。

| 角色 | 版本 | 文件数 | VPK SHA-256 |
| --- | --- | --- | --- |
| Neuron | 0.5.2 | 10 | 6fb101a0d5fbcee878adac715c24cdeff0bc5d93f18dbe9c1e827f8f77094fa3 |
| Evil Neuro (Eviling) | 0.5.3 | 10 | 76eb6a91607ccc240a7d90abe33c0498780026cad852409576e68ab5fef2b55a |

两版 addonAuthor 均为 **Daisy, Shannon & Sol**。addonDescription 为英文与中文两段，以实际换行写入 UTF-8。源码构建器和包内字段使用同一份 publication.json 配置；原画、配置和封面作者的署名仍保留在 NOTICE、工坊文案与原有包内许可／说明中。

本轮与 2026-10-07 的 10 文件候选包逐文件比较：只改 addoninfo.txt，其余 9 个条目逐字节一致，包含动作材质、202 帧图集、HUD 布局、附加内容图标、Evil 白边修复和所有原有许可。完整 VPK CRC、素材指纹、UTF-8 元数据、标题、封面、透明边框、255 个代理及 154 个参数检查通过。速度为 1，诊断关闭。

因此本轮没有重复启动游戏或重新执行 18,000 次行为模拟；也不声称已经另行实测新简介的界面排版。此前验证过的实际运行资源保持相同。每个角色的 metadata-equivalence-2026-10-09.json 记录与前一候选包的身份对应。

历史实机环境为 Windows、本地普通 c1m1_hotel coop、1280×720。Neuron 0.5.2 有 75 秒随机版和 120 秒慢爬演示；Evil 0.5.3 有 150 秒白边修复观察。用户确认爬行节奏舒服、白边减轻；游戏正常退出，未发现宠物材质错误。准备阶段曾临时用 cheats 控制测试环境，观察时关闭。正常运行不依赖 cheats；远程服务器、其他模式、宽高比和正式性能基准仍未验证。

精简工坊上传稿各为 4,469 UTF-8 字节，低于 [Steam 说明上限](https://partner.steamgames.com/doc/api/ISteamRemoteStorage#Constants)；完整双语长稿仍保留为参考，不作为默认上传文件。标题和封面原样保留，预览图为 1024×1024 JPEG。发布文件夹只有 github/、workshop/ 和首次发布说明，不再默认生成多层 ZIP。

详细记录见 docs/evidence/neuron-0.5.2/ 与 docs/evidence/evil-0.5.3/；native-baseline.json 和 branding-equivalence.json 为历史记录。机器可读简表为 [release-facts.json](release-facts.json)。

封面是 AI 辅助艺术设计，白边对比图是数值模型局部放大；两者都不能标成当前包的实机截图。
