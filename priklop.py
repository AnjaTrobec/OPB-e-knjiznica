import psycopg2, psycopg2.extensions, psycopg2.extras 
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)

from psycopg2 import sql

import csv

from auth import *

#UVOZ SQL SKRIPTE
def uvoziSQL(cur, datoteka):
    with open(datoteka) as f:
        skripta = f.read()
        cur.execute(skripta)

def uvoziCSV(cur, tabela):
    with open('obdelani-podatki/{0}.csv'.format(tabela), encoding='utf-8') as csvfile:
        podatki = csv.reader(csvfile)
        vsiPodatki = [vrstica for vrstica in podatki]
        glava = vsiPodatki[0]
        vrstice = vsiPodatki[1:]
        cur.executemany("INSERT INTO {0} ({1}) VALUES ({2})".format(
        tabela, ";".join(glava), ";".join(['%s']*len(glava))), vrstice)

def uvozi_knjigo(cur, tabela):
    with open('obdelani-podatki/{0}.csv'.format(tabela), encoding='utf-8') as csvfile:
        podatki = csv.reader(csvfile)
        glava = next(podatki)

        # pripravi predlogo za vstavljanje stolpcev
        stolpci = '(%s)' % ', '.join(['{}'] * len(glava))
        
        # pripravi predlogo za vstavljanje podatkov
        vrednosti = '(%s)' % ', '.join(['%s'] * len(glava))

         # vstavi ime tabele in stolpcev
        poizvedba = sql.SQL(" ".join(["INSERT INTO {}", stolpci, "VALUES", vrednosti])) \
            .format(sql.Identifier(tabela), *(sql.Identifier(stolpec) for stolpec in glava))

        for vrstica in podatki:
            
            #zamenjamo ime avtorja z id_avtorja
            avtor = vrstica[1]
            cur.execute("""SELECT id_avtorja FROM avtor WHERE ime = %s""", [avtor])
            try:
                vrstica[1], =cur.fetchone()
            except:
                continue

            if len(vrstica) == 0: #or len(vrstica) == 1:
                continue
            
            for i in range(len(vrstica)):
                vrstica[i] = str(vrstica[i])
            cur.execute(poizvedba, vrstica) # izvede poizvedbo

with psycopg2.connect(database=dbname, host=host, user=user, password=password) as con:
    cur = con.cursor()
    # uvoziSQL(cur, 'ogrodje_tabel.sql')
    # uvoziCSV(cur, 'avtor')
    uvozi_knjigo(cur, 'knjige')
    con.commit()