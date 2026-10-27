# -*- coding: utf-8 -*-
"""Generate TW MC level/HP scale SQL: clone templates for map 960, level 82/83, harder than T7."""
import os, subprocess

MYSQL = r"D:\acore\mysql8.4\bin\mysql.exe"
OUT = r"E:\azerothcore\modules\mod-timewalking\data\sql\db-world\zz_tw_mc_scale_80.sql"
ENTRY_BASE = 9100000  # new_entry = ENTRY_BASE + old_entry

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

def esc(s):
    if s is None or s == "\\N":
        return "NULL"
    return "'" + str(s).replace("\\", "\\\\").replace("'", "\\'") + "'"

def trash_hm(old: float) -> float:
    # Map classic MC trash HM into ~T7 trash band * 1.25
    return max(5.0, round(old / 45.0 * 18.0 * 1.25, 1))

def boss_hm(old: float) -> float:
    # Magmadar 248 -> ~372 (~1.2x T7 Patchwerk 310)
    return round(old * (310.0 / 248.0) * 1.2, 1)

# Distinct ids currently on map 960 (exclude entrance NPCs)
ids_raw = q("SELECT DISTINCT id FROM creature WHERE map=960 AND id NOT IN (9000100,9000101) ORDER BY id")
old_ids = [int(x) for x in ids_raw.split() if x.strip()]
print("ids", len(old_ids), old_ids)

# Load templates
rows = {}
for oid in old_ids:
    line = q(
        "SELECT entry,name,subname,minlevel,maxlevel,`exp`,`rank`,HealthModifier,DamageModifier,"
        "ArmorModifier,ManaModifier,unit_class,AIName,ScriptName,lootid "
        f"FROM creature_template WHERE entry={oid}"
    ).strip()
    if not line:
        raise SystemExit(f"missing template {oid}")
    p = line.split("\t")
    rows[oid] = {
        "entry": int(p[0]), "name": p[1], "subname": None if p[2] == "\\N" else p[2],
        "minlevel": int(p[3]), "maxlevel": int(p[4]), "exp": int(p[5]), "rank": int(p[6]),
        "HealthModifier": float(p[7]), "DamageModifier": float(p[8]),
        "ArmorModifier": float(p[9]), "ManaModifier": float(p[10]),
        "unit_class": int(p[11]), "AIName": p[12], "ScriptName": p[13],
        "lootid": int(p[14]),
    }

L = []
L.append("-- zz_tw_mc_scale_80.sql")
L.append("-- Timewalking MC: clone creature_template for map 960 to level 82/83, harder than T7 (~+20%).")
L.append("-- new_entry = 9100000 + old_entry. Idempotent.")
L.append("SET NAMES utf8mb4;")
L.append("")

new_ids = [ENTRY_BASE + oid for oid in old_ids]
id_list = ",".join(str(x) for x in new_ids)

L.append(f"-- Cleanup previous TW clones")
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

L.append("-- Clone base templates then patch scale fields")
for oid in old_ids:
    nid = ENTRY_BASE + oid
    L.append(
        f"INSERT INTO `creature_template` SELECT * FROM `creature_template` WHERE `entry`={oid};"
    )
    L.append(f"UPDATE `creature_template` SET `entry`={nid} WHERE `entry`={oid} AND `name`=(SELECT `name` FROM (SELECT `name` FROM `creature_template` WHERE `entry`={oid}) x);")
    # Wait - INSERT SELECT then UPDATE entry would create duplicate primary key if we update wrong.
    # Better approach: INSERT with entry rewrite via temp or explicit column list.

# Rewrite properly without the broken update approach
L = L[:L.index("-- Clone base templates then patch scale fields")]
L.append("-- Clone base templates (entry rewritten) then patch scale fields")
L.append("")

# Get full column list
cols = [ln.split("\t")[0] for ln in q("SHOW COLUMNS FROM creature_template").strip().splitlines()]
col_sql = ",".join(f"`{c}`" for c in cols)
print("template cols", len(cols))

for oid in old_ids:
    nid = ENTRY_BASE + oid
    t = rows[oid]
    is_boss = t["rank"] >= 3
    lvl = 83 if is_boss else 82
    hm = boss_hm(t["HealthModifier"]) if is_boss else trash_hm(t["HealthModifier"])
    dm = 42.0 if is_boss else 9.0
    # select expressions
    exprs = []
    for c in cols:
        if c == "entry":
            exprs.append(str(nid))
        elif c == "difficulty_entry_1" or c == "difficulty_entry_2" or c == "difficulty_entry_3":
            exprs.append("0")
        elif c == "minlevel" or c == "maxlevel":
            exprs.append(str(lvl))
        elif c == "exp":
            exprs.append("2")
        elif c == "HealthModifier":
            exprs.append(str(hm))
        elif c == "DamageModifier":
            exprs.append(str(dm))
        elif c == "lootid" or c == "pickpocketloot" or c == "skinloot":
            exprs.append("0")  # 219 loot not ready
        elif c == "mingold" or c == "maxgold":
            exprs.append("0")
        elif c == "name":
            exprs.append(f"CONCAT(`name`,'（时光）')")
        else:
            exprs.append(f"`{c}`")
    L.append(f"INSERT INTO `creature_template` ({col_sql})")
    L.append(f"SELECT {', '.join(exprs)} FROM `creature_template` WHERE `entry`={oid};")

