# -*- coding: utf-8 -*-
import subprocess
bq = chr(96)
def qi(name):
    return bq + name + bq

cols_ct = ", ".join(qi(c) for c in [
    "entry", "name", "subname", "IconName", "gossip_menu_id", "minlevel", "maxlevel",
    "faction", "npcflag", "unit_class", "unit_flags", "type", "flags_extra", "ScriptName", "AIName"])
cols_model = ", ".join(qi(c) for c in ["CreatureID", "Idx", "CreatureDisplayID", "DisplayScale", "Probability"])
cols_loc = ", ".join(qi(c) for c in ["entry", "locale", "Name", "Title", "VerifiedBuild"])
cols_gm = ", ".join(qi(c) for c in ["MenuID", "TextID"])
cols_gmo = ", ".join(qi(c) for c in [
    "MenuID", "OptionID", "OptionIcon", "OptionText", "OptionBroadcastTextID",
    "OptionType", "OptionNpcFlag", "ActionMenuID", "ActionPoiID", "BoxCoded", "BoxMoney", "BoxText", "BoxBroadcastTextID"])
cols_ctext = ", ".join(qi(c) for c in [
    "CreatureID", "GroupID", "ID", "Text", "Type", "Language",
    "Probability", "Emote", "Duration", "Sound", "BroadcastTextId", "TextRange", "comment"])
cols_smart = ",".join(qi(c) for c in [
    "entryorguid", "source_type", "id", "link", "event_type", "event_phase_mask", "event_chance", "event_flags",
    "event_param1", "event_param2", "event_param3", "event_param4", "event_param5", "event_param6",
    "action_type", "action_param1", "action_param2", "action_param3", "action_param4", "action_param5", "action_param6",
    "target_type", "target_param1", "target_param2", "target_param3", "target_param4",
    "target_x", "target_y", "target_z", "target_o", "comment"])
cols_cre = ",".join(qi(c) for c in [
    "guid", "id", "map", "zoneId", "areaId", "spawnMask", "phaseMask", "equipment_id",
    "position_x", "position_y", "position_z", "orientation", "spawntimesecs", "wander_distance",
    "currentwaypoint", "curhealth", "curmana", "MovementType"])

def S(s):
    return s

