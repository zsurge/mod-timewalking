# -*- coding: utf-8 -*-
"""Generate Timewalking MC ilvl-219 loot: T1-look sets, non-set clones, tokens, vendor, ItemSet.dbc."""
import os, struct, subprocess, shutil

MYSQL = r"D:\acore\mysql8.4\bin\mysql.exe"
OUT_SQL = r"E:\azerothcore\modules\mod-timewalking\data\sql\db-world\zz_tw_mc_loot_219.sql"
ITEMSET_DBC = r"E:\acore-server\data\dbc\ItemSet.dbc"
ITEMSET_OUT = r"E:\azerothcore\modules\mod-timewalking\client-patch\DBFilesClient\ItemSet.dbc"
MPQ_BUILDER = r"E:\azerothcore\modules\mod-timewalking\tools\build_tw_dbc_mpq.py"

ITEM_BASE = 9120000          # gear/token: ITEM_BASE + old_entry (tokens use 9129001+)
ITEMSET_BASE = 9200          # 9201..9209 <- 201..209
TOKEN_BASE = 9129000         # 9129001..9129008
EXTCOST_UNUSED = True        # gold vendor for now
BUY_PRICE = 500 * 10000      # 500 gold

TW_BOSSES = [11982, 11988, 12056, 12057, 12098, 12118, 12259, 12264]
T1_SETS = list(range(201, 210))

# InventoryType -> token index 1..8
SLOT_TOKEN = {1:1, 3:2, 5:3, 20:3, 9:4, 10:5, 6:6, 7:7, 8:8}
TOKEN_NAMES_EN = {
    1: "Molten Timewalking Sigil: Head",
    2: "Molten Timewalking Sigil: Shoulder",
    3: "Molten Timewalking Sigil: Chest",
    4: "Molten Timewalking Sigil: Wrist",
    5: "Molten Timewalking Sigil: Hands",
    6: "Molten Timewalking Sigil: Waist",
    7: "Molten Timewalking Sigil: Legs",
    8: "Molten Timewalking Sigil: Feet",
}
TOKEN_NAMES_ZH = {
    1: "\u7194\u706b\u65f6\u5149\u5370\u8bb0\uff1a\u5934\u90e8",
    2: "\u7194\u706b\u65f6\u5149\u5370\u8bb0\uff1a\u80a9\u90e8",
    3: "\u7194\u706b\u65f6\u5149\u5370\u8bb0\uff1a\u80f8\u90e8",
    4: "\u7194\u706b\u65f6\u5149\u5370\u8bb0\uff1a\u624b\u8155",
    5: "\u7194\u706b\u65f6\u5149\u5370\u8bb0\uff1a\u624b\u90e8",
    6: "\u7194\u706b\u65f6\u5149\u5370\u8bb0\uff1a\u8170\u90e8",
    7: "\u7194\u706b\u65f6\u5149\u5370\u8bb0\uff1a\u817f\u90e8",
    8: "\u7194\u706b\u65f6\u5149\u5370\u8bb0\uff1a\u811a\u90e8",
}
TW_SUFFIX = "\uff08\u65f6\u5149\uff09"
SET_NAME_EN = {
    201: "Arcanist Regalia", 202: "Vestments of Prophecy", 203: "Felheart Raiment",
    204: "Nightslayer Armor", 205: "Cenarion Raiment", 206: "Giantstalker Armor",
    207: "The Earthfury", 208: "Lawbringer Armor", 209: "Battlegear of Might",
}
SET_NAME_ZH = {
    201: "\u5965\u672f\u5e08", 202: "\u9884\u8a00", 203: "\u6076\u9b54\u4e4b\u5fc3",
    204: "\u591c\u5e55\u6740\u624b", 205: "\u585e\u7eb3\u91cc\u5965", 206: "\u5de8\u4eba\u8ffd\u730e\u8005",
    207: "\u5927\u5730\u4e4b\u6012", 208: "\u6cd5\u5219\u4f7f\u8005", 209: "\u529b\u91cf",
}

