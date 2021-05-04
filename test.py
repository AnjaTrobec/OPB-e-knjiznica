from bottle import route, run, template

@route('/')
def index():
    return 'Jakoba pa ni danes!'

@route('/')
def banana():
    return 'Poglejmo če deluje.'
run(host='localhost', port=8080, reloader=True)
