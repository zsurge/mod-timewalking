# -*- coding: utf-8 -*-
"""Generate TW MC scale SQL: only bosses -> L83 clones; trash keep original entries/levels."""
import os, subprocess

MYSQL = r"D:\acore\mysql8.4\bin\mysql.exe"
OUT = r"E:\azerothcore\modules\mod-timewalking\data\sql\db-world\zz_tw_mc_scale_80.sql"
ENTRY_BASE = 9100000  # new_entry = ENTRY_BASE + old_entry

# Classic MC boss creature_template entries (rank Boss)
MC_BOSSES = {
    12118,  # Lucifron
    11982,  # Magmadar
    12259,  # Gehennas
    12057,  # Garr
    12264,  # Shazzrah
    12056,  # Baron Geddon
    12098,  # Sulfuron Harbinger
    11988,  # Golemagg the Incinerator
    12018,  # Majordomo Executus
    11502,  # Ragnaros
}

def q(sql: str) -> str:
    env = os.environ.copy()
    env["MYSQL_PWD"] = "acer@1123"
    r = subprocess.run(
        [MYSQL, "--host=127.0.0.1", "--port=3308", "--user=surge", "--protocol=TCP",
         "--default-character-set=utf8mb4", "-N", "-B", "-e", sql, "acore_world"],
        capture_output=True, env=env,
    )
    out = r.stdout.decode("utf-8", "replace")
    err = r.stderr.decode("utf-8", "replace")
    if r.returncode != 0:
        raise SystemExit("SQL fail: " + err + out)
    return out

def boss_hm(old: float) -> float:
    # Magmadar 248 -> ~372 (~1.2x T7 Patchwerk 310)
    return round(old * (310.0 / 248.0) * 1.2, 1)

# Distinct ids on map 960, normalized to original entry (strip TW base if already remapped)
ids_raw = q(
    "SELECT DISTINCT IF(id>={0} AND id<{0}+100000, id-{0}, id) AS oid "
    "FROM creature WHERE map=960 AND id NOT IN (9000100,9000101) ORDER BY oid".format(ENTRY_BASE)
)
all_oids = [int(x) for x in ids_raw.split() if x.strip()]
boss_oids = [oid for oid in all_oids if oid in MC_BOSSES]
trash_oids = [oid for oid in all_oids if oid not in MC_BOSSES]
print("all", len(all_oids), "bosses", boss_oids, "trash", len(trash_oids))

rows = {}
for oid in boss_oids:
    line = q(
        "SELECT entry,name,subname,minlevel,maxlevel,`exp`,`rank`,HealthModifier,DamageModifier "
        f"FROM creature_template WHERE entry={oid}"
    ).strip()
    if not line:
        # maybe only TW clone exists
        line = q(
            "SELECT entry,name,subname,minlevel,maxlevel,`exp`,`rank`,HealthModifier,DamageModifier "
            f"FROM creature_template WHERE entry={ENTRY_BASE+oid}"
        ).strip()
        if not line:
            raise SystemExit(f"missing template {oid}")
    p = line.split("\t")
    # Prefer original template for base HM if available
    orig = q(
        f"SELECT HealthModifier,DamageModifier,minlevel,`rank`,name FROM creature_template WHERE entry={oid}"
    ).strip()
    if orig:
        op = orig.split("\t")
        rows[oid] = {
            "entry": oid, "name": op[4],
            "HealthModifier": float(op[0]), "DamageModifier": float(op[1]),
            "minlevel": int(op[2]), "rank": int(op[3]),
        }
    else:
        rows[oid] = {
            "entry": oid, "name": p[1],
            "HealthModifier": float(p[7]), "DamageModifier": float(p[8]),
            "minlevel": int(p[3]), "rank": int(p[6]),
        }

cols = [ln.split("\t")[0] for ln in q("SHOW COLUMNS FROM creature_template").strip().splitlines()]
col_sql = ",".join(f"`{c}`" for c in cols)

