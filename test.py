from bottle import route, run, template

@route('/')
def index():
    return 'Ali dela?'

@route('/')
def banana():
    return 'Oj.'
run(host='localhost', port=8080, reloader=True)
