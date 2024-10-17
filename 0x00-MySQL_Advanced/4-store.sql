-- Script to create a trigger that decreases quantity after adding an order
CREATE TRIGGER decrease_quantity 
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
    UPDATE items
    SET quantity = quantity - NEW.number
    WHERE name = NEW.item_name;
END;
