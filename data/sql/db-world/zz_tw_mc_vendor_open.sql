SET NAMES utf8mb4;

-- Open set vendor: gossip option opens vendor shop; remove 说明
UPDATE creature_template
SET subname='1印记+100金兑换任意部位',
    npcflag = (npcflag | 128),
    gossip_menu_id = 960101
WHERE entry = 9000101;

DELETE FROM gossip_menu_option WHERE MenuID = 960101;
INSERT INTO gossip_menu_option
(MenuID, OptionID, OptionIcon, OptionText, OptionBroadcastTextID, OptionType, OptionNpcFlag, ActionMenuID, ActionPoiID, BoxCoded, BoxMoney, BoxText, BoxBroadcastTextID, VerifiedBuild)
VALUES
(960101, 0, 1, '购买时光套装', 0, 3, 1, 0, 0, 0, 0, NULL, 0, 0);

-- Remove SmartAI that was saying 尚未开放 / showing 说明
DELETE FROM smart_scripts WHERE entryorguid = 9000101 AND source_type = 0;

-- Optional: clear obsolete creature_text for closed state
DELETE FROM creature_text WHERE CreatureID = 9000101 AND GroupID IN (0, 1);
UPDATE creature_template SET AIName='' WHERE entry=9000101;
