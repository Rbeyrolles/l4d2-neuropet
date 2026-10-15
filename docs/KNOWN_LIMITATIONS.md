# 已知限制与测试边界

| 项目 | 当前状态 |
| --- | --- |
| Windows 本地普通 coop，1280×720、16:9 | 已测试 |
| 只在本机安装、不要求服务器脚本 | 运行架构已实现；服务器仍可限制 addons |
| 所有远程服务器通用 | 未验证，不能保证 |
| Versus／Scavenge、感染者视角、分屏 | 未验证 |
| 其他宽高比 | 支持重建比例参数，实际显示仍需测试 |
| 其它 HUD addon | 不保证兼容；覆盖同一 `scripts/hudlayout.res` 时可能使宠物不显示或覆盖界面布局 |
| 两角色同时出现 | Duo 内已支持；两款单宠互相叠加不会自动成为 Duo，三款包只启用一款 |
| 性能、帧率、内存 | 未做正式量化基准 |
| VAC 或官方兼容认证 | 没有认证，不作保证 |

当前版没有精确的游戏事件联动、聊天、AI 推理、音频、鼠标拖拽、完整多宠物关系系统、HUD 避障、通用行为系统或实时二维碰撞物理。Tank／Witch／尸潮出现时发生的动作可能只是随机巧合，不能描述成事件反应。

服务器可以限制客户端 addons。遇到服务器限制时，请使用允许自定义 HUD 的环境；本项目不提供绕过限制的方法。运行现成 VPK 不需要 `sv_cheats`。

推荐使用原版 HUD。三款与其他修改同一 HUD 布局的 addon 可能互相覆盖；当前发布版不会自动检测、合并或调整第三方 HUD。先停用重复宠物副本及其他 HUD Mod，再重启游戏重新加载资源。创意工坊订阅和手动安装同一版本不要重复保留。具体排障步骤见 [HUD 冲突与排障](HUD_COMPATIBILITY.md)。

Evil 0.5.3 已减轻由隐藏白色 RGB 导致的过滤白边。原画自身的红色或浅色轮廓、正常抗锯齿、截图压缩和不同分辨率仍可能影响观感，不能承诺任意环境下完全没有边缘差异。

## Duo 双宠版的额外限制

- **互动只在底边。** 墙面和顶部不会抱抱；没有通用的碰撞避让，也没有牵手或跟随。未触发互动时，两只可能重叠。
- **不保证固定频率。** 抱完至少约 45 秒才可能再次互动，还要满足位置和随机条件。宣传视频为展示安排了互动机会，不代表正式版的频率。
- **同步边界。** 短暂漏帧、不同绘制频率和抱完恢复已检查。若其中一只长时间停止绘制、错过整个互动发起阶段，或只重新加载了两份材质中的一份，仍可能不同步。遇到时请完整重启游戏。我们不承诺绝不闪烁或绝不错位。
- **性能。** Duo 的材质计算与绘制开销高于单宠，尚未做 FPS 差异测量。
- **已测环境。** Windows、1280×720、本地合作模式；宣传视频另在 1920×1080 实机录制。其他宽高比、分屏、感染者视角、对抗、清道夫和远程服务器尚无测试结论。

## Additional limits for Duo

- **Floor-only interactions.** No hugging on walls or the ceiling, no general collision avoidance, no hand-holding or following. When no interaction is happening, the two pets may overlap.
- **No fixed frequency.** After a hug there's at least about 45 seconds before the next interaction, and position and chance also play a part. The promotional video staged its meetings; it doesn't reflect the release's frequency.
- **Sync limits.** Short frame drops, different draw rates and recovery after a hug have been checked. A long pause in drawing just one pet, missing the whole start of an interaction, or reloading only one of the two materials can still break sync. Fully restart the game if that happens. We don't promise zero flicker or mismatch.
- **Performance.** Duo does more material calculation and drawing than a single pet. FPS differences haven't been measured.
- **Tested setup.** Windows, 1280×720, local co-op; the promotional video was also recorded in game at 1920×1080. Other aspect ratios, split-screen, infected view, Versus, Scavenge and remote servers have no test results yet.
