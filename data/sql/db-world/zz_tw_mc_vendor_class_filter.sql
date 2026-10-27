SET NAMES utf8mb4;

-- TW set vendor: only show items for player class (CONDITION_CLASS uses class mask)
DELETE FROM conditions WHERE SourceTypeOrReferenceId=23 AND SourceGroup=9000101;

INSERT INTO conditions (SourceTypeOrReferenceId,SourceGroup,SourceEntry,SourceId,ElseGroup,ConditionTypeOrReference,ConditionTarget,ConditionValue1,ConditionValue2,ConditionValue3,NegativeCondition,ErrorType,ErrorTextId,ScriptName,Comment) VALUES
(23,9000101,9136795,0,0,15,0,128,0,0,0,0,0,'', 'TW vendor class filter: 奥术师头冠（时光）'),
(23,9000101,9136796,0,0,15,0,128,0,0,0,0,0,'', 'TW vendor class filter: 奥术师护腿（时光）'),
(23,9000101,9136797,0,0,15,0,128,0,0,0,0,0,'', 'TW vendor class filter: 奥术师衬肩（时光）'),
(23,9000101,9136798,0,0,15,0,128,0,0,0,0,0,'', 'TW vendor class filter: 奥术师长袍（时光）'),
(23,9000101,9136799,0,0,15,0,128,0,0,0,0,0,'', 'TW vendor class filter: 奥术师护腕（时光）'),
(23,9000101,9136800,0,0,15,0,128,0,0,0,0,0,'', 'TW vendor class filter: 奥术师便鞋（时光）'),
(23,9000101,9136801,0,0,15,0,128,0,0,0,0,0,'', 'TW vendor class filter: 奥术师手套（时光）'),
(23,9000101,9136802,0,0,15,0,128,0,0,0,0,0,'', 'TW vendor class filter: 奥术师腰带（时光）'),
(23,9000101,9136811,0,0,15,0,16,0,0,0,0,0,'', 'TW vendor class filter: 预言之靴（时光）'),
(23,9000101,9136812,0,0,15,0,16,0,0,0,0,0,'', 'TW vendor class filter: 预言手套（时光）'),
(23,9000101,9136813,0,0,15,0,16,0,0,0,0,0,'', 'TW vendor class filter: 预言头饰（时光）'),
(23,9000101,9136814,0,0,15,0,16,0,0,0,0,0,'', 'TW vendor class filter: 预言短裤（时光）'),
(23,9000101,9136815,0,0,15,0,16,0,0,0,0,0,'', 'TW vendor class filter: 预言法袍（时光）'),
(23,9000101,9136816,0,0,15,0,16,0,0,0,0,0,'', 'TW vendor class filter: 预言衬肩（时光）'),
(23,9000101,9136817,0,0,15,0,16,0,0,0,0,0,'', 'TW vendor class filter: 预言束带（时光）'),
(23,9000101,9136819,0,0,15,0,16,0,0,0,0,0,'', 'TW vendor class filter: 预言臂甲（时光）'),
(23,9000101,9136803,0,0,15,0,256,0,0,0,0,0,'', 'TW vendor class filter: 恶魔之心便鞋（时光）'),
(23,9000101,9136804,0,0,15,0,256,0,0,0,0,0,'', 'TW vendor class filter: 恶魔之心护腕（时光）'),
(23,9000101,9136805,0,0,15,0,256,0,0,0,0,0,'', 'TW vendor class filter: 恶魔之心手套（时光）'),
(23,9000101,9136806,0,0,15,0,256,0,0,0,0,0,'', 'TW vendor class filter: 恶魔之心腰带（时光）');

