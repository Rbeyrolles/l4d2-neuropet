# HUD conflicts and troubleshooting / HUD 冲突与排障

**Compatibility with third-party HUD mods is not guaranteed. The stock HUD is recommended.** Both Neuropet editions replace `scripts/hudlayout.res`. Another addon replacing it may hide the pet or override part of either HUD. The current release does not automatically merge third-party layouts or manage addon priority.

If the pet is missing:

1. Enable only one pet edition and keep only one installed copy. Avoid installing the same edition both manually and through Workshop.
2. Disable other HUD mods in the main-menu Add-ons list, restart L4D2, wait for addons to finish loading, and test in a normal local co-op map. The pet appears in gameplay, not on the main menu.
3. If that works, re-enable other addons one at a time and restart between checks to identify the conflict. Keep the conflicting HUD disabled when using Neuropet.
4. If it works locally but disappears on a server, that server may restrict client addons.

Seeing the pet and another HUD together on one machine does not establish compatibility: only one copy of the shared layout is selected. Priority changes may make the other addon win later. Renaming a VPK or changing subscription order is not a universal fix.

## 发布提示

**不保证与第三方 HUD Mod 兼容，推荐使用原版 HUD。** 两个桌宠版本都会替换 `scripts/hudlayout.res`。其他插件也修改它时，可能导致宠物不显示，或者某一方的界面布局被覆盖。当前发布版不提供自动合并第三方 HUD 或自动调整加载顺序的功能。

这不代表所有 UI 素材都会冲突；判断依据是是否覆盖相同资源。不过本项目不为第三方 HUD 逐个提供兼容保证。

## 为什么一台电脑正常，另一台电脑看不到？

B4B Modified HUD & UI（工坊条目 3041458606）的本地 VPK 和 Neuropet 都包含 `scripts/hudlayout.res`。B4B 的这份布局没有 Neuropet 的面板。加载到 B4B 的布局时，宠物的图片和材质虽然还在，负责显示它的面板却没有被创建。

反过来，Neuropet 的布局生效时，宠物可能正常显示，但 B4B 在这份文件里的部分布局设置也可能被覆盖。因此“现在两者都能看到”并不代表两份布局已经合并。安装方式和加载顺序不同，可以解释不同玩家的结果。

这是共享 HUD 文件的冲突，不是 Neuro-sama 和 Evil Neuro 的图片问题。当前版本没有可在客户端运行的脚本来扫描安装目录、合并其他 Mod 或改写加载列表。单靠给宠物的资源换一个独立名字，也不能让其他 HUD 的布局自动创建这个面板。

## 宠物不显示时

1. **只启用一版桌宠。** Neuro-sama 与 Evil Neuro 二选一；也检查是否留下了旧版或测试版。
2. **避免重复安装。** 工坊订阅与手动放入 `addons/` 的同一角色不要同时保留。
3. **先停用其他 HUD Mod。** 在主菜单“附加内容”中停用整体更换 HUD 的插件，例如 B4B；重启游戏，等待附加内容加载完成，再进入普通本地合作关卡测试。主菜单没有宠物属于正常情况。
4. **逐个定位。** 若宠物恢复显示，可以逐个重新启用其他插件，每次重启后检查。确认发生冲突的 HUD 后，使用桌宠时将它停用。
5. **区分服务器限制。** 若本地合作正常、某个服务器上不显示，该服务器可能限制客户端附加内容；这不一定是 HUD 冲突。

如果停用其他 HUD、只保留一版桌宠后，在本地合作关卡仍不显示，反馈时可提供：角色版本、安装方式、操作系统、分辨率、启用的 HUD 插件名称，以及是否只在某个服务器出现。截图和控制台报错有助于进一步定位，但不需要先手动解包 VPK。

## 关于加载优先级

提高桌宠优先级只能决定由哪一份完整的 HUD 布局生效，不能自动保留两份文件中的全部设置。重命名为 `000_*.vpk`、改变订阅先后或把 `addonlist.txt` 设为只读，都不作为本项目的通用修复方法。只读列表还可能妨碍后续正常启用、停用或添加 Mod。

需要同时保留某个特定 HUD 时，可以另行制作针对它的合并布局，但它依赖对方的具体版本，也仍需管理加载顺序。当前发布采用通用的兼容性提示与排障步骤，不附带第三方 HUD 的合并副本。
