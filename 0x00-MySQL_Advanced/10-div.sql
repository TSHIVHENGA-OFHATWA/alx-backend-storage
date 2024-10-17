-- Create a function SafeDiv that divides a by b, returning 0 if b is 0

DELIMITER $$

CREATE FUNCTION SafeDiv(a INT, b INT)
RETURNS DECIMAL(10, 6)
DETERMINISTIC
BEGIN
    RETURN IF(b = 0, 0, a / b);
END $$

DELIMITER ;
