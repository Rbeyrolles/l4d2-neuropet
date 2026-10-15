> 历史资料：本说明保留 2026-10-11 以前的单宠文案交接背景，不再描述当前发布状态。当前三款版本请看 [README](../README.zh-CN.md)、[FAQ](FAQ.md) 与 [发布记录](PUBLISHING.md)。

# 给 Claude：L4D2 Neuropet 发布文案讨论资料

可以直接复制本文件作为上下文。它独立说明项目现状，不要求 Claude 已读过开发聊天，也不要求它访问本地工作区。资料日期：2026-10-07。

## 这次希望一起讨论什么

我准备把 L4D2 Neuropet 的源码放到 GitHub，并考虑在 Steam 创意工坊发布两个角色版本。请先根据下面的事实讨论文案定位与结构，再帮助准备 GitHub 简介／README、Release notes、Neuron 与 Evil 两个工坊说明、简短 FAQ 和中文／英文版本。

语气希望温和、清楚、有一点可爱，重点是游戏时多一个小小的屏幕伙伴；不要夸大技术、保证兼容，也不要写成官方作品。以下内容是已核对的事实。涉及正式网址、工坊条目 ID 和上传授权的空缺，请列为待填写，不要编造。

## 1. 项目身份

- 项目工作名：**L4D2 Neuropet**。这是非官方粉丝制作的桌宠风格 HUD addon。
- 游戏：Left 4 Dead 2，Steam App ID 550。
- 角色二选一：Neuro-sama（原素材包名 **Neuron**），或 Evil Neuro（包名 **Eviling**）。
- 当前行为版本：Neuron **0.5.2**；Evil Neuro **0.5.3**。
- 两个角色版本分别打包；每次只启用一个。不是支持两个宠物同时活动的组合包。
- Neuro-sama 和 Evil Neuro 的角色背景及官方目的地见 https://vedal.ai/ ，官方直播频道为 https://www.twitch.tv/vedal987 。官网介绍她们为 AI VTuber，Evil 是 Neuro 的双胞胎姐妹。这里的小宠物仅使用角色形象，并没有接入她们的 AI、直播系统或聊天服务。
- 仓库／工坊实际地址尚未确定，不要虚构已经存在的订阅链接。

## 2. 玩家能看到什么

她会沿屏幕底边走动，也会小跑或慢慢趴着爬；可以攀爬左右屏幕边缘，沿顶部移动、悬挂、休息，偶尔松手跌落。底部停留点会变化，下一段从上次停下的地方继续。墙与顶部的停留、跌落位置也有变化。

不是一整套固定顺序循环。运行时按段抽取路线、速度、休息时间、目标位置、休息姿势和小插曲，抽到的行为在这一段保持稳定。

每个角色有八种休息表现：

| Neuron | Evil Neuro |
| --- | --- |
| 站立眨眼 | 站立眨眼 |
| 坐下眨眼 | 坐下眨眼 |
| 趴下偷懒 | 趴下偷懒 |
| 坐着抬头 | 坐着抬头 |
| Wink | 等抱抱 |
| 比心 | 趴着害羞 |
| 站着害羞 | 站着害羞 |
| 坐着害羞 | 坐着害羞 |

地面移动抽签：走路 60%、小跑 20%、慢爬 20%。慢爬会按距离延长时间，避免长距离动作幅度很小却滑得很快；两张原爬姿按 3 fps 交替。玩家已经确认速度和姿势交替舒服。

每段还抽一次小插曲：绊倒 20%、抱抱 20%、无插曲 60%。这些是抽签权重，不是每分钟概率。绊倒仅在走路或小跑时触发，不在慢爬、攀爬、原地休息时使用。抱抱可以在地面移动或休息时偶尔出现；适用的一段内最多一次，动作期间暂停移动，之后继续。

绊倒基准全程约 3.5 秒：失衡 → 倒地约 1.5 秒 → 撑起 → 坐起 → 站稳。全程受本段速度系数影响约为 3–4.1 秒，已经过人工节奏确认。

