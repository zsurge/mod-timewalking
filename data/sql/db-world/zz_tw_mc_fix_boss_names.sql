-- zz_tw_mc_fix_boss_names.sql
-- Repair TW boss zhCN locale names from original + （时光）
SET NAMES utf8mb4;
UPDATE `creature_template_locale` tw
INNER JOIN `creature_template_locale` orig
  ON orig.`entry` = tw.`entry` - 9100000 AND orig.`locale` = tw.`locale`
SET tw.`Name` = CONCAT(orig.`Name`, CHAR(0xEF,0xBC,0x88,0xE6,0x97,0xB6,0xE5,0x85,0x89,0xEF,0xBC,0x89))
WHERE tw.`entry` IN (9111982,9111988,9112056,9112057,9112098,9112118,9112259,9112264);

UPDATE `creature_template` tw
INNER JOIN `creature_template` orig ON orig.`entry` = tw.`entry` - 9100000
SET tw.`name` = CONCAT(orig.`name`, CHAR(0xEF,0xBC,0x88,0xE6,0x97,0xB6,0xE5,0x85,0x89,0xEF,0xBC,0x89))
WHERE tw.`entry` IN (9111982,9111988,9112056,9112057,9112098,9112118,9112259,9112264);