INSERT INTO conditions (SourceTypeOrReferenceId,SourceGroup,SourceEntry,SourceId,ElseGroup,ConditionTypeOrReference,ConditionTarget,ConditionValue1,ConditionValue2,ConditionValue3,NegativeCondition,ErrorType,ErrorTextId,ScriptName,Comment) VALUES
(23,9000101,9136807,0,0,15,0,256,0,0,0,0,0,'', 'TW vendor class filter: 恶魔之心护肩（时光）'),
(23,9000101,9136808,0,0,15,0,256,0,0,0,0,0,'', 'TW vendor class filter: 恶魔之心角饰（时光）'),
(23,9000101,9136809,0,0,15,0,256,0,0,0,0,0,'', 'TW vendor class filter: 恶魔之心长袍（时光）'),
(23,9000101,9136810,0,0,15,0,256,0,0,0,0,0,'', 'TW vendor class filter: 恶魔之心短裤（时光）'),
(23,9000101,9136820,0,0,15,0,8,0,0,0,0,0,'', 'TW vendor class filter: 夜幕杀手胸甲（时光）'),
(23,9000101,9136821,0,0,15,0,8,0,0,0,0,0,'', 'TW vendor class filter: 夜幕杀手头巾（时光）'),
(23,9000101,9136822,0,0,15,0,8,0,0,0,0,0,'', 'TW vendor class filter: 夜幕杀手短裤（时光）'),
(23,9000101,9136823,0,0,15,0,8,0,0,0,0,0,'', 'TW vendor class filter: 夜幕杀手护肩（时光）'),
(23,9000101,9136824,0,0,15,0,8,0,0,0,0,0,'', 'TW vendor class filter: 夜幕杀手长靴（时光）'),
(23,9000101,9136825,0,0,15,0,8,0,0,0,0,0,'', 'TW vendor class filter: 夜幕杀手护腕（时光）'),
(23,9000101,9136826,0,0,15,0,8,0,0,0,0,0,'', 'TW vendor class filter: 夜幕杀手手套（时光）'),
(23,9000101,9136827,0,0,15,0,8,0,0,0,0,0,'', 'TW vendor class filter: 夜幕杀手腰带（时光）'),
(23,9000101,9136828,0,0,15,0,1024,0,0,0,0,0,'', 'TW vendor class filter: 塞纳里奥腰带（时光）'),
(23,9000101,9136829,0,0,15,0,1024,0,0,0,0,0,'', 'TW vendor class filter: 塞纳里奥长靴（时光）'),
(23,9000101,9136830,0,0,15,0,1024,0,0,0,0,0,'', 'TW vendor class filter: 塞纳里奥护腕（时光）'),
(23,9000101,9136831,0,0,15,0,1024,0,0,0,0,0,'', 'TW vendor class filter: 塞纳里奥手套（时光）'),
(23,9000101,9136833,0,0,15,0,1024,0,0,0,0,0,'', 'TW vendor class filter: 塞纳里奥胸甲（时光）'),
(23,9000101,9136834,0,0,15,0,1024,0,0,0,0,0,'', 'TW vendor class filter: 塞纳里奥头盔（时光）'),
(23,9000101,9136835,0,0,15,0,1024,0,0,0,0,0,'', 'TW vendor class filter: 塞纳里奥护腿（时光）'),
(23,9000101,9136836,0,0,15,0,1024,0,0,0,0,0,'', 'TW vendor class filter: 塞纳里奥肩甲（时光）');