L.append("")
L.append("-- Models")
L.append(f"INSERT INTO `creature_template_model` (`CreatureID`,`Idx`,`CreatureDisplayID`,`DisplayScale`,`Probability`)")
L.append(f"SELECT `CreatureID`+{ENTRY_BASE},`Idx`,`CreatureDisplayID`,`DisplayScale`,`Probability` FROM `creature_template_model` WHERE `CreatureID` IN ({','.join(map(str,old_ids))});")
L.append("")

L.append("-- Locales (zhCN name + 时光)")
L.append(f"INSERT INTO `creature_template_locale` (`entry`,`locale`,`Name`,`Title`,`VerifiedBuild`)")
L.append(f"SELECT `entry`+{ENTRY_BASE},`locale`,CONCAT(`Name`,'（时光）'),`Title`,`VerifiedBuild` FROM `creature_template_locale` WHERE `entry` IN ({','.join(map(str,old_ids))});")
L.append("")

L.append("-- Template addon / equip / movement / resistance / spell")
L.append(f"INSERT INTO `creature_template_addon` SELECT `entry`+{ENTRY_BASE}, `path_id`, `mount`, `bytes1`, `bytes2`, `emote`, `visibilityDistanceType`, `auras` FROM `creature_template_addon` WHERE `entry` IN ({','.join(map(str,old_ids))});")
# equip template columns
eq_cols = [ln.split("\t")[0] for ln in q("SHOW COLUMNS FROM creature_equip_template").strip().splitlines()]
eq_sel = []
for c in eq_cols:
    if c == "CreatureID":
        eq_sel.append(f"`CreatureID`+{ENTRY_BASE}")
    else:
        eq_sel.append(f"`{c}`")
L.append(f"INSERT INTO `creature_equip_template` ({','.join('`'+c+'`' for c in eq_cols)}) SELECT {', '.join(eq_sel)} FROM `creature_equip_template` WHERE `CreatureID` IN ({','.join(map(str,old_ids))});")

mov_cols = [ln.split("\t")[0] for ln in q("SHOW COLUMNS FROM creature_template_movement").strip().splitlines()]
# CreatureId vs CreatureID
mov_id = "CreatureId" if "CreatureId" in mov_cols else "CreatureID"
mov_sel = [f"`{mov_id}`+{ENTRY_BASE}" if c == mov_id else f"`{c}`" for c in mov_cols]
L.append(f"INSERT INTO `creature_template_movement` ({','.join('`'+c+'`' for c in mov_cols)}) SELECT {', '.join(mov_sel)} FROM `creature_template_movement` WHERE `{mov_id}` IN ({','.join(map(str,old_ids))});")

res_cols = [ln.split("\t")[0] for ln in q("SHOW COLUMNS FROM creature_template_resistance").strip().splitlines()]
res_id = "CreatureID" if "CreatureID" in res_cols else "CreatureId"
res_sel = [f"`{res_id}`+{ENTRY_BASE}" if c == res_id else f"`{c}`" for c in res_cols]
L.append(f"INSERT INTO `creature_template_resistance` ({','.join('`'+c+'`' for c in res_cols)}) SELECT {', '.join(res_sel)} FROM `creature_template_resistance` WHERE `{res_id}` IN ({','.join(map(str,old_ids))});")

sp_cols = [ln.split("\t")[0] for ln in q("SHOW COLUMNS FROM creature_template_spell").strip().splitlines()]
sp_id = "CreatureID" if "CreatureID" in sp_cols else "CreatureId"
sp_sel = [f"`{sp_id}`+{ENTRY_BASE}" if c == sp_id else f"`{c}`" for c in sp_cols]
L.append(f"INSERT INTO `creature_template_spell` ({','.join('`'+c+'`' for c in sp_cols)}) SELECT {', '.join(sp_sel)} FROM `creature_template_spell` WHERE `{sp_id}` IN ({','.join(map(str,old_ids))});")
L.append("")

# smart_scripts
ss_cols = [ln.split("\t")[0] for ln in q("SHOW COLUMNS FROM smart_scripts").strip().splitlines()]
ss_sel = []
for c in ss_cols:
    if c == "entryorguid":
        ss_sel.append(f"`entryorguid`+{ENTRY_BASE}")
    else:
        ss_sel.append(f"`{c}`")
L.append("-- SmartAI scripts for trash")
L.append(f"INSERT INTO `smart_scripts` ({','.join('`'+c+'`' for c in ss_cols)})")
L.append(f"SELECT {', '.join(ss_sel)} FROM `smart_scripts` WHERE `source_type`=0 AND `entryorguid` IN ({','.join(map(str,old_ids))});")
L.append("")

L.append("-- Remap map 960 spawns to TW entries")
for oid in old_ids:
    nid = ENTRY_BASE + oid
    L.append(f"UPDATE `creature` SET `id`={nid} WHERE `map`=960 AND `id`={oid};")
L.append("")

L.append("-- Summary comment")
for oid in old_ids:
    t = rows[oid]
    nid = ENTRY_BASE + oid
    is_boss = t["rank"] >= 3
    hm = boss_hm(t["HealthModifier"]) if is_boss else trash_hm(t["HealthModifier"])
    lvl = 83 if is_boss else 82
    L.append(f"-- {oid} -> {nid} | {t['name']} | L{lvl} HM {t['HealthModifier']}->{hm} rank={t['rank']}")

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(L) + "\n")
print("wrote", OUT, "bytes", os.path.getsize(OUT))