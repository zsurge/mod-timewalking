# mod-timewalking

时光副本模块（骨架）。当前实现：**熔火之心（时光）** map `960`（复用 `MoltenCore` 资源），与原版 map `409` 并存。

## 规格（第一期骨架）

| 项 | 值 |
|---|---|
| Map ID | 960 |
| 名称 | 熔火之心（时光） / Molten Core (Timewalking) |
| 人数 | 10（`MapDifficulty.dbc` MaxPlayers；可改 DBC 后重打补丁） |
| 周锁 | 604800 秒（与原版 MC 分离） |
| 入口 | 达拉然 Krasus Landing NPC `9000100` 时光副本 |
| 换装 | NPC `9000101` 时光套装兑换（占位） |
| 掉落 | 下期：219 散件 + 代币换「时光」+原 T1 名套装 |

## 安装

1. 把本仓库放到 `modules/mod-timewalking`
2. 将 `client-patch/DBFilesClient/Map.dbc` 与 `MapDifficulty.dbc` 拷到 **服务端** `data/dbc/`（覆盖）
3. 客户端：把 `client-patch/patch-zhCN-TW.MPQ` 复制为 `Data/zhCN/patch-zhCN-9.MPQ`（或用 `tools/build_tw_dbc_mpq.py` 生成）。若 `patch-zhCN-Z.MPQ` 内已有 Map.dbc 且覆盖了 9，需用 MPQEditor 把两份 DBC 打进 Z
4. 开服让 updater 跑 `data/sql/db-world/zz_*.sql`，或手工导入
5. **本骨架无 C++ 逻辑**，不必为模块单独重编；若 CMake 未收录模块，SQL 需手工导入

## 游戏内验证

```
.reload creature
.go creature 5300800
```
与「时光副本」对话 →「进入熔火之心（时光）」→ 应进 map 960，可见 MC 怪/物件。

```
.go xyz 1091.89 -466.985 -105.084 960
```

## 下期

Boss 脚本绑定、血量、219 装、代币与套装商人货单。
