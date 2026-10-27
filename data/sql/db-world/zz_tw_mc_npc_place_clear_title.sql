SET NAMES utf8mb4;

-- Positions (confirm)
UPDATE creature SET
  position_x=5808.5, position_y=430.2, position_z=658.78, orientation=4.0
WHERE guid=5300800 AND id=9000100;

UPDATE creature SET
  position_x=5811.2, position_y=427.8, position_z=658.78, orientation=4.2
WHERE guid=5300801 AND id=9000101;

-- Remove subtitle under exchange NPC (no 占位 / no second line)
UPDATE creature_template SET subname='' WHERE entry=9000101;
UPDATE creature_template_locale SET Title='' WHERE entry=9000101;