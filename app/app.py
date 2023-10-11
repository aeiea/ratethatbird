'''
RATE THAT BIRD
v0.1.0
'''
import flask, json
from random import sample, choice
from unidecode import unidecode

app = flask.Flask(__name__)

app.jinja_env.globals.update(round=round)

birds: list[dict] = json.load(open('app/birds.json'))

for i in birds:
    i['name'] = unidecode(i['name'])
    i['description'] = unidecode(i['description'])

def rateBird(id, rating):
    print(type(birds), type(birds[0]))
    def search(id):
        for i, v in enumerate(birds):
            print(v['id'], id)
            if v['id'] == id:
                return i
        return 'llamas are birds'
    i = search(id)
    print(i, id, rating)
    if i == 'llamas are birds':
        return 'llamas are birds'
    else:
        birds[i]['rating_count'] += 1
        birds[i]['rating'] = (birds[i]['rating'] * (birds[i]['rating_count'] - 1)  + int(rating)) / birds[i]['rating_count']
        return 'success'

@app.route('/')
def index():
    return flask.render_template('birds.html', birds = sample(birds, len(birds)), botd = choice(birds))

@app.route('/birds/<path:bird>')
def getimg(bird):
    return flask.send_file('birds/' + bird)
@app.route('/rate', methods=['POST'])
def rate():
    request = flask.request
    if request.method == 'POST':
        rateBird(request.form['id'].strip(), int(request.form['rating']))
        return flask.redirect('/')
    else:
        return 'what the hell are you doin'
app.run(port=443)