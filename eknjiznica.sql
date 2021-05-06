DROP TABLE IF EXISTS avtor;
DROP TABLE IF EXISTS knjiga;
DROP TABLE IF EXISTS uporabnik;
DROP TABLE IF EXISTS transakcija;


    CREATE TABLE avtor (
    id_avtorja SERIAL PRIMARY KEY,
    ime TEXT NOT NULL
);
    
    CREATE TABLE knjiga (
        id_knjige SERIAL PRIMARY KEY,
        st_ocen NOT NULL
        avtor TEXT NOT NULL FOREIGN KEY,
        naslov TEXT NOT NULL,
        povprecna_ocena INTEGER NOT NULL,
        cena_nakupa INTEGER NOT NULL,
        cena_izposoje INTEGER NOT NULL
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
<<<<<<< HEAD


--GRANT SELECT ON DATABASE sem2020_domenfb TO javnost;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO javnost;
GRANT INSERT ON ALL TABLES IN SCHEMA public TO javnost;
GRANT DELETE ON  "public"."priljubljene" TO javnost;
=======
>>>>>>> 8e3cac79ce03340b62e2b0ad64b19ec30231b988
