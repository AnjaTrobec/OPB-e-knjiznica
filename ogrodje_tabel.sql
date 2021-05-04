ogrodje_tabel

DROP TABLE IF EXISTS avtor;
DROP TABLE IF EXISTS knjiga;
DROP TABLE IF EXISTS uporabnik;
DROP TABLE IF EXISTS transakcija;


    CREATE TABLE avtor (
    id_avtorja SERIAL PRIMARY KEY,
    ime TEXT NOT NULL,
    priimek TEXT NOT NULL
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
