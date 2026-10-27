-- zz_tw_dalaran_entrance_npcs.sql
-- Dalaran Timewalking entrance + set vendor placeholders (Krasus Landing)
-- Idempotent.
SET NAMES utf8mb4;

SET @ENTRY_PORTAL := 9000100;
SET @ENTRY_VENDOR := 9000101;
SET @GUID_PORTAL  := 5300800;
SET @GUID_VENDOR  := 5300801;
SET @MENU_PORTAL  := 960100;
SET @MENU_VENDOR  := 960101;
SET @MODEL_PORTAL := 28127;
SET @MODEL_VENDOR := 25907;

DELETE FROM `creature_template` WHERE `entry` IN (@ENTRY_PORTAL, @ENTRY_VENDOR);
INSERT INTO `creature_template`
(`entry`, `name`, `subname`, `IconName`, `gossip_menu_id`, `minlevel`, `maxlevel`, `faction`, `npcflag`, `unit_class`, `unit_flags`, `type`, `flags_extra`, `ScriptName`, `AIName`)
VALUES
(@ENTRY_PORTAL, '时光副本', '熔火之心（时光）', 'Speak', @MENU_PORTAL, 80, 80, 35, 1, 1, 2, 7, 2, '', 'SmartAI'),
(@ENTRY_VENDOR, '时光套装兑换', '代币换装（占位）', 'Speak', @MENU_VENDOR, 80, 80, 35, 1, 1, 2, 7, 2, '', 'SmartAI');

DELETE FROM `creature_template_model` WHERE `CreatureID` IN (@ENTRY_PORTAL, @ENTRY_VENDOR);
INSERT INTO `creature_template_model` (`CreatureID`, `Idx`, `CreatureDisplayID`, `DisplayScale`, `Probability`) VALUES
(@ENTRY_PORTAL, 0, @MODEL_PORTAL, 1, 1),
(@ENTRY_VENDOR, 0, @MODEL_VENDOR, 1, 1);

DELETE FROM `creature_template_locale` WHERE `entry` IN (@ENTRY_PORTAL, @ENTRY_VENDOR) AND `locale`='zhCN';
INSERT INTO `creature_template_locale` (`entry`, `locale`, `Name`, `Title`, `VerifiedBuild`) VALUES
(@ENTRY_PORTAL, 'zhCN', '时光副本', '熔火之心（时光）', 0),
(@ENTRY_VENDOR, 'zhCN', '时光套装兑换', '代币换装（占位）', 0);

DELETE FROM `gossip_menu` WHERE `MenuID` IN (@MENU_PORTAL, @MENU_VENDOR);
INSERT INTO `gossip_menu` (`MenuID`, `TextID`) VALUES
(@MENU_PORTAL, 1),
(@MENU_VENDOR, 1);

DELETE FROM `gossip_menu_option` WHERE `MenuID` IN (@MENU_PORTAL, @MENU_VENDOR);
INSERT INTO `gossip_menu_option`
(`MenuID`, `OptionID`, `OptionIcon`, `OptionText`, `OptionBroadcastTextID`, `OptionType`, `OptionNpcFlag`, `ActionMenuID`, `ActionPoiID`, `BoxCoded`, `BoxMoney`, `BoxText`, `BoxBroadcastTextID`)
VALUES
(@MENU_PORTAL, 0, 0, '进入熔火之心（时光）', 0, 1, 1, 0, 0, 0, 0, NULL, 0),
(@MENU_PORTAL, 1, 0, '了解时光副本（说明）', 0, 1, 1, 0, 0, 0, 0, NULL, 0),
(@MENU_VENDOR, 0, 0, '兑换时光套装（尚未开放）', 0, 1, 1, 0, 0, 0, 0, NULL, 0),
(@MENU_VENDOR, 1, 0, '说明：Boss 掉代币，按部位兑换「时光」+原T1名', 0, 1, 1, 0, 0, 0, 0, NULL, 0);

