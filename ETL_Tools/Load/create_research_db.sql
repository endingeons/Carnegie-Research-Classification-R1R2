CREATE DATABASE IF NOT EXISTS research;
USE research;

DROP TABLE IF EXISTS research_uni;
DROP TABLE IF EXISTS uni_stats;


CREATE TABLE research_uni(
university_key     INT          PRIMARY KEY,
name               VARCHAR(500)    NOT NULL,
city               VARCHAR(500)    NOT NULL,
state              VARCHAR(500)    NOT NULL,
level              VARCHAR(500)    NOT NULL,
control            VARCHAR(500)    NOT NULL,
undergrad_program  VARCHAR(500)    NOT NULL,
graduate_program   VARCHAR(500)    NOT NULL,
enrollment_profile VARCHAR(500)    NOT NULL,
undergrad_profile VARCHAR(500)    NOT NULL,
size_setting       VARCHAR(500)    NOT NULL,
basic              VARCHAR(500)    NOT NULL,
community_engagement               VARCHAR(500)    NOT NULL
);

CREATE TABLE uni_stats(
uni_stats_key        INT     PRIMARY KEY        AUTO_INCREMENT,
university_key       INT     NOT NULL,
CONSTRAINT fk_university_key FOREIGN KEY (university_key)
REFERENCES research_uni (university_key),
serd                    INT     NOT NULL,
nonserd                 INT     NOT NULL,
pdnfrstaff              INT     NOT NULL,
facnum                  INT     NOT NULL,
socsc_rsd               INT     NOT NULL,
hum_rsd                 INT     NOT NULL,
stem_rsd                INT     NOT NULL,
oth_rsd                 INT     NOT NULL,
pct_full_time_grad      DECIMAL(6, 1)     NOT NULL,
pct_research_space      DECIMAL(6, 1)     NOT NULL
);