L = []
L.append("-- zz_tw_mc_scale_80.sql")
L.append("-- Timewalking MC: ONLY bosses cloned to L83 (~T7+20%); trash keep original L62 templates.")
L.append("-- new_entry = 9100000 + old_entry. Idempotent.")
L.append("SET NAMES utf8mb4;")
L.append("")

# Cleanup ALL previous TW clones for map-960 creature set (bosses+trash), then re-create bosses only
prev_raw = q(
    "SELECT DISTINCT id FROM creature WHERE map=960 AND id>={0} AND id<{0}+100000".format(ENTRY_BASE)
)
# Also clean known old clone range from prior full clone
clean_ids = sorted(set(
    [ENTRY_BASE + oid for oid in all_oids] +
    [int(x) for x in prev_raw.split() if x.strip()]
))
if clean_ids:
    id_list = ",".join(str(x) for x in clean_ids)
    L.append("-- Cleanup previous TW clones (boss+trash from earlier full scale)")
    L.append(f"DELETE FROM `smart_scripts` WHERE `source_type`=0 AND `entryorguid` IN ({id_list});")
    L.append(f"DELETE FROM `creature_template_spell` WHERE `CreatureID` IN ({id_list});")
    L.append(f"DELETE FROM `creature_template_resistance` WHERE `CreatureID` IN ({id_list});")
    L.append(f"DELETE FROM `creature_template_movement` WHERE `CreatureId` IN ({id_list});")
    L.append(f"DELETE FROM `creature_equip_template` WHERE `CreatureID` IN ({id_list});")
    L.append(f"DELETE FROM `creature_template_addon` WHERE `entry` IN ({id_list});")
    L.append(f"DELETE FROM `creature_template_model` WHERE `CreatureID` IN ({id_list});")
    L.append(f"DELETE FROM `creature_template_locale` WHERE `entry` IN ({id_list});")
    L.append(f"DELETE FROM `creature_template` WHERE `entry` IN ({id_list});")
    L.append("")

L.append("-- Revert ALL map 960 combat spawns to original ids first")
L.append(
    f"UPDATE `creature` SET `id`=`id`-{ENTRY_BASE} "
    f"WHERE `map`=960 AND `id`>={ENTRY_BASE} AND `id`<{ENTRY_BASE}+100000 "
    f"AND `id` NOT IN (9000100,9000101);"
)
L.append("")

if not boss_oids:
    raise SystemExit("no bosses found on map 960")

boss_list = ",".join(str(x) for x in boss_oids)
new_boss = [ENTRY_BASE + oid for oid in boss_oids]
new_list = ",".join(str(x) for x in new_boss)

L.append("-- Clone ONLY boss templates to L83")
for oid in boss_oids:
    nid = ENTRY_BASE + oid
    t = rows[oid]
    hm = boss_hm(t["HealthModifier"])
    dm = 42.0
    exprs = []
    for c in cols:
        if c == "entry":
            exprs.append(str(nid))
        elif c in ("difficulty_entry_1", "difficulty_entry_2", "difficulty_entry_3"):
            exprs.append("0")
        elif c in ("minlevel", "maxlevel"):
            exprs.append("83")
        elif c == "exp":
            exprs.append("2")
        elif c == "HealthModifier":
            exprs.append(str(hm))
        elif c == "DamageModifier":
            exprs.append(str(dm))
        elif c in ("lootid", "pickpocketloot", "skinloot", "mingold", "maxgold"):
            exprs.append(f"`{c}`")  # keep original loot until 219 tables exist
        elif c == "name":
            exprs.append("CONCAT(`name`,'（时光）')")
        else:
            exprs.append(f"`{c}`")
    L.append(f"INSERT INTO `creature_template` ({col_sql})")
    L.append(f"SELECT {', '.join(exprs)} FROM `creature_template` WHERE `entry`={oid};")

