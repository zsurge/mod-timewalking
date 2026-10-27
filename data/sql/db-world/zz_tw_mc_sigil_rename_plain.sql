SET NAMES utf8mb4;
UPDATE item_template SET name='Molten Timewalking Sigil', description='Exchange for any Timewalking T1-look set piece (1 sigil + 100 gold).' WHERE entry BETWEEN 9129001 AND 9129008;
DELETE FROM item_template_locale WHERE ID BETWEEN 9129001 AND 9129008 AND locale='zhCN';
INSERT INTO item_template_locale (ID, locale, Name, Description, VerifiedBuild) VALUES
(9129001,'zhCN','熔火时光印记','达拉然时光套装兑换员处：1枚印记+100金兑换任意部位时光套装。',18019),
(9129002,'zhCN','熔火时光印记','达拉然时光套装兑换员处：1枚印记+100金兑换任意部位时光套装。',18019),
(9129003,'zhCN','熔火时光印记','达拉然时光套装兑换员处：1枚印记+100金兑换任意部位时光套装。',18019),
(9129004,'zhCN','熔火时光印记','达拉然时光套装兑换员处：1枚印记+100金兑换任意部位时光套装。',18019),
(9129005,'zhCN','熔火时光印记','达拉然时光套装兑换员处：1枚印记+100金兑换任意部位时光套装。',18019),
(9129006,'zhCN','熔火时光印记','达拉然时光套装兑换员处：1枚印记+100金兑换任意部位时光套装。',18019),
(9129007,'zhCN','熔火时光印记','达拉然时光套装兑换员处：1枚印记+100金兑换任意部位时光套装。',18019),
(9129008,'zhCN','熔火时光印记','达拉然时光套装兑换员处：1枚印记+100金兑换任意部位时光套装。',18019);