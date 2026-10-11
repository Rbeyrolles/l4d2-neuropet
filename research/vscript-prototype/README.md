# 早期服务端 VScript 原型

本目录保留项目最初的 Squirrel 状态机、模型检查、测试驱动和 mutation 入口，供研究历史设计。它需要服务器／主机执行脚本，并使用共享 Scripted HUD；不属于普通本机安装的客户端观赏版，不进入当前发行 VPK。

主要文件：`scripts/vscripts/neuropet/main.nut` 为事件与 HUD 连接，`model.nut` 为状态及运动，`model_tests.nut` 为模型检查，`lab.nut` 为历史测试辅助。`modes/neuropet.txt` 与 `scripts/vscripts/neuropet.nut` 是原 mutation 入口。

这里只提供原型源码，没有把 Valve HUD 资源、旧生成材质或实验 VPK 打包成一个可直接安装的目录。如继续开发，需要自行准备服务器部署、相应 HUD 资源、图集和游戏内验证。不能把这些原型中的事件反应、物理或 mutation 要求写进当前客户端版的功能说明。

本目录自写代码沿用仓库 MIT 许可。角色素材许可另见 `NOTICE.md`。
