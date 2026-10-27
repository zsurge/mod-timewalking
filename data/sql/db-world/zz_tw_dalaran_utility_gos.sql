-- zz_tw_dalaran_utility_gos.sql
-- Dalaran Krasus Landing utility gameobjects: DK Runeforge, Guild Vault, Mailbox, Forge, Anvil
-- Idempotent. Custom runeforge 9000103 = 191757 model at size=1 (stock 191757 is size 4.92).
SET NAMES utf8mb4;

SET @GUID_RUNE  := 5300810;
SET @GUID_GUILD := 5300811;
SET @GUID_MAIL  := 5300812;
SET @GUID_FORGE := 5300813;
SET @GUID_ANVIL := 5300814;
SET @ENTRY_RUNE  := 9000103;  -- custom Runeforge display 8176 size=1 type=8 spellfocus 1552
SET @ENTRY_GUILD := 193086;  -- Guild Vault type=34
SET @ENTRY_MAIL  := 193071;  -- Mailbox type=19
SET @ENTRY_FORGE := 1685;  -- Dalaran Forge type=8 Data0=3 size=1
SET @ENTRY_ANVIL := 1684;  -- Blacksmith's Anvil type=8 Data0=1 size=1

DELETE FROM `gameobject_template` WHERE `entry`=@ENTRY_RUNE;
INSERT INTO `gameobject_template` (`entry`,`type`,`displayId`,`name`,`IconName`,`castBarCaption`,`unk1`,`size`,`Data0`,`Data1`,`Data2`,`Data3`,`Data4`,`Data5`,`Data6`,`Data7`,`Data8`,`Data9`,`Data10`,`Data11`,`Data12`,`Data13`,`Data14`,`Data15`,`Data16`,`Data17`,`Data18`,`Data19`,`Data20`,`Data21`,`Data22`,`Data23`,`AIName`,`ScriptName`,`VerifiedBuild`)
VALUES
(@ENTRY_RUNE,8,8176,'Runeforge','','','',1,1552,15,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,'','',0);

DELETE FROM `gameobject_template_addon` WHERE `entry`=@ENTRY_RUNE;
INSERT INTO `gameobject_template_addon` (`entry`,`faction`,`flags`,`mingold`,`maxgold`,`artkit0`,`artkit1`,`artkit2`,`artkit3`)
VALUES (@ENTRY_RUNE,0,32,0,0,0,0,0,0);

DELETE FROM `gameobject_template_locale` WHERE `entry`=@ENTRY_RUNE;
INSERT INTO `gameobject_template_locale` (`entry`,`locale`,`name`,`castBarCaption`,`VerifiedBuild`) VALUES
(@ENTRY_RUNE,'zhCN','符文熔炉','',0),
(@ENTRY_RUNE,'zhTW','符文熔爐','',0),
(@ENTRY_RUNE,'enUS','Runeforge','',0);

DELETE FROM `gameobject` WHERE `guid` IN (@GUID_RUNE, @GUID_GUILD, @GUID_MAIL, @GUID_FORGE, @GUID_ANVIL);
INSERT INTO `gameobject`
(`guid`,`id`,`map`,`zoneId`,`areaId`,`spawnMask`,`phaseMask`,`position_x`,`position_y`,`position_z`,`orientation`,`rotation0`,`rotation1`,`rotation2`,`rotation3`,`spawntimesecs`,`animprogress`,`state`)
VALUES
(@GUID_RUNE,@ENTRY_RUNE,571,4395,4564,1,1,5778.2334,447.9638,658.25,3.2261343,0.000000,0.000000,0.999107,-0.042258,300,100,1),
(@GUID_GUILD,@ENTRY_GUILD,571,4395,4564,1,1,5780.4478,434.46454,660.05,0.44580877,0.000000,0.000000,0.221063,0.975260,300,100,1),
(@GUID_MAIL,@ENTRY_MAIL,571,4395,4564,1,1,5821.194,414.4446,657.58844,1.6788778,0.000000,0.000000,0.744268,0.667881,300,255,1),
(@GUID_FORGE,@ENTRY_FORGE,571,4395,4564,1,1,5845.276,458.3727,658.25,0.33191228,0.000000,0.000000,0.165195,0.986261,300,100,1),
(@GUID_ANVIL,@ENTRY_ANVIL,571,4395,4564,1,1,5846.857,450.22,658.25,2.7115955,0.000000,0.000000,0.976977,0.213346,300,100,1);
