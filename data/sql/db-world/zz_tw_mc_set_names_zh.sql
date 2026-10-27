SET NAMES utf8mb4;

UPDATE item_template it
INNER JOIN item_template_locale itl ON itl.ID = it.entry AND itl.locale = 'zhCN'
SET it.name = itl.Name
WHERE it.itemset BETWEEN 9201 AND 9209;

DELETE FROM item_set_names WHERE entry IN (SELECT entry FROM (SELECT entry FROM item_template WHERE itemset BETWEEN 9201 AND 9209) x);
INSERT INTO item_set_names (entry, name, InventoryType, VerifiedBuild)
SELECT it.entry, it.name, it.InventoryType, 18019
FROM item_template it
WHERE it.itemset BETWEEN 9201 AND 9209;

DELETE FROM item_set_names_locale WHERE locale='zhCN' AND ID IN (SELECT entry FROM (SELECT entry FROM item_template WHERE itemset BETWEEN 9201 AND 9209) x);
INSERT INTO item_set_names_locale (ID, locale, Name, VerifiedBuild)
SELECT it.entry, 'zhCN', it.name, 18019
FROM item_template it
WHERE it.itemset BETWEEN 9201 AND 9209;