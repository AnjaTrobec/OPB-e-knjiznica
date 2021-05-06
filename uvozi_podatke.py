import sqlite3
baza_datoteka = 'eknjiznica.db'

def uvoziSQL(cur, datoteka):
    with open(datoteka) as f:
        koda = f.read()
        cur.executescript(koda)

def uvoziCSV(cur, tabela):
    with open('obdelani-podatki/{0}.csv'.format(tabela)) as csvfile:
        podatki = csv.reader(csvfile)
        vsiPodatki = [vrstica for vrstica in podatki]
        glava = vsiPodatki[0]
        vrstice = vsiPodatki[1:]
        cur.executemany('''INSERT INTO {0} ({1}) VALUES ({2})'''.format(tabela, ','.join(glava), ','.join(['?']*len(glava))), vrstice)

with sqlite3.connect(baza_datoteka) as baza:
    cur = baza.cursor()
    uvoziSQL(cur, 'eknjiznica.sql')
    uvoziCSV(cur, 'obdelani-podatki/avtorji')
    uvoziCSV(cur, 'obdelani-podatki/knjige')
    uvoziCSV(cur, 'obdelani-podatki/ocena')