# Overlay fields from 219 donor onto T1 visual base
OVERLAY = [
    "ItemLevel","RequiredLevel","Quality","bonding","armor",
    "stat_type1","stat_value1","stat_type2","stat_value2","stat_type3","stat_value3",
    "stat_type4","stat_value4","stat_type5","stat_value5","stat_type6","stat_value6",
    "stat_type7","stat_value7","stat_type8","stat_value8","stat_type9","stat_value9",
    "stat_type10","stat_value10","StatsCount",
    "socketColor_1","socketContent_1","socketColor_2","socketContent_2",
    "socketColor_3","socketContent_3","socketBonus",
    "dmg_min1","dmg_max1","dmg_type1","dmg_min2","dmg_max2","dmg_type2","delay",
    "RangedModRange","ammo_type",
    "spellid_1","spelltrigger_1","spellcharges_1","spellppmRate_1","spellcooldown_1",
    "spellcategory_1","spellcategorycooldown_1",
    "spellid_2","spelltrigger_2","spellcharges_2","spellppmRate_2","spellcooldown_2",
    "spellcategory_2","spellcategorycooldown_2",
    "spellid_3","spelltrigger_3","spellcharges_3","spellppmRate_3","spellcooldown_3",
    "spellcategory_3","spellcategorycooldown_3",
    "spellid_4","spelltrigger_4","spellcharges_4","spellppmRate_4","spellcooldown_4",
    "spellcategory_4","spellcategorycooldown_4",
    "spellid_5","spelltrigger_5","spellcharges_5","spellppmRate_5","spellcooldown_5",
    "spellcategory_5","spellcategorycooldown_5",
    "holy_res","fire_res","nature_res","frost_res","shadow_res","arcane_res",
    "MaxDurability","DisenchantID","RequiredDisenchantSkill",
    "BuyPrice","SellPrice","Flags","FlagsExtra",
    "holy_res","GemProperties","ScalingStatDistribution","ScalingStatValue",
]

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
    if s is None:
        return "NULL"
    return "'" + str(s).replace("\\", "\\\\").replace("'", "\\'") + "'"

def tw_item(oid):
    return ITEM_BASE + oid

def tw_boss(oid):
    return 9100000 + oid

def tw_set(sid):
    return ITEMSET_BASE + (sid - 200)  # 201->9201

print("loading donors...")
# median-ish donor per (InventoryType, subclass) for armor; also weapons by (class,subclass,InventoryType)
donor = {}
rows = q(
    "SELECT InventoryType, subclass, entry FROM ("
    " SELECT InventoryType, subclass, entry,"
    " ROW_NUMBER() OVER (PARTITION BY InventoryType, subclass ORDER BY entry) rn,"
    " COUNT(*) OVER (PARTITION BY InventoryType, subclass) cnt"
    " FROM item_template WHERE ItemLevel=219 AND Quality=4 AND class=4 AND bonding IN (1,2)"
    ") t WHERE rn = FLOOR((cnt+1)/2)"
).strip().splitlines()
for line in rows:
    inv, sub, entry = line.split("\t")
    donor[("armor", int(inv), int(sub))] = int(entry)

rows = q(
    "SELECT InventoryType, class, subclass, entry FROM ("
    " SELECT InventoryType, class, subclass, entry,"
    " ROW_NUMBER() OVER (PARTITION BY InventoryType, class, subclass ORDER BY entry) rn,"
    " COUNT(*) OVER (PARTITION BY InventoryType, class, subclass) cnt"
    " FROM item_template WHERE ItemLevel=219 AND Quality=4 AND class IN (2,4) AND bonding IN (1,2)"
    ") t WHERE rn = FLOOR((cnt+1)/2)"
).strip().splitlines()
for line in rows:
    inv, cls, sub, entry = line.split("\t")
    donor[("any", int(inv), int(cls), int(sub))] = int(entry)

def pick_donor(inv, cls, sub):
    if cls == 4 and ("armor", inv, sub) in donor:
        return donor[("armor", inv, sub)]
    # chest robe inv 20 -> try 5
    if inv == 20 and ("armor", 5, sub) in donor:
        return donor[("armor", 5, sub)]
    if inv == 5 and ("armor", 20, sub) in donor:
        return donor[("armor", 20, sub)]
    if ("any", inv, cls, sub) in donor:
        return donor[("any", inv, cls, sub)]
    # fallback any 219 epic same inv
    r = q(f"SELECT entry FROM item_template WHERE ItemLevel=219 AND Quality=4 AND InventoryType={inv} LIMIT 1").strip()
    if not r:
        r = q("SELECT entry FROM item_template WHERE ItemLevel=219 AND Quality=4 LIMIT 1").strip()
    return int(r.splitlines()[0])

