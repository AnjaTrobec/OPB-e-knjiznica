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
    with open('testni-podatki/{0}.csv'.format(tabela), encoding='utf-8') as csvfile:
        podatki = csv.reader(csvfile)
        vsiPodatki = [vrstica for vrstica in podatki]
        glava = vsiPodatki[0]
        vrstice = vsiPodatki[1:]
        cur.executemany("INSERT INTO {0} ({1}) VALUES ({2})".format(
        tabela, ",".join(glava), ",".join(['%s']*len(glava))), vrstice)

def uvozi_knjigo(cur, tabela):
    with open('testni-podatki/{0}.csv'.format(tabela), encoding='utf-8') as csvfile:
        podatki = csv.reader(csvfile)
        vsiPodatki = [vrstica for vrstica in podatki]
        glava = vsiPodatki[0]
        vrstice = vsiPodatki[1:]
        for i in range(len(vrstice)):
            avtor = vrstice[i][1]
            cur.execute("SELECT id_avtorja FROM avtor WHERE ime = %s", [avtor])
            try:
                vrstice[i][1], = cur.fetchone()
            except:
                continue
        cur.executemany("INSERT INTO {0} ({1}) VALUES ({2})".format(
        tabela, ",".join(glava), ",".join(['%s']*len(glava))), vrstice)

with psycopg2.connect(database=dbname, host=host, user=user, password=password) as con:
    cur = con.cursor()
    uvoziSQL(cur, 'ogrodje_tabel.sql')
    # uvoziCSV(cur, 'test-avtor')
    # uvoziCSV(cur, 'test-knjiga')
    # uvoziCSV(cur, 'test-uporabnik')
    con.commit()