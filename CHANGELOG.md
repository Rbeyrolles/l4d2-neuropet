# 更新记录 / Changelog

Neuropet 有两个各自编号的发行系列：**单宠系列**（Neuro-sama、Evil Neuro）和 **Duo 双宠系列**。两个系列的版本号互不相关，即使出现相同的数字（例如都有过 0.2.0），也不是同一条升级线。Duo 0.2.3 不是从单宠 0.5.x 降级。

三款都在同一个源码仓库、同一条主分支中维护，分别构建和发布。

Neuropet has two separately numbered release series: the **single-pet series** (Neuro-sama, Evil Neuro) and the **Duo series**. Version numbers in one series have nothing to do with the other; a shared number such as 0.2.0 does not mean the same release.

---

## Duo 双宠系列 / Duo series

### Duo 0.2.3

- 加入选定的牵手封面（1024×1024 工坊 JPEG、包内 256×256 附加内容图标，原始 PNG 1254×1254）。
- 加入英文、中文两段游戏内简介，署名 Daisy, Shannon & Sol；配置位于 `publication-duo.json`。
- 更新封面来源说明，素材位于 `assets/promotion/duo/`。
- **行为不变：** HUD、两份行为材质、两套图集以及原画与代码许可与已测试的 0.2.2-preview 逐字节一致；只有元数据、附加内容图标和两份封面来源说明不同。牵手只是封面构图，游戏内互动仍是抱抱。

### Duo 0.2.2-preview

- 发起抱抱的角色不再由左右位置决定，Neuro 和 Evil 都可以主动发起，也不强制轮流。
- 靠近方式随距离变化：近距离走路，较远时小跑；不再固定用时。
- 可以从对方左侧或右侧靠近，并使用各自对应方向的抱抱画面（新增原抱抱帧的像素镜像副本，原画未重绘）。

### Duo 0.2.1-preview

- 修复两份材质更新时机不同导致的抱抱错位与提前恢复活动问题。
- 统一决策时钟及各阶段的坐标计算，抱抱期间两只使用共同的开始、结束和停靠位置。

### Duo 0.2.0-preview

- 首个本地双宠预览：两只分别活动，可在底边相遇抱抱或主动靠近。

---

## 单宠系列 / Single-pet series

### Evil Neuro 0.5.3

- 修正全透明像素中的隐藏白色 RGB，减轻深色角色的纹理过滤白边。
- 全部 alpha、可见 RGBA、角色尺寸、姿势锚点和动作材质保持原样。
- 用户确认白边明显减轻或已经看不到；本地普通 coop 测试通过。

### Neuro-sama 0.5.2 / Evil Neuro 0.5.2

- 长距离爬行按距离延长时间，两段地面爬行均有速度上限。
- 两张原爬姿按 3 fps 交替。
- Evil 使用独立素材包与材质路径；休息池以等抱抱／趴着害羞替换 Wink／比心。

### 0.5.1

- 绊倒加入约 1.5 秒倒地停留和逐步恢复姿势。

### 0.5.0

- 加入小跑、慢爬、绊倒及偶尔播放一次的原抱抱场景。

### 0.4.0

- 增加变化的地面停留点、墙与顶部跌落位置，以及八种地面休息表现。

### 0.3.0

- 由固定整套循环改为段落开始抽签、段内保持的随机活动。

### 0.2.0

- 原生客户端观赏版的固定循环验证。

---

## 源码与文档整理 / Repository

### 三款同库整理（2026-10-16）

- 同一仓库、同一主分支维护三个构建目标：Neuro-sama 单宠、Evil Neuro 单宠、Duo 双宠。
- 加入 Duo 构建入口 `tools/build_duo_interactive.py`、行为编译 `tools/duo_pair_graph.py` / `tools/duo_perimeter_behavior.py`、验证入口 `tools/check_duo_interactive.py` 和发布配置 `publication-duo.json`。
- README、构建说明、发布说明和本更新记录按三款整理。
- 此项整理不改变任何一款 VPK 的游戏行为或版本号。

### 公开源码整理（2026-10-07）

- 分离独立的 VPK/VTF 写入器与姿势数据。
- 构建器支持仓库内素材与从使用者本机游戏读取 HUD 模板。
- 增加 MIT 代码许可、第三方素材说明、可独立构建的源码目录和发布资料。
- 公开 VPK 增加 `CODE-LICENSE.txt`；游戏行为版本保持上表版本号，测试记录区分旧基线与公开包。