cols = [ln.split("\t")[0] for ln in q("SHOW COLUMNS FROM item_template").strip().splitlines()]
print("item_template cols", len(cols))

# T1 set pieces
t1_pieces = []
for line in q(
    "SELECT entry, name, InventoryType, class, subclass, itemset FROM item_template "
    "WHERE itemset BETWEEN 201 AND 209 ORDER BY itemset, InventoryType"
).strip().splitlines():
    e, name, inv, cls, sub, iset = line.split("\t")
    t1_pieces.append({
        "entry": int(e), "name": name, "InventoryType": int(inv),
        "class": int(cls), "subclass": int(sub), "itemset": int(iset),
    })
print("T1 pieces", len(t1_pieces))

# Non-set MC loot items from boss refs
nons = set()
set_entries = {p["entry"] for p in t1_pieces}
for boss in TW_BOSSES:
    refs = q(f"SELECT Reference FROM creature_loot_template WHERE Entry={boss} AND Reference>0").split()
    for ref in refs:
        if int(ref) == 30001:
            continue  # recipes skip
        for line in q(
            f"SELECT Item FROM reference_loot_template WHERE Entry={int(ref)} AND Reference=0"
        ).split():
            it = int(line)
            if it not in set_entries:
                nons.add(it)
nons = sorted(nons)
print("non-set candidates", len(nons), nons[:10], "...")

# Validate items exist
ok_nons = []
for it in nons:
    if q(f"SELECT entry FROM item_template WHERE entry={it}").strip():
        ok_nons.append(it)
nons = ok_nons
print("non-set ok", len(nons))

L = []
L.append("-- zz_tw_mc_loot_219.sql")
L.append("-- Timewalking MC: ilvl 219 set (T1 look) + non-set + tokens + gold vendor + boss loot")
L.append("SET NAMES utf8mb4;")
L.append("")

all_new_items = [tw_item(p["entry"]) for p in t1_pieces] + [tw_item(i) for i in nons] + [TOKEN_BASE + i for i in range(1, 9)]
id_list = ",".join(str(x) for x in all_new_items)

L.append("-- Cleanup previous TW loot items / loot / vendor rows")
L.append(f"DELETE FROM `npc_vendor` WHERE `entry`=9000101;")
L.append(f"DELETE FROM `creature_loot_template` WHERE `Entry` IN ({','.join(str(tw_boss(b)) for b in TW_BOSSES)});")
# reference entries we may create
L.append(f"DELETE FROM `reference_loot_template` WHERE `Entry` BETWEEN 9130000 AND 9139999;")
L.append(f"DELETE FROM `item_template_locale` WHERE `ID` IN ({id_list});")
L.append(f"DELETE FROM `item_template` WHERE `entry` IN ({id_list});")
L.append(f"DELETE FROM `itemset_dbc` WHERE `ID` BETWEEN 9201 AND 9209;")
L.append("")

