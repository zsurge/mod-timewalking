import subprocess, os

MYSQL = r"D:\acore\mysql8.4\bin\mysql.exe"
OUT = r"E:\azerothcore\modules\mod-timewalking\data\sql\db-world"
os.makedirs(OUT, exist_ok=True)
NEW_MAP = 960
GUID_BASE_CREATURE = 5320000
GUID_BASE_GO = 5720000
NPC_ENTRANCE = 9000100
NPC_VENDOR = 9000101

def q(sql: str) -> str:
    r = subprocess.run(
        [MYSQL, "--host=127.0.0.1", "--port=3308", "-usurge", "-pacer@1123",
         "--default-character-set=utf8mb4", "-N", "-B", "-e", sql],
        capture_output=True,
    )
    out = r.stdout.decode("utf-8", "replace")
    err = r.stderr.decode("utf-8", "replace")
    if r.returncode != 0:
        raise SystemExit("SQL fail: " + err + out)
    return out

def esc(s):
    if s is None:
        return "NULL"
    return "'" + str(s).replace("\\", "\\\\").replace("'", "\\'") + "'"

def nul(v):
    return "NULL" if v in ("\\N",) else v

cols = "guid,id,map,zoneId,areaId,spawnMask,phaseMask,equipment_id,position_x,position_y,position_z,orientation,spawntimesecs,wander_distance,currentwaypoint,curhealth,curmana,MovementType,npcflag,unit_flags,dynamicflags"
raw = q(f"SELECT {cols} FROM acore_world.creature WHERE map=409 ORDER BY guid")
creatures = []
old_guids = []
for line in raw.strip().splitlines():
    if not line.strip():
        continue
    parts = line.split("\t")
    old_guids.append(int(parts[0]))
    creatures.append(parts)

desc = q("SHOW COLUMNS FROM acore_world.creature_addon")
addon_field_names = [ln.split("\t")[0] for ln in desc.strip().splitlines()]
addon_sel = ",".join(addon_field_names)
guid_list = ",".join(str(g) for g in old_guids) if old_guids else "0"
addon_raw = q(f"SELECT {addon_sel} FROM acore_world.creature_addon WHERE guid IN ({guid_list})")
addons = {}
for line in addon_raw.strip().splitlines():
    if not line.strip():
        continue
    parts = line.split("\t")
    addons[int(parts[0])] = parts

go_cols_desc = q("SHOW COLUMNS FROM acore_world.gameobject")
go_fields = [ln.split("\t")[0] for ln in go_cols_desc.strip().splitlines()]
go_raw = q(f"SELECT {','.join(go_fields)} FROM acore_world.gameobject WHERE map=409 ORDER BY guid")
gos = []
go_old = []
for line in go_raw.strip().splitlines():
    if not line.strip():
        continue
    parts = line.split("\t")
    go_old.append(int(parts[0]))
    gos.append(parts)

print(f"creatures {len(creatures)} addons {len(addons)} gos {len(gos)}")
cmap = {old: GUID_BASE_CREATURE + i for i, old in enumerate(old_guids)}
gmap = {old: GUID_BASE_GO + i for i, old in enumerate(go_old)}

L = []
L.append("-- zz_tw_molten_core_instance_960.sql")
L.append("-- Timewalking Molten Core skeleton: map 960 (reuse MoltenCore assets), weekly lockout, maxPlayers=10 via MapDifficulty.dbc")
L.append("-- Idempotent. Pair with client-patch DBFilesClient Map.dbc + MapDifficulty.dbc")
L.append("SET NAMES utf8mb4;")
L.append("")
L.append("DELETE FROM `instance_template` WHERE `map`=960;")
L.append("INSERT INTO `instance_template` (`map`,`parent`,`script`,`allowMount`) VALUES (960,230,'',0);")
L.append("")
L.append("DELETE FROM `dungeon_access_template` WHERE `map_id`=960;")
L.append("INSERT INTO `dungeon_access_template` (`map_id`,`difficulty`,`min_level`,`max_level`,`min_avg_item_level`,`comment`) VALUES")
L.append("(960,0,80,0,0,'Molten Core (Timewalking) - 10man');")
L.append("")
L.append(f"DELETE FROM `creature_addon` WHERE `guid` BETWEEN {GUID_BASE_CREATURE} AND {GUID_BASE_CREATURE+9999};")
L.append(f"DELETE FROM `creature` WHERE `guid` BETWEEN {GUID_BASE_CREATURE} AND {GUID_BASE_CREATURE+9999};")
L.append(f"DELETE FROM `creature` WHERE `map`=960 AND `id` NOT IN ({NPC_ENTRANCE},{NPC_VENDOR});")
L.append(f"DELETE FROM `gameobject` WHERE `guid` BETWEEN {GUID_BASE_GO} AND {GUID_BASE_GO+9999};")
L.append("DELETE FROM `gameobject` WHERE `map`=960;")
L.append("")
L.append(f"-- Creatures map 409 -> {NEW_MAP} ({len(creatures)} rows)")
L.append("INSERT INTO `creature` (`guid`,`id`,`map`,`zoneId`,`areaId`,`spawnMask`,`phaseMask`,`equipment_id`,`position_x`,`position_y`,`position_z`,`orientation`,`spawntimesecs`,`wander_distance`,`currentwaypoint`,`curhealth`,`curmana`,`MovementType`,`npcflag`,`unit_flags`,`dynamicflags`) VALUES")
cvals = []
for parts in creatures:
    old = int(parts[0])
    vals = [str(cmap[old]), parts[1], str(NEW_MAP)] + [nul(x) for x in parts[3:]]
    cvals.append("(" + ",".join(vals) + ")")
L.append(",\n".join(cvals) + ";")
L.append("")

if addons:
    L.append("-- creature_addon remapped")
    L.append("INSERT INTO `creature_addon` (`" + "`,`".join(addon_field_names) + "`) VALUES")
    avals = []
    for old, parts in addons.items():
        if old not in cmap:
            continue
        row = []
        for i, fname in enumerate(addon_field_names):
            v = parts[i] if i < len(parts) else "\\N"
            if fname == "guid":
                row.append(str(cmap[old]))
            elif fname == "auras":
                row.append("NULL" if v in ("\\N", "") else esc(v))
            else:
                row.append(nul(v))
        avals.append("(" + ",".join(row) + ")")
    L.append(",\n".join(avals) + ";")
    L.append("")

go_insert_fields = [
    "guid","id","map","zoneId","areaId","spawnMask","phaseMask",
    "position_x","position_y","position_z","orientation",
    "rotation0","rotation1","rotation2","rotation3",
    "spawntimesecs","animprogress","state",
]
idx = {name: i for i, name in enumerate(go_fields)}
L.append(f"-- Gameobjects map 409 -> {NEW_MAP} ({len(gos)} rows)")
L.append("INSERT INTO `gameobject` (`" + "`,`".join(go_insert_fields) + "`) VALUES")
gvals = []
for parts in gos:
    old = int(parts[0])
    row = []
    for f in go_insert_fields:
        if f == "guid":
            row.append(str(gmap[old]))
        elif f == "map":
            row.append(str(NEW_MAP))
        else:
            row.append(nul(parts[idx[f]]))
    gvals.append("(" + ",".join(row) + ")")
L.append(",\n".join(gvals) + ";")
L.append("")

path1 = os.path.join(OUT, "zz_tw_molten_core_instance_960.sql")
with open(path1, "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(L))
print("wrote", path1, "bytes", os.path.getsize(path1))
