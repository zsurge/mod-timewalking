-- zz_tw_dalaran_utility_gos.sql
-- Dalaran Krasus Landing utility gameobjects: DK Runeforge, Guild Vault, Mailbox
-- Idempotent. Stock WotLK entries.
SET NAMES utf8mb4;

SET @GUID_RUNE  := 5300810;
SET @GUID_GUILD := 5300811;
SET @GUID_MAIL  := 5300812;
SET @ENTRY_RUNE  := 191757;  -- Runeforge type=8 spellfocus 1552
SET @ENTRY_GUILD := 193086;  -- Guild Vault type=34
SET @ENTRY_MAIL  := 193071;  -- Mailbox type=19

DELETE FROM `gameobject` WHERE `guid` IN (@GUID_RUNE, @GUID_GUILD, @GUID_MAIL);
INSERT INTO `gameobject`
(`guid`,`id`,`map`,`zoneId`,`areaId`,`spawnMask`,`phaseMask`,`position_x`,`position_y`,`position_z`,`orientation`,`rotation0`,`rotation1`,`rotation2`,`rotation3`,`spawntimesecs`,`animprogress`,`state`)
VALUES
(@GUID_RUNE,@ENTRY_RUNE,571,4395,4564,1,1,5778.2334,447.9638,657.5751,3.2261343,0.000000,0.000000,0.999107,-0.042258,300,100,1),
(@GUID_GUILD,@ENTRY_GUILD,571,4395,4564,1,1,5780.4478,434.46454,657.55396,0.44580877,0.000000,0.000000,0.221063,0.975260,300,100,1),
(@GUID_MAIL,@ENTRY_MAIL,571,4395,4564,1,1,5821.194,414.4446,657.58844,1.6788778,0.000000,0.000000,0.744268,0.667881,300,255,1);