# ---- tokens ----
L.append("-- Slot tokens (exchange later; still drop now)")
for i in range(1, 9):
    tid = TOKEN_BASE + i
    # clone a simple token-like item: Badge of Justice 29434 as base junk epic? use 47241 or 49426 - emblem
    # Use 34622 as scrap or create from 29434
    base_tok = 29434
    exprs = []
    for c in cols:
        if c == "entry":
            exprs.append(str(tid))
        elif c == "name":
            exprs.append(esc(TOKEN_NAMES_EN[i]))
        elif c == "displayid":
            exprs.append("56857")  # emblem-like; fallback keep base
        elif c == "Quality":
            exprs.append("4")
        elif c == "bonding":
            exprs.append("1")
        elif c == "ItemLevel":
            exprs.append("219")
        elif c == "RequiredLevel":
            exprs.append("80")
        elif c == "class":
            exprs.append("15")  # miscellaneous
        elif c == "subclass":
            exprs.append("4")  # other
        elif c == "InventoryType":
            exprs.append("0")
        elif c == "stackable":
            exprs.append("20")
        elif c == "maxcount":
            exprs.append("0")
        elif c == "BuyPrice":
            exprs.append("0")
        elif c == "SellPrice":
            exprs.append("0")
        elif c == "Flags":
            exprs.append("0")
        elif c.startswith("stat_") or c.startswith("dmg_") or c.startswith("spell") or c.startswith("socket"):
            exprs.append("0")
        elif c in ("armor","delay","holy_res","fire_res","nature_res","frost_res","shadow_res","arcane_res"):
            exprs.append("0")
        elif c == "description":
            exprs.append(esc("Turn in later at the Timewalking set vendor."))
        else:
            exprs.append(f"`{c}`")
    L.append(f"INSERT INTO `item_template` ({','.join('`'+c+'`' for c in cols)})")
    L.append(f"SELECT {', '.join(exprs)} FROM `item_template` WHERE `entry`={base_tok};")
    L.append(
        f"INSERT INTO `item_template_locale` (`ID`,`locale`,`Name`,`Description`,`VerifiedBuild`) VALUES "
        f"({tid},'zhCN',{esc(TOKEN_NAMES_ZH[i])},{esc('\u5728\u8fbe\u62c9\u7136\u65f6\u5149\u5957\u88c5\u5151\u6362\u5458\u5904\u5151\u6362\uff08\u6682\u672a\u5f00\u653e\uff09')},18019);"
    )
L.append("")

# ---- set pieces ----
L.append("-- T1-look set pieces at 219")
set_items = {sid: [] for sid in T1_SETS}
for p in t1_pieces:
    oid = p["entry"]
    nid = tw_item(oid)
    d = pick_donor(p["InventoryType"], p["class"], p["subclass"])
    new_set = tw_set(p["itemset"])
    set_items[p["itemset"]].append(nid)
    exprs = []
    for c in cols:
        if c == "entry":
            exprs.append(str(nid))
        elif c == "name":
            exprs.append(f"CONCAT(`name`, {esc(TW_SUFFIX)})")
        elif c == "itemset":
            exprs.append(str(new_set))
        elif c == "displayid":
            exprs.append("`displayid`")  # from T1 (base row)
        elif c in OVERLAY or c in ("ItemLevel","RequiredLevel","Quality","bonding"):
            # take from donor via subquery later - use join style: select from t1 with overlays from donor
            exprs.append(f"d.`{c}`")
        elif c == "AllowableClass":
            exprs.append("t.`AllowableClass`")
        elif c == "AllowableRace":
            exprs.append("t.`AllowableRace`")
        elif c in ("class","subclass","InventoryType","Material","sheath","SoundOverrideSubclass"):
            exprs.append(f"t.`{c}`")
        else:
            exprs.append(f"t.`{c}`")
    # Fix: base FROM t1 AS t, donor AS d
    # Rebuild cleaner
    exprs = []
    for c in cols:
        if c == "entry":
            exprs.append(str(nid))
        elif c == "name":
            exprs.append(f"CONCAT(t.`name`, {esc(TW_SUFFIX)})")
        elif c == "itemset":
            exprs.append(str(new_set))
        elif c == "displayid":
            exprs.append("t.`displayid`")
        elif c in ("class","subclass","InventoryType","AllowableClass","AllowableRace","Material","sheath",
                   "SoundOverrideSubclass","TotemCategory","RequiredSpell","area","Map","BagFamily",
                   "itemset"):  # itemset already handled
            if c == "itemset":
                exprs.append(str(new_set))
            else:
                exprs.append(f"t.`{c}`")
        elif c in OVERLAY:
            exprs.append(f"d.`{c}`")
        else:
            # default prefer T1 visual/meta, but level-ish from donor already in OVERLAY
            exprs.append(f"t.`{c}`")
    # Force required fields
    # Replace ItemLevel etc already in OVERLAY from donor
    L.append(f"INSERT INTO `item_template` ({','.join('`'+c+'`' for c in cols)})")
    L.append(
        f"SELECT {', '.join(exprs)} FROM `item_template` t "
        f"JOIN `item_template` d ON d.`entry`={d} WHERE t.`entry`={oid};"
    )
    # locale
    L.append(
        f"INSERT INTO `item_template_locale` (`ID`,`locale`,`Name`,`Description`,`VerifiedBuild`) "
        f"SELECT {nid},`locale`,CONCAT(`Name`,{esc(TW_SUFFIX)}),`Description`,`VerifiedBuild` "
        f"FROM `item_template_locale` WHERE `ID`={oid};"
    )

