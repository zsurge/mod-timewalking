# -*- coding: utf-8 -*-
"""Regenerate Dalaran TW NPC + utility GO SQL and import into acore_world:3308.

NPCs (creature):
  9000100 / guid 5300800  时光副本 portal
  9000101 / guid 5300801  时光套装兑换 vendor
  9000102 / guid 5300802  拍卖师 (neutral, Alliance+Horde)

Gameobjects:
  entry 191757 / guid 5300810  DK Runeforge (type 8, spellfocus 1552)
  entry 193086 / guid 5300811  Guild Vault (type 34, Dalaran model)
  entry 193071 / guid 5300812  Mailbox (type 19, Dalaran model)
"""
import math
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SQL_NPC = ROOT / "data" / "sql" / "db-world" / "zz_tw_dalaran_entrance_npcs.sql"
SQL_GO = ROOT / "data" / "sql" / "db-world" / "zz_tw_dalaran_utility_gos.sql"
MYSQL = [r"D:\acore\mysql8.4\bin\mysql.exe", "--host=127.0.0.1", "--port=3308",
         "-usurge", "-pacer@1123", "--default-character-set=utf8mb4", "acore_world"]

bq = chr(96)

def qi(name):
    return bq + name + bq

def rot(o):
    return (0.0, 0.0, math.sin(o / 2.0), math.cos(o / 2.0))

PORTAL_XYZO = (5794.0737, 429.3953, 658.7858, 0.7693)
VENDOR_XYZO = (5791.0757, 433.6151, 658.7834, 0.565)
AUCTION_XYZO = (5839.514, 439.50998, 658.7835, 2.7588007)
RUNEFORGE_XYZO = (5778.2334, 447.9638, 657.5751, 3.2261343)
GUILD_XYZO = (5780.4478, 434.46454, 657.55396, 0.44580877)
MAIL_XYZO = (5821.194, 414.4446, 657.58844, 1.6788778)

