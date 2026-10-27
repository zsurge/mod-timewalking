-- zz_tw_mc_restore_boss_loot.sql
-- Point TW bosses back at original MC loot tables (placeholder until ilvl 219 loot).
SET NAMES utf8mb4;
UPDATE `creature_template` tw
INNER JOIN `creature_template` orig ON orig.`entry` = tw.`entry` - 9100000
SET tw.`lootid` = orig.`lootid`,
    tw.`pickpocketloot` = orig.`pickpocketloot`,
    tw.`skinloot` = orig.`skinloot`,
    tw.`mingold` = orig.`mingold`,
    tw.`maxgold` = orig.`maxgold`
WHERE tw.`entry` IN (9111982,9111988,9112056,9112057,9112098,9112118,9112259,9112264);