L.append("")
L.append("-- Non-set 219 clones of classic MC epics")
for oid in nons:
    nid = tw_item(oid)
    meta = q(f"SELECT InventoryType, class, subclass FROM item_template WHERE entry={oid}").strip().split("\t")
    if len(meta) < 3:
        continue
    inv, cls, sub = map(int, meta)
    d = pick_donor(inv, cls, sub)
    exprs = []
    for c in cols:
        if c == "entry":
            exprs.append(str(nid))
        elif c == "name":
            exprs.append(f"CONCAT(t.`name`, {esc(TW_SUFFIX)})")
        elif c == "itemset":
            exprs.append("0")
        elif c == "displayid":
            exprs.append("t.`displayid`")
        elif c in ("class","subclass","InventoryType","AllowableClass","AllowableRace","Material","sheath",
                   "SoundOverrideSubclass","TotemCategory"):
            exprs.append(f"t.`{c}`")
        elif c in OVERLAY:
            exprs.append(f"d.`{c}`")
        else:
            exprs.append(f"t.`{c}`")
    L.append(f"INSERT INTO `item_template` ({','.join('`'+c+'`' for c in cols)})")
    L.append(
        f"SELECT {', '.join(exprs)} FROM `item_template` t "
        f"JOIN `item_template` d ON d.`entry`={d} WHERE t.`entry`={oid};"
    )
    L.append(
        f"INSERT INTO `item_template_locale` (`ID`,`locale`,`Name`,`Description`,`VerifiedBuild`) "
        f"SELECT {nid},`locale`,CONCAT(`Name`,{esc(TW_SUFFIX)}),`Description`,`VerifiedBuild` "
        f"FROM `item_template_locale` WHERE `ID`={oid};"
    )

L.append("")
# Force ItemLevel/Req/bonding on all TW gear (donor should already, belt-and-suspenders)
L.append(
    f"UPDATE `item_template` SET `ItemLevel`=219, `RequiredLevel`=80, `bonding`=1, `Quality`=4 "
    f"WHERE `entry` IN ({','.join(str(tw_item(p['entry'])) for p in t1_pieces)},"
    f"{','.join(str(tw_item(i)) for i in nons)});"
)
L.append("")
L.append("-- Prefer zhCN as item_template.name so set tooltips are Chinese")
L.append(
    "UPDATE `item_template` it "
    "INNER JOIN `item_template_locale` itl ON itl.`ID`=it.`entry` AND itl.`locale`='zhCN' "
    "SET it.`name`=itl.`Name` "
    "WHERE it.`itemset` BETWEEN 9201 AND 9209;"
)
L.append("")

# ---- itemset_dbc rows (server) ----
L.append("-- itemset_dbc (server). Client ItemSet.dbc written by this script separately.")
for sid in T1_SETS:
    ns = tw_set(sid)
    items = set_items[sid] + [0] * 16
    items = items[:17]
    en = SET_NAME_EN[sid] + " (Timewalking)"
    zh = SET_NAME_ZH[sid] + "\u65f6\u5149"
    # copy spells from DBC via later Python; for SQL use zeros first then script fills DBC
    L.append(
        f"INSERT INTO `itemset_dbc` (`ID`,`Name_Lang_enUS`,`Name_Lang_zhCN`,`Name_Lang_Mask`,"
        + ",".join(f"`ItemID_{i}`" for i in range(1, 18)) + ","
        + ",".join(f"`SetSpellID_{i}`" for i in range(1, 9)) + ","
        + ",".join(f"`SetThreshold_{i}`" for i in range(1, 9)) + ","
        "`RequiredSkill`,`RequiredSkillRank`) VALUES ("
        f"{ns},{esc(en)},{esc(zh)},16712190,"
        + ",".join(str(x) for x in items) + ","
        + "0,0,0,0,0,0,0,0,"
        + "0,0,0,0,0,0,0,0,"
        + "0,0);"
    )