抱抱基准约 3.5 秒，保留原素材的双人画面，之后恢复当前宠物。画面里的另一角色只是这段动画的一部分，没有第二只宠物的独立逻辑。随机动作可能要等几分钟才出现，不应写成持续拥抱或可按键触发。

两侧与顶部允许少量图像出屏幕以呈现抓住边缘的感觉。底部不保留血条避让空间，角色可能与原 HUD 重叠。

## 3. 当前没有的功能

没有鼠标拖拽、点击互动、聊天、语音、AI 推理、完整 Shimeji 行为系统、多宠物关系、HUD 避障或实时二维碰撞物理。

当前客户端版**没有游戏事件联动**：不会精确监听玩家倒地／获救、Tank、Witch、尸潮或安全屋事件。视觉上的跌落来自随机片段及加速轨迹。如果动作恰好与事件同时发生，不应宣传成“被 Tank 吓掉下来”。

有一个早期服务端 VScript 研究原型，源码保存在 research 目录，它研究过状态机、物理和事件。它不属于当前普通本机 VPK 的运行实现，不能混进当前功能清单，也不是这次工坊候选包。

## 4. 安装、运行与兼容

| 角色 | VPK 文件 | 游戏附加内容名称 |
| --- | --- | --- |
| Neuron | l4d2_neuropet_client.vpk | Neuropet – Neuro-sama Screen Pet (Fan-made HUD Mascot) |
| Evil Neuro | l4d2_neuropet_evil_client.vpk | Neuropet – Evil Neuro Screen Pet (Fan-made HUD Mascot) |

手动安装：把一个 VPK 放到游戏的 left4dead2/addons/，在“附加内容”中启用，等加载完成后正常进入游戏。切换角色后重启；卸载时移除 VPK 并重启。

如果之后通过工坊订阅相同版本，不要再保留手动安装的重复副本。建议两角色分别发工坊条目、互相链接，并明确二选一；不要设置互相必须依赖。

运行时只需要普通客户端 addon。本机安装，服务器无需安装宠物脚本；玩家不需要 SourceMod、VSLib、Python、外部覆盖程序、浏览器、作弊命令或手动启动 VScript。Python 仅用于源码构建。

两版都覆盖 scripts/hudlayout.res。发布文案明确“不保证与第三方自定义 HUD Mod 兼容”，推荐原版 HUD；覆盖同一文件可能使宠物不显示或覆盖界面布局。第三方自定义 HUD Mod 如果也提供这一文件，不同加载顺序可以解释不同玩家的结果。当前发布版不自动合并 HUD；排障见 HUD_COMPATIBILITY.md。

服务器仍可以限制客户端 addons。允许 addon 的环境中架构不要求服务器脚本，但远程实测尚未完成，不能写“所有服务器通用”“突破服务器限制”或“Versus 已验证”。

默认按 16:9 校正比例；已验证 Windows、本地普通 coop、1280×720。其他宽高比可用源码参数重建，但分屏、感染者视角、Versus／Scavenge、其它比例仍有待验证。没有正式性能基准，也没有 VAC 或官方兼容认证。

## 5. 技术摘要，给 GitHub 读者

客户端 VGUI ImagePanel + VMT 材质代理 + 多帧 VTF。Python 在构建时读取原动作、生成图集、编译材质计算、读取使用者本机的原版 HUD 模板并写 VPK。游戏里由原生材质代理计算时间、随机选择、图片帧和位置。

运行包没有 Squirrel／mutation／SourceMod／DLL／外部程序。当前每包一个面板、202 帧图集、255 个材质代理、154 个自定义参数；图集用未压缩 RGBA8888，所以每个 VPK 约 50.6 MiB。没有量化性能数据，不能从实现简单推导“零性能损失”。

没有移植 web-mascot 的 TypeScript／DOM／XML 执行引擎。使用的是它单独许可的原素材与动作帧参考，行为和轨迹另行实现。不是 web-mascot 完整移植版，也没有接入 Neuro SDK。

