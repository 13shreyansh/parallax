CREATE DATABASE IF NOT EXISTS npov CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE npov;
CREATE TABLE IF NOT EXISTS article (
 lang CHAR(2) NOT NULL, page_id INT UNSIGNED NOT NULL, qid VARCHAR(24) NOT NULL,
 rev_id BIGINT UNSIGNED NOT NULL, title VARCHAR(255) NOT NULL,
 revised_at DATETIME(6) NOT NULL, text MEDIUMTEXT NOT NULL, origin VARCHAR(80) NOT NULL,
 PRIMARY KEY(lang,page_id), KEY(qid)
);
CREATE TABLE IF NOT EXISTS passage (
 id VARCHAR(64) CHARACTER SET ascii NOT NULL PRIMARY KEY, qid VARCHAR(24) NOT NULL, lang CHAR(2) NOT NULL,
 page_id INT UNSIGNED NOT NULL, rev_id BIGINT UNSIGNED NOT NULL, ordinal INT NOT NULL,
 section VARCHAR(255) NOT NULL, text TEXT NOT NULL, embedding VECTOR(384) NOT NULL,
 KEY(qid,lang), VECTOR INDEX passage_cosine (embedding) M=16 DISTANCE=cosine
);
-- Wikipedia valid time, explicitly imported from genuine revision timestamps.
-- Observation/fetch time is separate and never presented as Wikipedia edit time.
CREATE TABLE IF NOT EXISTS revision (
 lang CHAR(2) NOT NULL, page_id INT UNSIGNED NOT NULL, rev_id BIGINT UNSIGNED NOT NULL,
 title VARCHAR(255) NOT NULL, text MEDIUMTEXT NOT NULL,
 row_start TIMESTAMP(6) GENERATED ALWAYS AS ROW START INVISIBLE,
 row_end TIMESTAMP(6) GENERATED ALWAYS AS ROW END INVISIBLE,
 PERIOD FOR SYSTEM_TIME(row_start,row_end),
 PRIMARY KEY(lang,page_id), KEY(lang,page_id,row_start)
) WITH SYSTEM VERSIONING;
CREATE TABLE IF NOT EXISTS finding (
 id VARCHAR(64) CHARACTER SET ascii NOT NULL PRIMARY KEY, qid VARCHAR(24) NOT NULL, payload LONGTEXT NOT NULL
);