L = []
L.append("-- zz_tw_dalaran_entrance_npcs.sql")
L.append("-- Dalaran Timewalking entrance + set vendor placeholders (Krasus Landing)")
L.append("-- Idempotent.")
L.append("SET NAMES utf8mb4;")
L.append("")
L.append("SET @ENTRY_PORTAL := 9000100;")
L.append("SET @ENTRY_VENDOR := 9000101;")
L.append("SET @GUID_PORTAL  := 5300800;")
L.append("SET @GUID_VENDOR  := 5300801;")
L.append("SET @MENU_PORTAL  := 960100;")
L.append("SET @MENU_VENDOR  := 960101;")
L.append("SET @MODEL_PORTAL := 28127;")
L.append("SET @MODEL_VENDOR := 25907;")
L.append("")
L.append("DELETE FROM " + qi("creature_template") + " WHERE " + qi("entry") + " IN (@ENTRY_PORTAL, @ENTRY_VENDOR);")
L.append("INSERT INTO " + qi("creature_template"))
L.append("(" + cols_ct + ")")
L.append("VALUES")
L.append("(@ENTRY_PORTAL, " + repr("时光副本") + ", " + repr("熔火之心（时光）") + ", 'Speak', @MENU_PORTAL, 80, 80, 35, 1, 1, 2, 7, 2, '', 'SmartAI'),")
L.append("(@ENTRY_VENDOR, " + repr("时光套装兑换") + ", " + repr("代币换装（占位）") + ", 'Speak', @MENU_VENDOR, 80, 80, 35, 1, 1, 2, 7, 2, '', 'SmartAI');")
L.append("")
L.append("DELETE FROM " + qi("creature_template_model") + " WHERE " + qi("CreatureID") + " IN (@ENTRY_PORTAL, @ENTRY_VENDOR);")
L.append("INSERT INTO " + qi("creature_template_model") + " (" + cols_model + ") VALUES")
L.append("(@ENTRY_PORTAL, 0, @MODEL_PORTAL, 1, 1),")
L.append("(@ENTRY_VENDOR, 0, @MODEL_VENDOR, 1, 1);")
L.append("")
L.append("DELETE FROM " + qi("creature_template_locale") + " WHERE " + qi("entry") + " IN (@ENTRY_PORTAL, @ENTRY_VENDOR) AND " + qi("locale") + "='zhCN';")
L.append("INSERT INTO " + qi("creature_template_locale") + " (" + cols_loc + ") VALUES")
L.append("(@ENTRY_PORTAL, 'zhCN', " + repr("时光副本") + ", " + repr("熔火之心（时光）") + ", 0),")
L.append("(@ENTRY_VENDOR, 'zhCN', " + repr("时光套装兑换") + ", " + repr("代币换装（占位）") + ", 0);")
L.append("")
L.append("DELETE FROM " + qi("gossip_menu") + " WHERE " + qi("MenuID") + " IN (@MENU_PORTAL, @MENU_VENDOR);")
L.append("INSERT INTO " + qi("gossip_menu") + " (" + cols_gm + ") VALUES")
L.append("(@MENU_PORTAL, 1),")
L.append("(@MENU_VENDOR, 1);")
L.append("")
L.append("DELETE FROM " + qi("gossip_menu_option") + " WHERE " + qi("MenuID") + " IN (@MENU_PORTAL, @MENU_VENDOR);")
L.append("INSERT INTO " + qi("gossip_menu_option"))
L.append("(" + cols_gmo + ")")
L.append("VALUES")
L.append("(@MENU_PORTAL, 0, 0, " + repr("进入熔火之心（时光）") + ", 0, 1, 1, 0, 0, 0, 0, NULL, 0),")
L.append("(@MENU_PORTAL, 1, 0, " + repr("了解时光副本（说明）") + ", 0, 1, 1, 0, 0, 0, 0, NULL, 0),")
L.append("(@MENU_VENDOR, 0, 0, " + repr("兑换时光套装（尚未开放）") + ", 0, 1, 1, 0, 0, 0, 0, NULL, 0),")
L.append("(@MENU_VENDOR, 1, 0, " + repr("说明：Boss 掉代币，按部位兑换「时光」+原T1名") + ", 0, 1, 1, 0, 0, 0, 0, NULL, 0);")
L.append("")
L.append("DELETE FROM " + qi("creature_text") + " WHERE " + qi("CreatureID") + " IN (@ENTRY_PORTAL, @ENTRY_VENDOR);")
L.append("INSERT INTO " + qi("creature_text") + " (" + cols_ctext + ") VALUES")
L.append("(@ENTRY_PORTAL, 0, 0, " + repr("时光熔火之心：10 人团本，装等目标 219，周锁。Boss 脚本与 219 掉落下一阶段再做。") + ", 12, 0, 100, 1, 0, 0, 0, 0, 'TW portal help'),")
L.append("(@ENTRY_VENDOR, 0, 0, " + repr("套装兑换尚未开放。计划：Boss 掉 219 散件 + 代币，按部位兑换「时光」+ 原 T1 套装名。") + ", 12, 0, 100, 1, 0, 0, 0, 0, 'TW vendor help'),")
L.append("(@ENTRY_VENDOR, 1, 0, " + repr("兑换功能占位中，请稍后再来。") + ", 12, 0, 100, 1, 0, 0, 0, 0, 'TW vendor not open');")
L.append("")
L.append("DELETE FROM " + qi("smart_scripts") + " WHERE " + qi("entryorguid") + " IN (@ENTRY_PORTAL, @ENTRY_VENDOR) AND " + qi("source_type") + "=0;")
L.append("INSERT INTO " + qi("smart_scripts"))
L.append("(" + cols_smart + ")")
L.append("VALUES")
L.append("(@ENTRY_PORTAL,0,0,1,62,0,100,0,@MENU_PORTAL,0,0,0,0,0,62,960,0,0,0,0,0,7,0,0,0,0,1091.89,-466.985,-105.084,3.14159,'TW Portal - Enter TW MC'),")
L.append("(@ENTRY_PORTAL,0,1,0,61,0,100,0,0,0,0,0,0,0,72,0,0,0,0,0,0,7,0,0,0,0,0,0,0,0,'TW Portal - Close'),")
L.append("(@ENTRY_PORTAL,0,2,3,62,0,100,0,@MENU_PORTAL,1,0,0,0,0,1,0,0,0,0,0,0,7,0,0,0,0,0,0,0,0,'TW Portal - Help text'),")
L.append("(@ENTRY_PORTAL,0,3,0,61,0,100,0,0,0,0,0,0,0,72,0,0,0,0,0,0,7,0,0,0,0,0,0,0,0,'TW Portal - Close help'),")
L.append("(@ENTRY_VENDOR,0,0,1,62,0,100,0,@MENU_VENDOR,0,0,0,0,0,1,1,0,0,0,0,0,7,0,0,0,0,0,0,0,0,'TW Vendor - Not open text'),")
L.append("(@ENTRY_VENDOR,0,1,0,61,0,100,0,0,0,0,0,0,0,72,0,0,0,0,0,0,7,0,0,0,0,0,0,0,0,'TW Vendor - Close'),")
L.append("(@ENTRY_VENDOR,0,2,3,62,0,100,0,@MENU_VENDOR,1,0,0,0,0,1,0,0,0,0,0,0,7,0,0,0,0,0,0,0,0,'TW Vendor - Spec text'),")
L.append("(@ENTRY_VENDOR,0,3,0,61,0,100,0,0,0,0,0,0,0,72,0,0,0,0,0,0,7,0,0,0,0,0,0,0,0,'TW Vendor - Close help');")
L.append("")
L.append("DELETE FROM " + qi("creature") + " WHERE " + qi("guid") + " IN (@GUID_PORTAL, @GUID_VENDOR) OR " + qi("id") + " IN (@ENTRY_PORTAL, @ENTRY_VENDOR);")
L.append("INSERT INTO " + qi("creature"))
L.append("(" + cols_cre + ")")
L.append("VALUES")
L.append("(@GUID_PORTAL,@ENTRY_PORTAL,571,4395,4564,1,1,0,5808.50,430.20,658.78,4.0,300,0,0,1,0,0),")
L.append("(@GUID_VENDOR,@ENTRY_VENDOR,571,4395,4564,1,1,0,5811.20,427.80,658.78,4.2,300,0,0,1,0,0);")
L.append("")

