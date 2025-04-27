-- Create users table
CREATE TABLE users (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL DEFAULT 0.00 CHECK (amount >= 0),
    orders INTEGER NOT NULL DEFAULT 0 CHECK (orders >= 0)
);

-- Create orders table
CREATE TABLE orders (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    user_id BIGINT NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL CHECK (total_amount >= 0),
    status TEXT NOT NULL DEFAULT 'Pending' CHECK (status IN ('Pending', 'Completed', 'Cancelled')),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Create order_items table
CREATE TABLE order_items (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    order_id BIGINT NOT NULL,
    menu_item_id BIGINT NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    price_at_order DECIMAL(10, 2) NOT NULL CHECK (price_at_order >= 0),
    CONSTRAINT fk_order FOREIGN KEY (order_id) REFERENCES orders(id)
);

CREATE TABLE topups (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    user_id BIGINT NOT NULL,
    amount DECIMAL(10, 2) NOT NULL CHECK (amount > 0),
    currency TEXT NOT NULL DEFAULT 'usd' CHECK (currency IN ('usd', 'dollars')),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Enable Row Level Security
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;
ALTER TABLE order_items ENABLE ROW LEVEL SECURITY;
ALTER TABLE topups ENABLE ROW LEVEL SECURITY;

-- Policies for authenticated users to read data
CREATE POLICY "Allow authenticated read on users" ON users
    FOR SELECT USING (auth.role() = 'authenticated');
CREATE POLICY "Allow authenticated read on orders" ON orders
    FOR SELECT USING (auth.role() = 'authenticated');
CREATE POLICY "Allow authenticated read on order_items" ON order_items
    FOR SELECT USING (auth.role() = 'authenticated');

-- Policy for authenticated users to insert orders
CREATE POLICY "Allow authenticated insert on orders" ON orders
    FOR INSERT WITH CHECK (auth.role() = 'authenticated');
CREATE POLICY "Allow authenticated insert on order_items" ON order_items
    FOR INSERT WITH CHECK (auth.role() = 'authenticated');

-- RLS Policies for topups table
CREATE POLICY "Allow authenticated read on topups" ON topups
    FOR SELECT USING (auth.role() = 'authenticated' AND user_id = (auth.uid())::BIGINT);
CREATE POLICY "Allow authenticated insert on topups" ON topups
    FOR INSERT WITH CHECK (auth.role() = 'authenticated' AND user_id = (auth.uid())::BIGINT);

-- Create function to update users.amount after topup insert
CREATE OR REPLACE FUNCTION update_user_amount()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE users
    SET amount = amount + NEW.amount
    WHERE id = NEW.user_id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_user_amount
AFTER INSERT ON topups
FOR EACH ROW
EXECUTE FUNCTION update_user_amount();

