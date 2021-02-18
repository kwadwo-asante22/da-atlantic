-- CREATE TABLES

CREATE TABLE IF NOT EXISTS customers (
    'customer_id' INTEGER NOT NULL PRIMARY KEY,
    'customer_firstname' TEXT,
    'customer_lastname' TEXT,
    'customer_street_address' TEXT,
    'customer_state' TEXT,
    'customer_zip_code' INTEGER,
    'purchase_status' TEXT,
);

CREATE TABLE IF NOT EXISTS products (
    'product_id' INTEGER NOT NULL PRIMARY KEY,
    'product_name' TEXT,
    'purchase_amount' REAL,
    'date_time' NUMERIC,
    'customer_id' INTEGER
    FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
);
