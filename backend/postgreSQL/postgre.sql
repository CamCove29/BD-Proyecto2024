CREATE database proyecto_dostres;

\c proyecto_dostres;

DROP TABLE IF EXISTS songs;

CREATE TABLE songs (
    track_id TEXT PRIMARY KEY,
    track_name TEXT,
    track_artist TEXT NULL,
    track_album_name TEXT,
    lyrics TEXT
);

\copy songs FROM 'C:/Users/Camila/Downloads/BD-Proyecto2024/backend/postgreSQL/spotify_songs_1000.csv' DELIMITER ',' CSV HEADER;

ALTER TABLE songs ADD COLUMN weighted_tsv tsvector;
ALTER TABLE songs ADD COLUMN weighted_tsv2 tsvector;

UPDATE songs
SET
    weighted_tsv = x.weighted_tsv,
    weighted_tsv2 = x.weighted_tsv
FROM (
    SELECT
        track_id,
        setweight(to_tsvector('english', COALESCE(track_name, '')), 'A') ||
        setweight(to_tsvector('english', COALESCE(lyrics, '')), 'B') AS weighted_tsv
    FROM songs
) AS x
WHERE x.track_id = songs.track_id;

SELECT weighted_tsv, weighted_tsv2 FROM songs;

CREATE INDEX weighted_tsv_idx1e3 ON songs USING GIN (weighted_tsv2);

--sin indice
VACUUM ANALYZE;
EXPLAIN ANALYZE
SELECT track_id, track_name, ts_rank_cd(weighted_tsv, query) AS rank
FROM songs, to_tsquery('english', 'imagination') query
WHERE query @@ weighted_tsv
ORDER BY rank DESC
LIMIT 10;

-- con indice
ANALYZE songs;
SET enable_seqscan = OFF;
EXPLAIN ANALYZE
SELECT track_id, track_name, ts_rank_cd(weighted_tsv2, query) AS rank
FROM songs, to_tsquery('english', 'imagination') query
WHERE query @@ weighted_tsv2
ORDER BY rank DESC
LIMIT 10;