def build_npc_sql():
    L = []
    a = L.append
    a("-- zz_tw_dalaran_entrance_npcs.sql")
    a("-- Dalaran Timewalking entrance + set vendor + neutral auctioneer (Krasus Landing)")
    a("-- Idempotent. Coordinates synced to live placement (2026-10-27).")
    a("SET NAMES utf8mb4;")
    a("")
    a("SET @ENTRY_PORTAL := 9000100;")
    a("SET @ENTRY_VENDOR := 9000101;")
    a("SET @ENTRY_AUCTION := 9000102;")
    a("SET @GUID_PORTAL  := 5300800;")
    a("SET @GUID_VENDOR  := 5300801;")
    a("SET @GUID_AUCTION := 5300802;")
    a("SET @MENU_PORTAL  := 960100;")
    a("SET @MENU_VENDOR  := 960101;")
    a("SET @MODEL_PORTAL := 28127;")
    a("SET @MODEL_VENDOR := 25907;")
    a("SET @MODEL_AUCTION := 7993;")
    a("")
    a("DELETE FROM " + qi("creature_template") + " WHERE " + qi("entry") + " IN (@ENTRY_PORTAL, @ENTRY_VENDOR, @ENTRY_AUCTION);")
    a("INSERT INTO " + qi("creature_template"))
    a("(" + ", ".join(qi(c) for c in [
        "entry", "name", "subname", "IconName", "gossip_menu_id", "minlevel", "maxlevel",
        "faction", "npcflag", "unit_class", "unit_flags", "type", "flags_extra", "ScriptName", "AIName"]) + ")")
    a("VALUES")
    a("(@ENTRY_PORTAL, '时光副本', '熔火之心（时光）', 'Speak', @MENU_PORTAL, 80, 80, 35, 1, 1, 2, 7, 2, '', 'SmartAI'),")
    a("(@ENTRY_VENDOR, '时光套装兑换', '', 'Speak', @MENU_VENDOR, 80, 80, 35, 129, 1, 2, 7, 2, '', ''),")
    a("(@ENTRY_AUCTION, '拍卖师', '联盟/部落可用', 'Speak', 0, 80, 80, 35, 2097154, 1, 2, 7, 2, '', '');")
    a("")
    a("DELETE FROM " + qi("creature_template_model") + " WHERE " + qi("CreatureID") + " IN (@ENTRY_PORTAL, @ENTRY_VENDOR, @ENTRY_AUCTION);")
    a("INSERT INTO " + qi("creature_template_model") + " (" + ", ".join(qi(c) for c in ["CreatureID", "Idx", "CreatureDisplayID", "DisplayScale", "Probability"]) + ") VALUES")
    a("(@ENTRY_PORTAL, 0, @MODEL_PORTAL, 1, 1),")
    a("(@ENTRY_VENDOR, 0, @MODEL_VENDOR, 1, 1),")
    a("(@ENTRY_AUCTION, 0, @MODEL_AUCTION, 1, 1);")
    a("")
    a("DELETE FROM " + qi("creature_template_locale") + " WHERE " + qi("entry") + " IN (@ENTRY_PORTAL, @ENTRY_VENDOR, @ENTRY_AUCTION) AND " + qi("locale") + "='zhCN';")
    a("INSERT INTO " + qi("creature_template_locale") + " (" + ", ".join(qi(c) for c in ["entry", "locale", "Name", "Title", "VerifiedBuild"]) + ") VALUES")
    a("(@ENTRY_PORTAL, 'zhCN', '时光副本', '熔火之心（时光）', 0),")
    a("(@ENTRY_VENDOR, 'zhCN', '时光套装兑换', '', 0),")
    a("(@ENTRY_AUCTION, 'zhCN', '拍卖师', '联盟/部落可用', 0);")
    a("")
    a("DELETE FROM " + qi("gossip_menu") + " WHERE " + qi("MenuID") + " IN (@MENU_PORTAL, @MENU_VENDOR);")
    a("INSERT INTO " + qi("gossip_menu") + " (" + ", ".join(qi(c) for c in ["MenuID", "TextID"]) + ") VALUES")
    a("(@MENU_PORTAL, 1),")
    a("(@MENU_VENDOR, 1);")
    a("")
    a("DELETE FROM " + qi("gossip_menu_option") + " WHERE " + qi("MenuID") + " IN (@MENU_PORTAL, @MENU_VENDOR);")
    a("INSERT INTO " + qi("gossip_menu_option"))
    a("(" + ", ".join(qi(c) for c in [
        "MenuID", "OptionID", "OptionIcon", "OptionText", "OptionBroadcastTextID",
        "OptionType", "OptionNpcFlag", "ActionMenuID", "ActionPoiID", "BoxCoded", "BoxMoney", "BoxText", "BoxBroadcastTextID"]) + ")")
    a("VALUES")
    a("(@MENU_PORTAL, 0, 0, '进入熔火之心（时光）', 0, 1, 1, 0, 0, 0, 0, NULL, 0),")
    a("(@MENU_PORTAL, 1, 0, '了解时光副本的说明', 0, 1, 1, 0, 0, 0, 0, NULL, 0),")
    a("(@MENU_VENDOR, 0, 1, '购买时光套装', 0, 3, 1, 0, 0, 0, 0, NULL, 0);")
    a("")
    a("DELETE FROM " + qi("creature_text") + " WHERE " + qi("CreatureID") + " IN (@ENTRY_PORTAL, @ENTRY_VENDOR, @ENTRY_AUCTION);")
    a("INSERT INTO " + qi("creature_text") + " (" + ", ".join(qi(c) for c in [
        "CreatureID", "GroupID", "ID", "Text", "Type", "Language",
        "Probability", "Emote", "Duration", "Sound", "BroadcastTextId", "TextRange", "comment"]) + ") VALUES")
    a("(@ENTRY_PORTAL, 0, 0, '时光熔火之心：10 人副本，装备目标 219。击败 Boss 可掉落 219 散件与熔火时光印记。', 12, 0, 100, 1, 0, 0, 0, 0, 'TW portal help');")
    a("")
    a("DELETE FROM " + qi("smart_scripts") + " WHERE " + qi("entryorguid") + " IN (@ENTRY_PORTAL, @ENTRY_VENDOR, @ENTRY_AUCTION) AND " + qi("source_type") + "=0;")
    a("INSERT INTO " + qi("smart_scripts"))
    a("(" + ",".join(qi(c) for c in [
        "entryorguid", "source_type", "id", "link", "event_type", "event_phase_mask", "event_chance", "event_flags",
        "event_param1", "event_param2", "event_param3", "event_param4", "event_param5", "event_param6",
        "action_type", "action_param1", "action_param2", "action_param3", "action_param4", "action_param5", "action_param6",
        "target_type", "target_param1", "target_param2", "target_param3", "target_param4",
        "target_x", "target_y", "target_z", "target_o", "comment"]) + ")")
    a("VALUES")
    a("(@ENTRY_PORTAL,0,0,1,62,0,100,0,@MENU_PORTAL,0,0,0,0,0,62,960,0,0,0,0,0,7,0,0,0,0,1091.89,-466.985,-105.084,3.14159,'TW Portal - Enter TW MC'),")
    a("(@ENTRY_PORTAL,0,1,0,61,0,100,0,0,0,0,0,0,0,72,0,0,0,0,0,0,7,0,0,0,0,0,0,0,0,'TW Portal - Close'),")
    a("(@ENTRY_PORTAL,0,2,3,62,0,100,0,@MENU_PORTAL,1,0,0,0,0,1,0,0,0,0,0,0,7,0,0,0,0,0,0,0,0,'TW Portal - Help text'),")
    a("(@ENTRY_PORTAL,0,3,0,61,0,100,0,0,0,0,0,0,0,72,0,0,0,0,0,0,7,0,0,0,0,0,0,0,0,'TW Portal - Close help');")
    a("")
    a("DELETE FROM " + qi("creature") + " WHERE " + qi("guid") + " IN (@GUID_PORTAL, @GUID_VENDOR, @GUID_AUCTION) OR " + qi("id") + " IN (@ENTRY_PORTAL, @ENTRY_VENDOR, @ENTRY_AUCTION);")
    a("INSERT INTO " + qi("creature"))
    a("(" + ",".join(qi(c) for c in [
        "guid", "id", "map", "zoneId", "areaId", "spawnMask", "phaseMask", "equipment_id",
        "position_x", "position_y", "position_z", "orientation", "spawntimesecs", "wander_distance",
        "currentwaypoint", "curhealth", "curmana", "MovementType"]) + ")")
    a("VALUES")
    px, py, pz, po = PORTAL_XYZO
    vx, vy, vz, vo = VENDOR_XYZO
    ax, ay, az, ao = AUCTION_XYZO
    a(f"(@GUID_PORTAL,@ENTRY_PORTAL,571,4395,4564,1,1,0,{px},{py},{pz},{po},300,0,0,1,0,0),")
    a(f"(@GUID_VENDOR,@ENTRY_VENDOR,571,4395,4564,1,1,0,{vx},{vy},{vz},{vo},300,0,0,1,0,0),")
    a(f"(@GUID_AUCTION,@ENTRY_AUCTION,571,4395,4564,1,1,0,{ax},{ay},{az},{ao},300,0,0,1,0,0);")
    a("")
    return "\n".join(L)