L.append("")

# ---- loot tables ----
L.append("-- Boss loot: mirror classic refs -> token group + non-set group")
ref_id = 9130001
boss_ref_map = {}  # boss -> list of new ref ids

for boss in TW_BOSSES:
    tb = tw_boss(boss)
    refs = [int(x) for x in q(f"SELECT Reference FROM creature_loot_template WHERE Entry={boss} AND Reference>0").split()]
    L.append(f"-- boss {boss} -> {tb}")
    L.append(f"UPDATE `creature_template` SET `lootid`={tb} WHERE `entry`={tb};")
    new_refs = []
    for ref in refs:
        if ref == 30001:
            continue
        items = []
        for line in q(f"SELECT Item, Chance, GroupId, MinCount, MaxCount FROM reference_loot_template WHERE Entry={ref} AND Reference=0").strip().splitlines():
            if not line.strip():
                continue
            p = line.split("\t")
            items.append({"Item": int(p[0]), "Chance": float(p[1]), "GroupId": int(p[2]), "MinCount": int(p[3]), "MaxCount": int(p[4])})
        if not items:
            continue
        # Classify: if any T1 set piece -> emit TOKEN group for those slots; else non-set clones
        token_slots = set()
        nons_here = []
        for it in items:
            if it["Item"] in set_entries:
                inv = int(q(f"SELECT InventoryType FROM item_template WHERE entry={it['Item']}").strip() or "0")
                if inv in SLOT_TOKEN:
                    token_slots.add(SLOT_TOKEN[inv])
            else:
                if it["Item"] in nons:
                    nons_here.append(it)
        nref = ref_id
        ref_id += 1
        new_refs.append(nref)
        if token_slots:
            # equal chance tokens (GroupId=1, Chance=0)
            for slot in sorted(token_slots):
                tid = TOKEN_BASE + slot
                L.append(
                    f"INSERT INTO `reference_loot_template` (`Entry`,`Item`,`Reference`,`Chance`,`QuestRequired`,`LootMode`,`GroupId`,`MinCount`,`MaxCount`,`Comment`) VALUES "
                    f"({nref},{tid},0,0,0,1,1,1,1,{esc('TW token slot '+str(slot))});"
                )
            # also include non-set from same ref into group 2
            for it in nons_here:
                L.append(
                    f"INSERT INTO `reference_loot_template` (`Entry`,`Item`,`Reference`,`Chance`,`QuestRequired`,`LootMode`,`GroupId`,`MinCount`,`MaxCount`,`Comment`) VALUES "
                    f"({nref},{tw_item(it['Item'])},0,0,0,1,2,1,1,{esc('TW non-set')});"
                )
        else:
            for it in nons_here:
                L.append(
                    f"INSERT INTO `reference_loot_template` (`Entry`,`Item`,`Reference`,`Chance`,`QuestRequired`,`LootMode`,`GroupId`,`MinCount`,`MaxCount`,`Comment`) VALUES "
                    f"({nref},{tw_item(it['Item'])},0,0,0,1,1,1,1,{esc('TW non-set')});"
                )
        L.append(
            f"INSERT INTO `creature_loot_template` (`Entry`,`Item`,`Reference`,`Chance`,`QuestRequired`,`LootMode`,`GroupId`,`MinCount`,`MaxCount`,`Comment`) VALUES "
            f"({tb},{nref},{nref},100,0,1,0,1,1,{esc('TW ref '+str(ref))});"
        )
    # light gold via mingold already on template
L.append("")

# ---- vendor gold ----
L.append("-- Set vendor 9000101: sell all TW set pieces for gold (token exchange later)")
L.append("UPDATE `creature_template` SET `npcflag`=`npcflag`|128 WHERE `entry`=9000101;")
slot = 0
for p in t1_pieces:
    nid = tw_item(p["entry"])
    # set BuyPrice on item already from donor; force vendor price
    L.append(f"UPDATE `item_template` SET `BuyPrice`={BUY_PRICE}, `SellPrice`={BUY_PRICE//4} WHERE `entry`={nid};")
    L.append(
        f"INSERT INTO `npc_vendor` (`entry`,`slot`,`item`,`maxcount`,`incrtime`,`ExtendedCost`,`VerifiedBuild`) VALUES "
        f"(9000101,{slot},{nid},0,0,0,0);"
    )
    slot += 1