源码目录包含构建器、两套素材、许可、文档和少量验证记录。没有整个原始 references 目录、Valve 游戏资源副本、SDK 二进制、私人路径或实验日志。HUD 原版模板从使用者本机游戏读取；VPK、生成图集和中间目录不进 Git 历史，建议作为 Releases 附件。

## 6. Evil 0.5.3 的白边修复

深色角色边缘曾出现浅色描边。分析发现原 PNG 的全透明像素保存着白色 RGB；纹理过滤时可能被混进边缘。现在把附近原画颜色延伸到四个像素步长内的全透明像素，保留全部透明度与所有可见 RGBA。

全部 202 帧已检查。角色尺寸、锚点、可见细节、完整动作材质和 HUD 布局保持原样。用户人工反馈：“明显减轻或已经看不到了”。可以写“减轻白边／修复透明边缘采样问题”，不要保证所有分辨率或环境永远完全没有边缘差异。

仓库中的白边对比图是数值采样模型的局部放大，不是实机截图。模型测得的约 85–93% 边缘误差下降不是玩家画面改善百分比，不宜写进工坊宣传数字。

## 7. 验证事实

Neuron 0.5.2 的本地普通 coop 测试为 75 秒，另有 120 秒固定慢爬演示；玩家确认爬行节奏舒服。Evil 0.5.3 的本地普通 coop 测试为 150 秒；玩家确认白边减轻。均为 1280×720、Windows，游戏正常退出，未发现宠物材质错误。

测试准备阶段曾临时用 cheats 停止 Director／保护测试玩家，观察动作时关闭 cheats，最后临时打开以查询服务端根表。不能把测试说成“全程从未打开 cheats”；宠物正常运行不依赖 cheats。根表查询确认没有服务器 NeuroPet 状态机。

公开源码整理后，两版均从新目录独立构建、逐文件读回 CRC，并各通过 18,000 次实际材质绑定模拟。正式待发布包为 10 文件：补齐代码／封面说明与附加内容图标，并更新正式名称和署名。运行材质、图集和 HUD 布局逐字节保持已验证版本；SHA-256 因元数据变化而不同，不能冒称新字节包已经另做完整实机测试。

远程服务器、其他模式、其他比例、性能和平台认证没有相应测试结论。

## 8. 许可与完整署名

推荐并已整理的方案：**自写代码 MIT；角色图片、配置及其改编 CC BY-NC-SA 4.0**。代码可以复用，但图片不能因为代码 MIT 而获得商用授权。分享素材及其改编还须保留许可、署名、标明修改、遵守非商业和相同方式共享。不要只写“带上作者就可以随便分发”。

角色图片作者：**Paccha** — https://linktr.ee/paccha_

原动作／行为配置：**@promote.**（https://z.ne1.co 、https://neuro.us.to）和 **@dalekcraft**。

原包打包与元数据：**qingchenyouforcc**。

本地素材来源项目：**CommentOut64/web-mascot** — https://github.com/CommentOut64/web-mascot

素材上游：**NeurolingsCE-Qt** — https://github.com/qingchenyouforcc/NeurolingsCE-Qt

素材许可： https://creativecommons.org/licenses/by-nc-sa/4.0/

转换说明：PNG → 带透明边框的 RGBA8888 VTF；方向镜像；动作采样／重排时间；抱抱锚点归一；绊倒停留与恢复；爬行节奏与运动限速；Evil 全透明 RGB 颜色延伸。原 PNG 不改写。

Neuro-sama／Evil Neuro 的身份与官方链接和具体图片许可是不同事项。本项目不能自称官方、已获 Vedal 认可或获得角色所有权。

Valve 的原 HUD 模板来自使用者自己的 L4D2 安装，不以 MIT 重新授权。VSLib、SourceMod 社区实现和 Source SDK 2013 只作机制参考，没有随当前客户端包一起提供。

