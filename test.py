from bottle import route, run, template

@route('/')
def index():
    return 'Ali dela?'

@route('/')
def banana():
    return 'Poglejmo če deluje.'
run(host='localhost', port=8080, reloader=True)
