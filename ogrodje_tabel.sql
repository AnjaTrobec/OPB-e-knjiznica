
-- DROP TABLE IF EXISTS avtor ;
-- DROP TABLE IF EXISTS uporabnik;
-- DROP TABLE IF EXISTS transakcija;
-- DROP TABLE IF EXISTS knjige;


--     CREATE TABLE avtor (
--     id_avtorja SERIAL PRIMARY KEY,
--     ime TEXT NOT NULL
-- );
    
--     CREATE TABLE uporabnik (
--         ime TEXT NOT NULL,
--         id_uporabnika SERIAL PRIMARY KEY,
--         priimek TEXT NOT NULL,
--         username TEXT NOT NULL UNIQUE,
--         geslo TEXT NOT NULL,
--         email TEXT NOT NULL UNIQUE,
--         narocnina TEXT NOT NULL
-- );


--     CREATE TABLE knjige (
--     id_knjige SERIAL PRIMARY KEY,
--     naslov TEXT NOT NULL,
--     id_avtorja INTEGER REFERENCES avtor(id_avtorja),
--     cena_nakupa INTEGER
-- );

--     CREATE TABLE transakcija(
--         id_transakcije SERIAL PRIMARY KEY,
--         id_uporabnika INTEGER REFERENCES uporabnik (id_uporabnika),
--         id_knjige INTEGER REFERENCES knjige (id_knjige),
--         tip TEXT,
--         datum DATE NOT NULL DEFAULT (datetime('now'))
--  );


    CREATE TABLE vse_transakcije (
    id_transakcije SERIAL PRIMARY KEY,
    id_uporabnika INTEGER REFERENCES uporabnik (id_uporabnika),
    id_knjige INTEGER REFERENCES knjige (id_knjige),
    tip TEXT,
    datum DATE NOT NULL
);

GRANT ALL ON DATABASE sem2021_anamarijab TO anjat;
GRANT ALL ON SCHEMA public TO anjat;
GRANT ALL ON ALL TABLES IN SCHEMA public TO anjat;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO anjat;

GRANT ALL ON DATABASE sem2021_anamarijab TO jakobz;
GRANT ALL ON SCHEMA public TO jakobz;
GRANT ALL ON ALL TABLES IN SCHEMA public TO jakobz;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO jakobz;

GRANT ALL ON DATABASE sem2021_anamarijab TO javnost;
GRANT ALL ON SCHEMA public TO javnost;
GRANT ALL ON ALL TABLES IN SCHEMA public TO javnost;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO javnost;