## 9. 平台发布待确认

GitHub 仓库采用清楚的许可划分；VPK 放 Releases。创意工坊上传另涉及授予 Valve 平台使用等权利，上传者需要具备足够权利，不能仅凭免费分发或署名推定授权已经满足。需要核对实际上传条款，范围不明时向权利人确认。当前没有证据证明“工坊授权已经全部取得”，也不要反向断言“肯定不能发”。

项目制作署名已确定为 Daisy, Shannon & Sol，正式名称与左右呼应封面也已确定。源码仓库为 https://github.com/Rbeyrolles/l4d2-neuropet，反馈使用 https://github.com/Rbeyrolles/l4d2-neuropet/issues；首次上传采用 Private 可见性，供发布者审阅，尚未公开。release 标签、两个工坊 ID 和地址仍待发布者确定。宣传视频和图片另放在本地发布文件夹的 promotion/ 中，每个角色各一支双语视频，片尾按英文图 → 中文图结束。工坊公开文案中的源码链接应在仓库公开后使用。

建议待讨论问题：标题是否同时强调角色与“客户端观赏版”；中文和英文如何简洁说明二选一、HUD 冲突及服务器限制；署名区如何清楚区分作者、素材来源与角色官方渠道；FAQ 中是否解释抱抱双人画面、随机动作等待和没有游戏事件联动；首次公开发行如何兼顾温柔介绍与准确边界。

## 10. 推荐的文案框架与关键词

GitHub：一段简介 → 可见行为 → 安装 → 实现与构建 → 已知限制 → 许可证与署名 → 贡献／反馈。

工坊：简短介绍 → 主要动作 → 只启用本版 → 安装与 HUD 冲突 → 服务器限制和无事件联动 → 完整署名 → GitHub／另一角色链接。

可讨论的关键词：Left 4 Dead 2、L4D2、Neuro-sama、Evil Neuro、screen pet、HUD mascot、client-side、cosmetic、random animation、native VGUI、fan-made。它们是关键词建议，不代表已确认平台提供这些分类标签。

应避免：official、all servers、zero performance cost、real AI、full Shimeji、Tank/Witch reactions、拖拽、双宠互动、VAC-safe certified，以及没有证据的“已获得全部授权”。

## 官方／原始资料链接

- MIT： https://choosealicense.com/licenses/mit/
- CC BY-NC-SA 4.0： https://creativecommons.org/licenses/by-nc-sa/4.0/
- GitHub 许可说明： https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository
- Steam 上传条款第 6 节： https://store.steampowered.com/subscriber_agreement/#6
- Neuro-sama／Evil Neuro 官方站点： https://vedal.ai/

以上资料支持事实与边界，不应被文案工具扩展成不存在的功能、测试、许可或官方关系。


## 已确认的发布名称与封面

Neuropet – Neuro-sama Screen Pet (Fan-made HUD Mascot)

Neuropet – Evil Neuro Screen Pet (Fan-made HUD Mascot)

采用左右呼应的抱抱封面：Neuro 在左、Evil 在右，文字正向。封面为参考原抱抱素材的 AI 辅助设计，保持素材署名与同一许可。项目制作署名已确定为 Daisy, Shannon & Sol；游戏附加内容列表的简介采用简短的中英文两段。GitHub 与工坊地址仍待发布者确定。

## 2026-10-09 发布资料更新

游戏内创作者署名确定为 Daisy, Shannon & Sol，短简介改为英文＋中文。VPK 只改 addoninfo.txt，原运行资源、封面和素材署名不变；当前 SHA-256 见 RELEASE_CHECKS.md。最终交付采用一个 github/ 源码目录和两个 workshop/ 上传目录；另有首次发布说明。原双语长稿超过 Steam 接口说明的 8,000 字节上限，作为参考保留；实际上传使用各约 4.4 KB 的精简双语稿。精简稿省略未确定的网址，发布后再补源码与角色交叉链接。
