import json
import re
import requests
import orodja

vzorec_bloka = re.compile(
    r'<tr itemscope itemtype="http://schema.org/Book".*?'
    r'</div>\s*</td>\s*</tr>',
    flags=re.DOTALL
)

vzorec_knjige = re.compile(
    r'<div id="(?P<id_knjiga>.+?)".*?'
    r'data-resource-type="Book">\n.*<a title="(?P<ime_knjiga>.+?)".*?' #zajamem naslove
    r'<a class="bookTitle" itemprop="url" href="/book/show/(?P<link>.+?)".*?'
    r'"https://www.goodreads.com/author/show/(?P<id_avtor>.+?)\..*?".*?'
    r'itemprop="name">(?P<ime_avtor>.*?)<' , #zajamem avtorje
    flags=re.DOTALL
)

vzorec_ocene = re.compile(
    r'<span class="minirating">.*?</span></span>'
    r'(?P<ocena>.*?)'
    r'avg rating &mdash; '
    r'(?P<stevilo_ocen>.*?) ratings',
    flags=re.DOTALL
)

vzorec_kritike = re.compile(
    r'<span class="smallText uitext">.*?'
    r'score: (?P<kljucna_ocena>.*?)</a>.*?'
    r'return false;">(?P<stevilo_kritik>.*?) people voted',
    flags=re.DOTALL
)


def izloci_podatke_knjige(blok):
    knjiga = vzorec_knjige.search(blok).groupdict()
    knjiga['id_knjiga']= knjiga['id_knjiga']
    knjiga['ime_knjiga'] = knjiga['ime_knjiga']
    knjiga['id_avtor'] = knjiga['id_avtor']
    knjiga['link'] = knjiga['link']
    knjiga['ime_avtor'] = knjiga['ime_avtor']

    povp_ocena = vzorec_ocene.search(blok)
    knjiga['ocena'] = povp_ocena['ocena']
    knjiga['stevilo_ocen'] = povp_ocena['stevilo_ocen'] 

    koncna_ocena =vzorec_kritike.search(blok)
    knjiga['kljucna_ocena']=koncna_ocena['kljucna_ocena']
    knjiga['stevilo_kritik'] = int(float(koncna_ocena['stevilo_kritik'].replace(',','')))

    return knjiga


def knjige_na_strani(st_strani, na_stran = 100):
    url = (
        'https://www.goodreads.com/list/show/'
        '1.Best_Books_Ever?'
        f'page={st_strani}'
    )
    ime_datoteke = f'htmlji/knjige-{st_strani}.html'
    orodja.shrani_spletno_stran(url, ime_datoteke)
    vsebina = orodja.vsebina_datoteke(ime_datoteke)
    for blok in vzorec_bloka.finditer(vsebina):
        yield izloci_podatke_knjige(blok.group(0))

knjige = []
for st_strani in range(1,7):
    for knjiga in knjige_na_strani(st_strani, 100):
        knjige.append(knjiga)

knjige.sort(key=lambda ocena: knjiga['ocena'])

orodja.zapisi_csv(
    knjige,
    ['id_knjiga', 'ime_knjiga', 'link', 'id_avtor', 
    'ime_avtor', 'ocena','stevilo_ocen','kljucna_ocena',
    'stevilo_kritik'], 'obdelani-podatki/knjige.csv'
)

def izloci_gnezdene_podatke(knjige):
    avtorji, url_zanri = [], []
    
    for knjiga in knjige:
            avtorji.append({'id_avtor':knjiga['id_avtor'], 'ime_avtor':knjiga['ime_avtor']})
            url_zanri.append(knjiga['link'])
        
    return avtorji, url_zanri

avtorji, url_zanri = izloci_gnezdene_podatke(knjige)
orodja.zapisi_csv(avtorji, ['id_avtor', 'ime_avtor'], 'obdelani-podatki/avtorji.csv')

vzorec_bloka_zanra = re.compile(
    r'<script>.*?googletag.cmd.push.*?'
    r'googletag.enableServices().*?</script>',
    flags=re.DOTALL
)

vzorec_zanra = re.compile(
    r'googletag.pubads().setTargeting("shelf", (?P<zanri>.*?)).*?'
    r'googletag.pubads().setTargeting("resource", "Work_(?P<id_filma>.*?)")',
    flags = re.DOTALL
)

def izloci_podatke_zanrov(blok):
    zanri = vzorec_zanra.search(blok)
    if zanri:
        zanri.groupdict()
        print (zanri)
        zanri['id_filma'] = zanri['id_filma']
        zanri['zanri'] = zanri['zanri']
    return zanri

print(re.search(re.compile('d'), 'danes je lep dan'))
print('htmlji-knjig-posebej/1.Harry_Potter_and_the_Half_Blood_Prince.html')
vsebina = orodja.vsebina_datoteke('htmlji-knjig-posebej/1.Harry_Potter_and_the_Half_Blood_Prince.html')

blok = re.finditer(vzorec_bloka_zanra, vsebina)
print(blok)
#izloci_podatke_zanrov(blok.group(0))


def zanri_url(seznam):
    for konec in seznam:
        url = (
            'https://www.goodreads.com/book/show/'
            f'{konec}'
            )
        ime_datoteke = f'htmlji-knjig-posebej/{konec}.html'
        orodja.shrani_spletno_stran(url, ime_datoteke)
        vsebina = orodja.vsebina_datoteke(ime_datoteke)
        blok = re.finditer(vzorec_zanra, vsebina)
        print(blok)
        #yield izloci_podatke_zanrov(blok.group(0))

zanri_url(url_zanri)

#zanri = []
#for knjiga in zanri_url(url_zanri):
    #zanri.append(knjiga)