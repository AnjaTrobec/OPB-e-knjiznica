from bottleext import *

import auth_public as auth

import psycopg2, psycopg2.extensions, psycopg2.extras 
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)

import hashlib

# KONFIGURACIJA

#Privzete nastavitve
SERVER_PORT = os.environ.get('BOTTLE_PORT', 8080)
RELOADER = os.environ.get('BOTTLE_RELOADER', True)
ROOT = os.environ.get('BOTTLE_ROOT', '/')
DB_PORT = os.environ.get('POSTGRES_PORT', 5432)

# Odkomentiraj, če želiš sporočila o napakah
debug(True)  # za izpise pri razvoju

@get('/')
def index():
    redirect('/prijava')

def nastaviSporocilo(sporocilo = None):
    staro = request.get_cookie("sporocilo", secret=skrivnost)
    if sporocilo is None:
        response.delete_cookie('sporocilo')
    else:
        response.set_cookie('sporocilo', sporocilo, path="/", secret=skrivnost)
    return staro 

def preveriUporabnika(): 
    username = request.get_cookie("username", secret=skrivnost)
    if username:
        cur = baza.cursor()    
        oseba = None
        try: 
            cur.execute("SELECT * FROM uporabnik WHERE username = %s", (username, ))
            oseba = cur.fetchone()
            print(oseba)  #v oseba se shranijo vsi podatki o uporabniku
        except:
            oseba = None
        if oseba: 
            return oseba
    redirect('/prijava')

def hashGesla(s):
    m = hashlib.sha256()
    m.update(s.encode("utf-8"))
    return m.hexdigest()

# Mapa za statične vire (slike, css, ...)
static_dir = "./static"

skrivnost = "rODX3ulHw3ZYRdbIVcp1IfJTDn8iQTH6TFaNBgrSkjIulr"

@route("/static/<filename:path>")
def static(filename):
    return static_file(filename, root=static_dir)

@get('/prijava')
def prijava_get():
    napaka = nastaviSporocilo()
    return template('prijava.html', napaka=napaka)

@post('/prijava')
def prijava_post():
    username = request.forms.username
    geslo = request.forms.password
    if username is None or geslo is None:
        nastaviSporocilo('Uporabniško ime in geslo morata biti neprazna') 
        redirect('/prijava')
    cur = baza.cursor()    
    hashBaza = None
    try: 
        cur.execute("SELECT geslo FROM uporabnik WHERE username = %s", (username, ))
        hashBaza, = cur.fetchone()
        print(hashBaza)
        print(geslo)
    except Exception as x:
        hashBaza = None
        print(x)
    if hashBaza is None:
        nastaviSporocilo('Uporabniško ime ali geslo nista ustrezni') 
        redirect('/prijava')
        return
    if geslo != hashBaza:
        nastaviSporocilo('Uporabniško ime ali geslo nista ustrezni') 
        redirect('/prijava')
        return
    response.set_cookie('username', username, secret=skrivnost)
    redirect('/uporabnik')


@get('/odjava')
def odjava_get():
    response.delete_cookie('username')
    redirect('/prijava')


####--UPORABNIK--######

@get('/uporabnik')
def uporabnik():
    oseba = preveriUporabnika()
    if oseba is None: 
        return
    napaka = nastaviSporocilo()
    return template('uporabnik.html', oseba=oseba, napaka=napaka)

@post('/uporabnik/brisi/<username>')
def brisi_uporabnika(username):
    oseba = preveriUporabnika()
    if oseba is None: 
        return
    cur = baza.cursor()
    try:
        cur.execute("DELETE FROM uporabnik WHERE username = %s", (username, ))
    except:
        nastaviSporocilo('Brisanje osebe z UPORABNIŠKIM IMENOM {0} ni bilo uspešno.'.format(username)) 
    redirect('/uporabnik')

# @post('/uporabnik/dodaj') 
# def dodaj_uporabnik_post():
#     oseba = preveriUporabnika()
#     if oseba is None: 
#         return
#     ime = request.forms.ime
#     priimek = request.forms.priimek
#     username = request.forms.username
#     geslo = request.forms.geslo
#     email = request.forms.email
#     cur = baza.cursor()
#     cur.execute("INSERT INTO oseba (ime, priimek, username, geslo, email) VALUES (%s, %s, %s, %s, %s)", 
#          (ime, priimek, username, geslo, email))
#     redirect('/uporabnik')


@get('/uporabnik/uredi/<username>')
def uredi_komitenta_get(username):
    oseba = preveriUporabnika()
    if oseba is None: 
        return
    cur = baza.cursor()
    uporabnik = cur.execute("SELECT ime, priimek, username, geslo, email FROM uporabnik WHERE username = %s", (username,)).fetchone()
    return template('uporabnik-edit.html', uporabnik=uporabnik, naslov="Uredi uporabnika")

@post('/uporabnik/uredi/<username>')
def uredi_uporabnik_post(username):
    oseba = preveriUporabnika()
    if oseba is None: 
        return
    ime = request.forms.ime
    priimek = request.forms.priimek
    novi_username = request.forms.novi_username
    geslo = request.forms.geslo
    email = request.forms.email

    cur = baza.cursor()
    cur.execute("UPDATE oseba SET ime = %s, priimek = %s, novi_username = %s, geslo = %s, email = %s WHERE username = %s", 
         (ime, priimek, novi_username, geslo, email, username))
    redirect('/uporabnik')

@get('/registracija')
def registracija_get():
    napaka = nastaviSporocilo()
    return template('registracija.html', napaka=napaka)

@post('/registracija')
def registracija_post():
    username = request.forms.username
    password = request.forms.password
    password2 = request.forms.password2
    if username is None or password is None or password2 is None:
        nastaviSporocilo('Registracija ni možna') 
        redirect('/registracija')
        return
    cur = baza.cursor()    
    uporabnik = None
    try: 
        uporabnik = cur.execute("SELECT * FROM uporabnik WHERE username = %s", (username, )).fetchone()
    except:
        uporabnik = None
    if uporabnik is None:
        nastaviSporocilo('Registracija ni možna') 
        redirect('/registracija')
        return
    if len(password) < 4:
        nastaviSporocilo('Geslo mora imeti vsaj 4 znake.') 
        redirect('/registracija')
        return
    if password != password2:
        nastaviSporocilo('Gesli se ne ujemata.') 
        redirect('/registracija')
        return
    zgostitev = hashGesla(password)
    cur.execute("UPDATE uporabnik SET password = %s WHERE username = %s", (zgostitev, username))
    response.set_cookie(username, secret=skrivnost)
    redirect('/uporabnik')




baza = psycopg2.connect(database=auth.dbname, host=auth.host, user=auth.user, password=auth.password, port = DB_PORT)
cur = baza.cursor()

run(host='localhost', port=8080, reloader=True) # reloader=True nam olajša razvoj (ozveževanje sproti - razvoj)