INSERT INTO conditions (SourceTypeOrReferenceId,SourceGroup,SourceEntry,SourceId,ElseGroup,ConditionTypeOrReference,ConditionTarget,ConditionValue1,ConditionValue2,ConditionValue3,NegativeCondition,ErrorType,ErrorTextId,ScriptName,Comment) VALUES
(23,9000101,9136845,0,0,15,0,4,0,0,0,0,0,'', 'TW vendor class filter: 巨人追猎者胸甲（时光）'),
(23,9000101,9136846,0,0,15,0,4,0,0,0,0,0,'', 'TW vendor class filter: 巨人追猎者头盔（时光）'),
(23,9000101,9136847,0,0,15,0,4,0,0,0,0,0,'', 'TW vendor class filter: 巨人追猎者护腿（时光）'),
(23,9000101,9136848,0,0,15,0,4,0,0,0,0,0,'', 'TW vendor class filter: 巨人追猎者肩饰（时光）'),
(23,9000101,9136849,0,0,15,0,4,0,0,0,0,0,'', 'TW vendor class filter: 巨人追猎者长靴（时光）'),
(23,9000101,9136850,0,0,15,0,4,0,0,0,0,0,'', 'TW vendor class filter: 巨人追猎者护腕（时光）'),
(23,9000101,9136851,0,0,15,0,4,0,0,0,0,0,'', 'TW vendor class filter: 巨人追猎者腰带（时光）'),
(23,9000101,9136852,0,0,15,0,4,0,0,0,0,0,'', 'TW vendor class filter: 巨人追猎者手套（时光）'),
(23,9000101,9136837,0,0,15,0,64,0,0,0,0,0,'', 'TW vendor class filter: 大地之怒长靴（时光）'),
(23,9000101,9136838,0,0,15,0,64,0,0,0,0,0,'', 'TW vendor class filter: 大地之怒腰带（时光）'),
(23,9000101,9136839,0,0,15,0,64,0,0,0,0,0,'', 'TW vendor class filter: 大地之怒护手（时光）'),
(23,9000101,9136840,0,0,15,0,64,0,0,0,0,0,'', 'TW vendor class filter: 大地之怒护腕（时光）'),
(23,9000101,9136841,0,0,15,0,64,0,0,0,0,0,'', 'TW vendor class filter: 大地之怒外衣（时光）'),
(23,9000101,9136842,0,0,15,0,64,0,0,0,0,0,'', 'TW vendor class filter: 大地之怒头盔（时光）'),
(23,9000101,9136843,0,0,15,0,64,0,0,0,0,0,'', 'TW vendor class filter: 大地之怒腿甲（时光）'),
(23,9000101,9136844,0,0,15,0,64,0,0,0,0,0,'', 'TW vendor class filter: 大地之怒肩饰（时光）'),
(23,9000101,9136853,0,0,15,0,2,0,0,0,0,0,'', 'TW vendor class filter: 秩序之源胸甲（时光）'),
(23,9000101,9136854,0,0,15,0,2,0,0,0,0,0,'', 'TW vendor class filter: 秩序之源头盔（时光）'),
(23,9000101,9136855,0,0,15,0,2,0,0,0,0,0,'', 'TW vendor class filter: 秩序之源腿铠（时光）'),
(23,9000101,9136856,0,0,15,0,2,0,0,0,0,0,'', 'TW vendor class filter: 秩序之源肩铠（时光）');

INSERT INTO conditions (SourceTypeOrReferenceId,SourceGroup,SourceEntry,SourceId,ElseGroup,ConditionTypeOrReference,ConditionTarget,ConditionValue1,ConditionValue2,ConditionValue3,NegativeCondition,ErrorType,ErrorTextId,ScriptName,Comment) VALUES
(23,9000101,9136857,0,0,15,0,2,0,0,0,0,0,'', 'TW vendor class filter: 秩序之源护腕（时光）'),
(23,9000101,9136858,0,0,15,0,2,0,0,0,0,0,'', 'TW vendor class filter: 秩序之源腰带（时光）'),
(23,9000101,9136859,0,0,15,0,2,0,0,0,0,0,'', 'TW vendor class filter: 秩序之源战靴（时光）'),
(23,9000101,9136860,0,0,15,0,2,0,0,0,0,0,'', 'TW vendor class filter: 秩序之源护手（时光）'),
(23,9000101,9136861,0,0,15,0,1,0,0,0,0,0,'', 'TW vendor class filter: 力量护腕（时光）'),
(23,9000101,9136862,0,0,15,0,1,0,0,0,0,0,'', 'TW vendor class filter: 力量马靴（时光）'),
(23,9000101,9136863,0,0,15,0,1,0,0,0,0,0,'', 'TW vendor class filter: 力量护手（时光）'),
(23,9000101,9136864,0,0,15,0,1,0,0,0,0,0,'', 'TW vendor class filter: 力量腰带（时光）'),
(23,9000101,9136865,0,0,15,0,1,0,0,0,0,0,'', 'TW vendor class filter: 力量胸甲（时光）'),
(23,9000101,9136866,0,0,15,0,1,0,0,0,0,0,'', 'TW vendor class filter: 力量头盔（时光）'),
(23,9000101,9136867,0,0,15,0,1,0,0,0,0,0,'', 'TW vendor class filter: 力量腿铠（时光）'),
(23,9000101,9136868,0,0,15,0,1,0,0,0,0,0,'', 'TW vendor class filter: 力量肩铠（时光）');
