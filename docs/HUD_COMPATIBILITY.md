# HUD conflicts and troubleshooting / HUD 冲突与排障

**Compatibility with third-party custom HUD mods is not guaranteed. The stock HUD is recommended.** All three Neuropet packages replace `scripts/hudlayout.res`. Another addon replacing it may hide the pet or override part of either HUD. The current release does not automatically merge third-party layouts or manage addon priority.

If the pet is missing:

1. Enable only one pet edition and keep only one installed copy. Avoid installing the same edition both manually and through Workshop.
2. Disable other HUD mods in the main-menu Add-ons list, restart L4D2, wait for addons to finish loading, and test in a normal local co-op map. The pet appears in gameplay, not on the main menu.
3. If that works, re-enable other addons one at a time and restart between checks to identify the conflict. Keep the conflicting HUD disabled when using Neuropet.
4. If it works locally but disappears on a server, that server may restrict client addons.

Seeing the pet and another HUD together on one machine does not establish compatibility: only one copy of the shared layout is selected. Priority changes may make the other addon win later. Renaming a VPK or changing subscription order is not a universal fix.

## 发布提示

**不保证与第三方自定义 HUD Mod 兼容，推荐使用原版 HUD。** 三款桌宠包都会替换 `scripts/hudlayout.res`。其他插件也修改它时，可能导致宠物不显示，或者某一方的界面布局被覆盖。当前发布版不提供自动合并第三方 HUD 或自动调整加载顺序的功能。

这不代表所有 UI 素材都会冲突；判断依据是是否覆盖相同资源。不过本项目不为第三方 HUD 逐个提供兼容保证。

## 为什么一台电脑正常，另一台电脑看不到？

如果第三方自定义 HUD Mod 也包含 `scripts/hudlayout.res`，而它的布局中没有 Neuropet 的面板，那么加载到这份布局时，宠物的图片和材质虽然还在，负责显示它的面板却可能没有被创建。

反过来，Neuropet 的布局生效时，宠物可能正常显示，但第三方自定义 HUD Mod 在这份文件里的部分布局设置也可能被覆盖。因此“现在两者都能看到”并不代表两份布局已经合并。安装方式和加载顺序不同，可以解释不同玩家的结果。

这是共享 HUD 文件的冲突，不是 Neuro-sama 和 Evil Neuro 的图片问题。当前版本没有可在客户端运行的脚本来扫描安装目录、合并其他 Mod 或改写加载列表。单靠给宠物的资源换一个独立名字，也不能让其他 HUD 的布局自动创建这个面板。

## 宠物不显示时

1. **只启用一版桌宠。** Neuro-sama 单宠、Evil Neuro 单宠与 Duo 双宠三选一；也检查是否留下了旧版或测试版。
2. **避免重复安装。** 工坊订阅与手动放入 `addons/` 的同一角色不要同时保留。
3. **先停用其他 HUD Mod。** 在主菜单“附加内容”中停用第三方自定义 HUD Mod；重启游戏，等待附加内容加载完成，再进入普通本地合作关卡测试。主菜单没有宠物属于正常情况。
4. **逐个定位。** 若宠物恢复显示，可以逐个重新启用其他插件，每次重启后检查。确认发生冲突的 HUD 后，使用桌宠时将它停用。
5. **区分服务器限制。** 若本地合作正常、某个服务器上不显示，该服务器可能限制客户端附加内容；这不一定是 HUD 冲突。

如果停用其他 HUD、只保留一版桌宠后，在本地合作关卡仍不显示，反馈时可提供：角色版本、安装方式、操作系统、分辨率、启用的 HUD 插件名称，以及是否只在某个服务器出现。截图和控制台报错有助于进一步定位，但不需要先手动解包 VPK。

## 关于加载优先级

提高桌宠优先级只能决定由哪一份完整的 HUD 布局生效，不能自动保留两份文件中的全部设置。重命名为 `000_*.vpk`、改变订阅先后或把 `addonlist.txt` 设为只读，都不作为本项目的通用修复方法。只读列表还可能妨碍后续正常启用、停用或添加 Mod。

需要同时保留某个特定 HUD 时，可以另行制作针对它的合并布局，但它依赖对方的具体版本，也仍需管理加载顺序。当前发布采用通用的兼容性提示与排障步骤，不附带第三方 HUD 的合并副本。

### 先确认只启用了一款 Neuropet

Neuro-sama、Evil Neuro 和 Duo 三款都会替换同一份 `scripts/hudlayout.res`，同时启用时只有其中一份会生效，宠物可能不显示或只显示其中一款。想要两只一起出现，请只启用 Duo，不要叠加两款单宠。

排查顺序：

1. 进入关卡后再查看；主菜单没有宠物是正常的。
2. 只保留一款 Neuropet：停用另一款单宠、旧版 Duo 和研究版，删除与工坊订阅重复的手动 VPK。
3. 停用其他 HUD Mod。
4. 完整重启游戏，在普通本地合作关卡检查。

本插件不会自动扫描、合并第三方 HUD，也不会调整加载优先级。某台电脑上能一起显示，不代表兼容保证。

### Make sure only one Neuropet package is enabled

Neuro-sama, Evil Neuro and Duo all replace the same `scripts/hudlayout.res`. If more than one is enabled, only one file wins, so the pets may be missing or only one package may show. For both pets on screen, enable Duo alone instead of stacking the two single pets.

In order:

1. Check after loading into a map; the main menu has no pets.
2. Keep one Neuropet package only: disable the other single pet, older Duo builds and the research build, and remove manual VPKs that duplicate a Workshop subscription.
3. Disable other HUD mods.
4. Fully restart the game and check in an ordinary local co-op map.

Neuropet doesn't scan or merge third-party HUDs or change load order. Seeing both on one PC is not a compatibility guarantee.