DELETE FROM `creature_text` WHERE `CreatureID` IN (@ENTRY_PORTAL, @ENTRY_VENDOR);
INSERT INTO `creature_text` (`CreatureID`, `GroupID`, `ID`, `Text`, `Type`, `Language`, `Probability`, `Emote`, `Duration`, `Sound`, `BroadcastTextId`, `TextRange`, `comment`) VALUES
(@ENTRY_PORTAL, 0, 0, '时光熔火之心：10 人团本，装等目标 219，周锁。Boss 脚本与 219 掉落下一阶段再做。', 12, 0, 100, 1, 0, 0, 0, 0, 'TW portal help'),
(@ENTRY_VENDOR, 0, 0, '套装兑换尚未开放。计划：Boss 掉 219 散件 + 代币，按部位兑换「时光」+ 原 T1 套装名。', 12, 0, 100, 1, 0, 0, 0, 0, 'TW vendor help'),
(@ENTRY_VENDOR, 1, 0, '兑换功能占位中，请稍后再来。', 12, 0, 100, 1, 0, 0, 0, 0, 'TW vendor not open');

DELETE FROM `smart_scripts` WHERE `entryorguid` IN (@ENTRY_PORTAL, @ENTRY_VENDOR) AND `source_type`=0;
INSERT INTO `smart_scripts`
(`entryorguid`,`source_type`,`id`,`link`,`event_type`,`event_phase_mask`,`event_chance`,`event_flags`,`event_param1`,`event_param2`,`event_param3`,`event_param4`,`event_param5`,`event_param6`,`action_type`,`action_param1`,`action_param2`,`action_param3`,`action_param4`,`action_param5`,`action_param6`,`target_type`,`target_param1`,`target_param2`,`target_param3`,`target_param4`,`target_x`,`target_y`,`target_z`,`target_o`,`comment`)
VALUES
(@ENTRY_PORTAL,0,0,1,62,0,100,0,@MENU_PORTAL,0,0,0,0,0,62,960,0,0,0,0,0,7,0,0,0,0,1091.89,-466.985,-105.084,3.14159,'TW Portal - Enter TW MC'),
(@ENTRY_PORTAL,0,1,0,61,0,100,0,0,0,0,0,0,0,72,0,0,0,0,0,0,7,0,0,0,0,0,0,0,0,'TW Portal - Close'),
(@ENTRY_PORTAL,0,2,3,62,0,100,0,@MENU_PORTAL,1,0,0,0,0,1,0,0,0,0,0,0,7,0,0,0,0,0,0,0,0,'TW Portal - Help text'),
(@ENTRY_PORTAL,0,3,0,61,0,100,0,0,0,0,0,0,0,72,0,0,0,0,0,0,7,0,0,0,0,0,0,0,0,'TW Portal - Close help'),
(@ENTRY_VENDOR,0,0,1,62,0,100,0,@MENU_VENDOR,0,0,0,0,0,1,1,0,0,0,0,0,7,0,0,0,0,0,0,0,0,'TW Vendor - Not open text'),
(@ENTRY_VENDOR,0,1,0,61,0,100,0,0,0,0,0,0,0,72,0,0,0,0,0,0,7,0,0,0,0,0,0,0,0,'TW Vendor - Close'),
(@ENTRY_VENDOR,0,2,3,62,0,100,0,@MENU_VENDOR,1,0,0,0,0,1,0,0,0,0,0,0,7,0,0,0,0,0,0,0,0,'TW Vendor - Spec text'),
(@ENTRY_VENDOR,0,3,0,61,0,100,0,0,0,0,0,0,0,72,0,0,0,0,0,0,7,0,0,0,0,0,0,0,0,'TW Vendor - Close help');

DELETE FROM `creature` WHERE `guid` IN (@GUID_PORTAL, @GUID_VENDOR) OR `id` IN (@ENTRY_PORTAL, @ENTRY_VENDOR);
INSERT INTO `creature`
(`guid`,`id`,`map`,`zoneId`,`areaId`,`spawnMask`,`phaseMask`,`equipment_id`,`position_x`,`position_y`,`position_z`,`orientation`,`spawntimesecs`,`wander_distance`,`currentwaypoint`,`curhealth`,`curmana`,`MovementType`)
VALUES
(@GUID_PORTAL,@ENTRY_PORTAL,571,4395,4564,1,1,0,5808.50,430.20,658.78,4.0,300,0,0,1,0,0),
(@GUID_VENDOR,@ENTRY_VENDOR,571,4395,4564,1,1,0,5811.20,427.80,658.78,4.2,300,0,0,1,0,0);
