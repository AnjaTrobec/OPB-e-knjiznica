from bottle import *
import sqlite3

# KONFIGURACIJA
baza_datoteka = 'eknjiznica.db'

# Odkomentiraj, če želiš sporočila o napakah
debug(True)  # za izpise pri razvoju

@get('/')
def index():
    return 'UPAJMO DA BO DELALO'

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
            oseba = cur.execute("SELECT * FROM uporabnik WHERE username = ?", (username, )).fetchone()
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
    geslo = request.forms.geslo
    if username is None or geslo is None:
        nastaviSporocilo('Uporabniško ima in geslo morata biti neprazna') 
        redirect('/prijava')
    cur = baza.cursor()    
    hashBaza = None
    try: 
        hashBaza = cur.execute("SELECT geslo FROM uporabnik WHERE username = ?", (username, )).fetchone()
        hashBaza = hashBaza[0]
    except:
        hashBaza = None
    if hashBaza is None:
        nastaviSporocilo('Uporabniško ime ali geslo nista ustrezni') 
        redirect('/prijava')
        return
    if hashGesla(geslo) != hashBaza:
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
    cur = baza.cursor()
    uporabnik = cur.execute("""
    SELECT ime,priimek,username,geslo,email FROM uporabnik
    ORDER BY uporabnik.username""")
    return template('uporabnik.html', uporabnik=uporabnik, napaka=napaka)

@post('/uporabnik/brisi/<username>')
def brisi_uporabnika(username):
    oseba = preveriUporabnika()
    if oseba is None: 
        return
    cur = baza.cursor()
    try:
        cur.execute("DELETE FROM uporabnik WHERE username = ?", (username, ))
    except:
        nastaviSporocilo('Brisanje osebe z UPORABNIŠKIM IMENOM {0} ni bilo uspešno.'.format(username)) 
    redirect('/uporabnik')

@post('/uporabnik/dodaj') 
def dodaj_uporabnik_post():
    oseba = preveriUporabnika()
    if oseba is None: 
        return
    ime = request.forms.ime
    priimek = request.forms.priimek
    username = request.forms.username
    geslo = request.forms.geslo
    email = request.forms.email
    cur = baza.cursor()
    cur.execute("INSERT INTO oseba (ime, priimek, username, geslo, email) VALUES (?, ?, ?, ?, ?)", 
         (ime, priimek, username, geslo, email))
    redirect('/uporabnik')


@get('/uporabnik/uredi/<username>')
def uredi_komitenta_get(username):
    oseba = preveriUporabnika()
    if oseba is None: 
        return
    cur = baza.cursor()
    uporabnik = cur.execute("SELECT ime, priimek, username, geslo, email FROM uporabnik WHERE username = ?", (username,)).fetchone()
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
    cur.execute("UPDATE oseba SET ime = ?, priimek = ?, novi_username = ?, geslo = ?, email = ? WHERE username = ?", 
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
        uporabnik = cur.execute("SELECT * FROM uporabnik WHERE username = ?", (username, )).fetchone()
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
    cur.execute("UPDATE uporabnik SET password = ? WHERE username = ?", (zgostitev, username))
    response.set_cookie(username, secret=skrivnost)
    redirect('/uporabnik')




baza = sqlite3.connect(baza_datoteka, isolation_level=None)
baza.set_trace_callback(print) # izpis sql stavkov v terminal (za debugiranje pri razvoju) TO PRI PRAVI APLIKACIJI UGASNEŠ
# zapoved upoštevanja omejitev FOREIGN KEY
cur = baza.cursor()
cur.execute("PRAGMA foreign_keys = ON;")
run(host='localhost', port=8080, reloader=True) # reloader=True nam olajša razvoj (ozveževanje sproti - razvoj)