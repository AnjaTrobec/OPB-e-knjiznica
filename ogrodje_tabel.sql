
DROP TABLE IF EXISTS knjige;

    CREATE TABLE knjige (
        -- id_knjige SERIAL PRIMARY KEY,
        id_knjiga INTEGER,
        ime_knjiga TEXT NOT NULL,
        link TEXT,
        id_avtor TEXT,
        ime_avtor TEXT,
        ocena TEXT NOT NULL,
        stevilo_ocen REAL,
        kljucna_ocena TEXT,
        stevilo_kritik TEXT
);

    CREATE TABLE avtor (
    id_avtorja SERIAL PRIMARY KEY,
    ime TEXT NOT NULL,
    priimek TEXT NOT NULL
);
    
    CREATE TABLE uporabnik (
        ime TEXT NOT NULL,
        id_uporabnika SERIAL PRIMARY KEY,
        priimek TEXT NOT NULL,
        username TEXT NOT NULL,
        geslo TEXT NOT NULL,
        email TEXT NOT NULL,
        narocnina INTEGER
);
    CREATE TABLE transakcija(
        id_transakcije SERIAL PRIMARY KEY,
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