L.append("")
L.append("-- Boss models / locale / addon / equip / movement / resistance / spell")
L.append(
    f"INSERT INTO `creature_template_model` (`CreatureID`,`Idx`,`CreatureDisplayID`,`DisplayScale`,`Probability`) "
    f"SELECT `CreatureID`+{ENTRY_BASE},`Idx`,`CreatureDisplayID`,`DisplayScale`,`Probability` "
    f"FROM `creature_template_model` WHERE `CreatureID` IN ({boss_list});"
)
L.append(
    f"INSERT INTO `creature_template_locale` (`entry`,`locale`,`Name`,`Title`,`VerifiedBuild`) "
    f"SELECT `entry`+{ENTRY_BASE},`locale`,CONCAT(`Name`,'（时光）'),`Title`,`VerifiedBuild` "
    f"FROM `creature_template_locale` WHERE `entry` IN ({boss_list});"
)
L.append(
    f"INSERT INTO `creature_template_addon` "
    f"SELECT `entry`+{ENTRY_BASE}, `path_id`, `mount`, `bytes1`, `bytes2`, `emote`, `visibilityDistanceType`, `auras` "
    f"FROM `creature_template_addon` WHERE `entry` IN ({boss_list});"
)

eq_cols = [ln.split("\t")[0] for ln in q("SHOW COLUMNS FROM creature_equip_template").strip().splitlines()]
eq_sel = [f"`CreatureID`+{ENTRY_BASE}" if c == "CreatureID" else f"`{c}`" for c in eq_cols]
L.append(
    f"INSERT INTO `creature_equip_template` ({','.join('`'+c+'`' for c in eq_cols)}) "
    f"SELECT {', '.join(eq_sel)} FROM `creature_equip_template` WHERE `CreatureID` IN ({boss_list});"
)

mov_cols = [ln.split("\t")[0] for ln in q("SHOW COLUMNS FROM creature_template_movement").strip().splitlines()]
mov_id = "CreatureId" if "CreatureId" in mov_cols else "CreatureID"
mov_sel = [f"`{mov_id}`+{ENTRY_BASE}" if c == mov_id else f"`{c}`" for c in mov_cols]
L.append(
    f"INSERT INTO `creature_template_movement` ({','.join('`'+c+'`' for c in mov_cols)}) "
    f"SELECT {', '.join(mov_sel)} FROM `creature_template_movement` WHERE `{mov_id}` IN ({boss_list});"
)

res_cols = [ln.split("\t")[0] for ln in q("SHOW COLUMNS FROM creature_template_resistance").strip().splitlines()]
res_id = "CreatureID" if "CreatureID" in res_cols else "CreatureId"
res_sel = [f"`{res_id}`+{ENTRY_BASE}" if c == res_id else f"`{c}`" for c in res_cols]
L.append(
    f"INSERT INTO `creature_template_resistance` ({','.join('`'+c+'`' for c in res_cols)}) "
    f"SELECT {', '.join(res_sel)} FROM `creature_template_resistance` WHERE `{res_id}` IN ({boss_list});"
)

sp_cols = [ln.split("\t")[0] for ln in q("SHOW COLUMNS FROM creature_template_spell").strip().splitlines()]
sp_id = "CreatureID" if "CreatureID" in sp_cols else "CreatureId"
sp_sel = [f"`{sp_id}`+{ENTRY_BASE}" if c == sp_id else f"`{c}`" for c in sp_cols]
L.append(
    f"INSERT INTO `creature_template_spell` ({','.join('`'+c+'`' for c in sp_cols)}) "
    f"SELECT {', '.join(sp_sel)} FROM `creature_template_spell` WHERE `{sp_id}` IN ({boss_list});"
)
L.append("")

L.append("-- Remap ONLY bosses on map 960 to TW entries; trash stay original")
for oid in boss_oids:
    nid = ENTRY_BASE + oid
    L.append(f"UPDATE `creature` SET `id`={nid} WHERE `map`=960 AND `id`={oid};")
L.append("")

L.append("-- Summary")
for oid in boss_oids:
    t = rows[oid]
    nid = ENTRY_BASE + oid
    hm = boss_hm(t["HealthModifier"])
    L.append(f"-- BOSS {oid} -> {nid} | {t['name']} | L83 HM {t['HealthModifier']}->{hm}")
for oid in trash_oids:
    L.append(f"-- TRASH keep {oid} (original level/HP)")

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(L) + "\n")
print("wrote", OUT, "bytes", os.path.getsize(OUT))
