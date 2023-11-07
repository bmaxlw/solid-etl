CREATE TABLE IF NOT EXISTS jokes (
    joke_id UUID DEFAULT gen_random_uuid() NOT NULL,
    joke_type VARCHAR(100),
    joke_setup VARCHAR(100) UNIQUE,
    joke_punch VARCHAR(100)
);
