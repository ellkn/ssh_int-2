-- CREATE DATABASE int_ssh
--     WITH
--     OWNER = postgres
--     ENCODING = 'UTF8'
--     CONNECTION LIMIT = -1
--     IS_TEMPLATE = False;


BEGIN;


CREATE TABLE IF NOT EXISTS public.history
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY,
    ip text NOT NULL,
    os text NOT NULL,
    version text NOT NULL,
    build text NOT NULL,
    architecture text NOT NULL,
    "time" timestamp without time zone NOT NULL,
    PRIMARY KEY (id)
);
END;