def build_go_sql():
    L = []
    a = L.append
    a("-- zz_tw_dalaran_utility_gos.sql")
    a("-- Dalaran Krasus Landing utility gameobjects: DK Runeforge, Guild Vault, Mailbox")
    a("-- Idempotent. Stock WotLK entries.")
    a("SET NAMES utf8mb4;")
    a("")
    a("SET @GUID_RUNE  := 5300810;")
    a("SET @GUID_GUILD := 5300811;")
    a("SET @GUID_MAIL  := 5300812;")
    a("SET @ENTRY_RUNE  := 191757;  -- Runeforge type=8 spellfocus 1552")
    a("SET @ENTRY_GUILD := 193086;  -- Guild Vault type=34")
    a("SET @ENTRY_MAIL  := 193071;  -- Mailbox type=19")
    a("")
    a("DELETE FROM " + qi("gameobject") + " WHERE " + qi("guid") + " IN (@GUID_RUNE, @GUID_GUILD, @GUID_MAIL);")
    a("INSERT INTO " + qi("gameobject"))
    a("(" + ",".join(qi(c) for c in [
        "guid", "id", "map", "zoneId", "areaId", "spawnMask", "phaseMask",
        "position_x", "position_y", "position_z", "orientation",
        "rotation0", "rotation1", "rotation2", "rotation3",
        "spawntimesecs", "animprogress", "state"]) + ")")
    a("VALUES")
    rows = []
    for guid, entry, xyzo, anim, state in [
        ("@GUID_RUNE", "@ENTRY_RUNE", RUNEFORGE_XYZO, 100, 1),
        ("@GUID_GUILD", "@ENTRY_GUILD", GUILD_XYZO, 100, 1),
        ("@GUID_MAIL", "@ENTRY_MAIL", MAIL_XYZO, 255, 1),
    ]:
        x, y, z, o = xyzo
        r0, r1, r2, r3 = rot(o)
        rows.append(f"({guid},{entry},571,4395,4564,1,1,{x},{y},{z},{o},{r0:.6f},{r1:.6f},{r2:.6f},{r3:.6f},300,{anim},{state})")
    a(",\n".join(rows) + ";")
    a("")
    return "\n".join(L)

def mysql_exec(sql_text):
    r = subprocess.run(MYSQL, input=sql_text.encode("utf-8"), capture_output=True)
    print("mysql", r.returncode)
    if r.stderr:
        print(r.stderr.decode("utf-8", "replace"))
    return r.returncode

def main():
    npc = build_npc_sql()
    go = build_go_sql()
    SQL_NPC.write_text(npc, encoding="utf-8", newline="\n")
    SQL_GO.write_text(go, encoding="utf-8", newline="\n")
    print("wrote", SQL_NPC, len(npc))
    print("wrote", SQL_GO, len(go))
    rc1 = mysql_exec(npc)
    rc2 = mysql_exec(go)
    r = subprocess.run(MYSQL[:-1] + ["-N", MYSQL[-1], "-e",
        "SELECT entry,name,subname,faction,npcflag FROM creature_template WHERE entry IN (9000100,9000101,9000102);"
        "SELECT guid,id,ROUND(position_x,2),ROUND(position_y,2),ROUND(position_z,2),ROUND(orientation,3) FROM creature WHERE guid IN (5300800,5300801,5300802);"
        "SELECT g.guid,g.id,t.name,t.type,ROUND(g.position_x,2),ROUND(g.position_y,2),ROUND(g.position_z,2) "
        "FROM gameobject g JOIN gameobject_template t ON g.id=t.entry WHERE g.guid IN (5300810,5300811,5300812);"],
        capture_output=True)
    print(r.stdout.decode("utf-8", "replace"))
    if rc1 or rc2 or r.returncode:
        raise SystemExit(1)

if __name__ == "__main__":
    main()
