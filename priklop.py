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
        tabela, ";".join(glava), ";".join(['%s']*len(glava))), vrstice)

def uvozi_knjigo(cur, tabela):
    with open('obdelani-podatki/{0}.csv'.format(tabela), encoding='utf-8') as csvfile:
        podatki = csv.reader(csvfile, delimiter=';')
        vsiPodatki = [vrstica for vrstica in podatki]
        glava = vsiPodatki[0]
        glava = glava[0].strip()
        vrstice = vsiPodatki[1:]
        vrstice1 = []
        for i in range(len(vrstice)):
            vrstica = vrstice[i][0].strip()
            vrstica = vrstica.split(';')
            vrstice1.append(vrstica)
        #print(vrstice1)
        #print(len(vrstice1))
# do sem je zdej okej, te vrtice1 so zrihtane

        for i in range(len(vrstice1)):
            avtor = vrstice1[i][1] #problem, ker ločuje tudi po vejicah namesto samo po ;
            print(avtor)
            vrstice1[i][2]=int(vrstice1[i][2])
            cur.execute("""SELECT id_avtorja FROM avtor WHERE ime = %s""", (avtor,))
            try:
                vrstice1[i][2], = cur.fetchone()
            except:
                continue
        cur.executemany("""INSERT INTO {0} ({1}) VALUES ({2})""".format(
        tabela, ",".join(glava), ",".join(['%s']*len(glava))), vrstice1)

with psycopg2.connect(database=dbname, host=host, user=user, password=password) as con:
    cur = con.cursor()
    # uvoziSQL(cur, 'ogrodje_tabel.sql')
    # uvoziCSV(cur, 'avtor')
    uvozi_knjigo(cur, 'knjige')
    con.commit()