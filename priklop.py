import psycopg2, psycopg2.extensions, psycopg2.extras
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)

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
        tabela, ",".join(glava), ",".join(['%s']*len(glava))), vrstice)

with psycopg2.connect(database=db, host=host, user=user, password=password) as con:
    cur = con.cursor()
    uvoziSQL(cur, 'ogrodje_tabel.sql')
<<<<<<< HEAD
    #uvoziCSV(cur, 'knjige')
    # uvoziCSV(cur, 'agencije')
    # uvoziNepremicnineCSV(cur, 'nepremicnine')
    # uvoziCSV(cur, 'uporabniki')
=======
    # uvoziCSV(cur, 'knjige')
>>>>>>> 77e9d57cef166c5c375c96d7b287562bb2259f10
    con.commit()