L.append("")

os.makedirs(os.path.dirname(OUT_SQL), exist_ok=True)
with open(OUT_SQL, "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(L) + "\n")
print("wrote", OUT_SQL, "bytes", os.path.getsize(OUT_SQL))

# ---- ItemSet.dbc append ----
print("patching ItemSet.dbc...")
with open(ITEMSET_DBC, "rb") as f:
    data = bytearray(f.read())
magic, records, fields, recsize, strsize = struct.unpack_from("<4sIIII", data, 0)
assert magic == b"WDBC" and fields == 53 and recsize == 212
sb_off = 20 + records * recsize
string_block = bytearray(data[sb_off:sb_off + strsize])
records_data = bytearray(data[20:sb_off])

# index existing spells for T1 sets from DBC
def read_row(i):
    return list(struct.unpack_from("<" + "i" * fields, records_data, i * recsize))

id_to_row = {}
for i in range(records):
    row = read_row(i)
    id_to_row[row[0]] = row

def add_string(s: str) -> int:
    b = s.encode("utf-8") + b"\x00"
    # reuse if exists
    idx = string_block.find(b)
    if idx >= 0:
        return idx
    off = len(string_block)
    string_block.extend(b)
    return off

new_rows = []
for sid in T1_SETS:
    src = id_to_row[sid]
    ns = tw_set(sid)
    row = list(src)
    row[0] = ns
    en = SET_NAME_EN[sid] + " (Timewalking)"
    zh = SET_NAME_ZH[sid] + "\u65f6\u5149"
    en_off = add_string(en)
    zh_off = add_string(zh)
    # clear all name offsets then set enUS(1) and zhCN(7) — field index: 0=ID, 1=enUS ... 7=zhCN (0-based in row)
    for j in range(1, 17):
        row[j] = 0
    row[1] = en_off  # enUS
    row[7] = zh_off  # zhCN
    row[17] = 16712190  # mask
    items = set_items[sid] + [0] * 17
    for j in range(17):
        row[18 + j] = items[j]
    # keep spells/thresholds from T1 (same bonuses)
    new_rows.append(row)

for row in new_rows:
    records_data.extend(struct.pack("<" + "i" * fields, *row))
records += len(new_rows)
strsize = len(string_block)
out = bytearray()
out.extend(struct.pack("<4sIIII", b"WDBC", records, fields, recsize, strsize))
out.extend(records_data)
out.extend(string_block)
os.makedirs(os.path.dirname(ITEMSET_OUT), exist_ok=True)
with open(ITEMSET_OUT, "wb") as f:
    f.write(out)
# also install to server dbc
shutil.copy2(ITEMSET_OUT, ITEMSET_DBC)
print("ItemSet.dbc records", records, "->", ITEMSET_OUT)

# rebuild MPQ including ItemSet.dbc
print("rebuilding client MPQ...")
# patch build script files dict by running inline
import importlib.util
spec = importlib.util.spec_from_file_location("build_tw", MPQ_BUILDER)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
base = r"E:\azerothcore\modules\mod-timewalking\client-patch\DBFilesClient"
files = {
    r"DBFilesClient\Map.dbc": open(os.path.join(base, "Map.dbc"), "rb").read(),
    r"DBFilesClient\MapDifficulty.dbc": open(os.path.join(base, "MapDifficulty.dbc"), "rb").read(),
    r"DBFilesClient\ItemSet.dbc": open(os.path.join(base, "ItemSet.dbc"), "rb").read(),
}
out_mpq = r"E:\azerothcore\modules\mod-timewalking\client-patch\patch-zhCN-TW.MPQ"
mod.build_mpq(files, out_mpq)
for dest in (
    r"F:\World of Warcraft Dev\Data\zhCN\patch-zhCN-9.MPQ",
    r"F:\claw-code\Lwow\Data\zhCN\patch-zhCN-9.MPQ",
):
    ddir = os.path.dirname(dest)
    if os.path.isdir(ddir):
        shutil.copy2(out_mpq, dest)
        print("installed", dest)

print("DONE")