path = r"E:\azerothcore\modules\mod-timewalking\data\sql\db-world\zz_tw_dalaran_entrance_npcs.sql"
text = "\n".join(L)
# MySQL wants single-quoted strings; repr() uses single quotes for Chinese - good
open(path, "w", encoding="utf-8", newline="\n").write(text)
assert qi("name") in text and qi("faction") in text
print("wrote ok", len(text))

r = subprocess.run(
    [r"D:\acore\mysql8.4\bin\mysql.exe", "--host=127.0.0.1", "--port=3308", "-usurge", "-pacer@1123",
     "--default-character-set=utf8mb4", "acore_world"],
    input=text.encode("utf-8"), capture_output=True)
print("mysql", r.returncode)
print(r.stderr.decode("utf-8", "replace"))
r = subprocess.run(
    [r"D:\acore\mysql8.4\bin\mysql.exe", "--host=127.0.0.1", "--port=3308", "-usurge", "-pacer@1123", "-N",
     "--default-character-set=utf8mb4", "acore_world", "-e",
     "SELECT entry,name,subname,AIName,gossip_menu_id FROM creature_template WHERE entry IN (9000100,9000101);"
     "SELECT guid,id,ROUND(position_x,2),ROUND(position_y,2),ROUND(position_z,2) FROM creature WHERE id IN (9000100,9000101);"
     "SELECT COUNT(*) FROM smart_scripts WHERE entryorguid IN (9000100,9000101);"],
    capture_output=True)
print(r.stdout.decode("utf-8", "replace"))
