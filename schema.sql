--DROP DATABASE IF EXISTS gains;
--CREATE DATABASE gains;

--CREATE EXTENSION IF NOT EXISTS hstore;
--CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
--CREATE EXTENSION IF NOT EXISTS pgcrypto;

--alter database gains OWNER TO gains ;

     
DROP TABLE IF EXISTS gains_user;
  

DROP TABLE IF EXISTS session;
CREATE TABLE session (
    uuid uuid DEFAULT uuid_generate_v4() NOT NULL,
    properties hstore default ''::hstore,
    created timestamp without time zone DEFAULT now(),
    modified timestamp without time zone DEFAULT now()
);


ALTER TABLE session OWNER TO gains;


