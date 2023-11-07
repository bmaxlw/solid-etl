INSERT INTO jokes (joke_type, joke_setup, joke_punch)
SELECT
    s.joke_type,
    s.joke_setup,
    s.joke_punch
FROM staging s
ON CONFLICT (joke_setup) DO NOTHING;
