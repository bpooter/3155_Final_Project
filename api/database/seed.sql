-- ============================================
-- CUSTOMERS
-- ============================================

INSERT INTO customers
(customer_id, first_name, last_name, email, phone, address)
VALUES
(1, 'John', 'Smith', 'john.smith@email.com', '555-111-1111', '123 Main St'),
(2, 'Sarah', 'Johnson', 'sarah.johnson@email.com', '555-222-2222', '456 Oak Ave');


-- ============================================
-- MENU ITEMS
-- ============================================

INSERT INTO menu_items
(menu_item_id, item_name, description, price, calories, category)
VALUES
(1, 'Turkey Sandwich', 'Turkey, cheese, lettuce, tomato', 8.99, 650, 'SANDWICH'),
(2, 'BLT', 'Bacon, lettuce, tomato sandwich', 7.99, 550, 'SANDWICH'),
(3, 'French Fries', 'Seasoned fries', 3.49, 400, 'SIDE'),
(4, 'Soft Drink', 'Fountain drink', 1.99, 150, 'DRINK');


-- ============================================
-- RESOURCES / INGREDIENTS
-- Some deliberately low
-- ============================================

INSERT INTO resources
(resource_id, item_name, quantity_on_hand, unit)
VALUES
(1, 'Turkey', 5.00, 'pound'),
(2, 'Bread', 20.00, 'each'),
(3, 'Cheese', 15.00, 'slice'),
(4, 'Lettuce', 10.00, 'ounce'),
(5, 'Tomato', 8.00, 'ounce'),
(6, 'Bacon', 2.00, 'pound'),
(7, 'Potatoes', 3.00, 'pound'),
(8, 'Soda Syrup', 50.00, 'ounce');


-- ============================================
-- RECIPES
-- ============================================

-- Turkey Sandwich
INSERT INTO recipes
(menu_item_id, resource_id, quantity_required)
VALUES
(1,1,0.50),
(1,2,2),
(1,3,1),
(1,4,1),
(1,5,1);

-- BLT
INSERT INTO recipes
(menu_item_id, resource_id, quantity_required)
VALUES
(2,6,0.50),
(2,2,2),
(2,4,1),
(2,5,1);

-- Fries
INSERT INTO recipes
(menu_item_id, resource_id, quantity_required)
VALUES
(3,7,0.50);

-- Drink
INSERT INTO recipes
(menu_item_id, resource_id, quantity_required)
VALUES
(4,8,2);


-- ============================================
-- PROMOTIONS
-- ============================================

INSERT INTO promotions
(promotion_id, promotion_code, discount_type, discount_amount, expiration_date, active)
VALUES
(1,'SAVE20','PERCENTAGE',20.00,'2027-01-01',TRUE),
(2,'FIVEOFF','FIXED',5.00,'2027-01-01',TRUE);


-- ============================================
-- COMPLETED ORDERS
-- Used for revenue/reporting
-- ============================================

INSERT INTO orders
(
order_id,
tracking_number,
customer_id,
guest_name,
guest_email,
guest_phone,
order_type,
order_status,
subtotal,
discount_amount,
total_price,
promotion_id,
order_date
)
VALUES

(1,
'ITIS-A1B2C3',
1,
NULL,
NULL,
NULL,
'TAKEOUT',
'COMPLETED',
17.98,
0.00,
17.98,
NULL,
'2026-07-20 12:30:00'),


(2,
'ITIS-D4E5F6',
NULL,
'Mike Wilson',
'mike@email.com',
'555-333-3333',
'DELIVERY',
'COMPLETED',
25.00,
5.00,
20.00,
2,
'2026-07-21 18:00:00'),


(3,
'ITIS-G7H8I9',
2,
NULL,
NULL,
NULL,
'TAKEOUT',
'COMPLETED',
35.00,
7.00,
28.00,
1,
'2026-07-22 13:00:00');


-- ============================================
-- ORDER DETAILS
-- ============================================

INSERT INTO order_details
(order_id, menu_item_id, quantity, unit_price, special_instructions)
VALUES
(1,1,1,8.99,'No tomato'),
(1,3,1,3.49,NULL),

(2,2,2,7.99,'Extra bacon'),

(3,1,2,8.99,NULL),
(3,4,2,1.99,NULL);


-- ============================================
-- PAYMENTS
-- ============================================

INSERT INTO payments
(order_id, payment_type, amount, card_last_four, transaction_status)
VALUES
(1,'CASH',17.98,NULL,'COMPLETED'),
(2,'CARD',20.00,'1234','COMPLETED'),
(3,'CARD',28.00,'5678','COMPLETED');


-- ============================================
-- REVIEWS
-- Demonstrates high/low ratings
-- ============================================

INSERT INTO reviews
(customer_id, order_id, rating, comment, created_at)
VALUES

(1,1,5,
'Great sandwich and fast service',
'2026-07-20 14:00:00'),

(2,3,4,
'Food was good but delivery was slow',
'2026-07-22 15:00:00'),

(1,2,2,
'Order arrived cold',
'2026-07-21 20:00:00');