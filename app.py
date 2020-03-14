from flask import Flask, jsonify, request
from flask_cors import CORS
import uuid

from flask_mail import Mail, Message

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

#mail config
app.config['SECRET_KEY'] = ''
app.config['MAIL_SERVER'] = ''
app.config['MAIL_PORT'] = ''
app.config['MAIL_USE_TLS'] = ''
app.config['MAIL_USERNAME'] = ''
app.config['MAIL_PASSWORD'] = ''
app.config['MAIL_DEFAULT_SENDER'] =''

mail=Mail(app)
# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})



URLS = [
    {
        'id':uuid.uuid4().hex,
        'urlinput': 'http://bootstrap.com',

    },
    {
        'id':uuid.uuid4().hex,
        'urlinput': 'https://koty.org',

    },
    {
        'id':uuid.uuid4().hex,
        'urlinput': 'https://onet.pl',
    }
]

####MAIL
@app.route('/send',methods=['GET','POST'])
def send():
    response_object ={'status': "success"}
    if request.method == 'POST':
        recipient = request.get_data(as_text=True)
        print(recipient)# json i wtedy ...send : tresc
        #msg = Message('Your Urls', recipients=[recipient['mail']])
        # msg.html('<h1>ooooo<h2>')
        #mail.send(msg)
        response_object['message'] = 'Mail sended'
    else:
        response_object['message'] = 'Maila Error'
    return response_object



def remove_url(url_id):
    for u in URLS:
        if u['id'] == url_id:
            URLS.remove(u)
            return URLS  #wczesniej bylo tu True i nie dzialalo
    return False

#####REST API HTTP METHODS

@app.route('/urls', methods=['GET', 'POST'])
def all_urls():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        URLS.append({
            'id': uuid.uuid4().hex,
            'urlinput': post_data.get('urlinput'),
        })
        response_object['message'] = 'Url added!'
    else:
        response_object['urls'] = URLS
    return jsonify(response_object)


@app.route('/urls/<url_id>', methods=['PUT', 'DELETE'])
def single_url(url_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json()
        remove_url(url_id)
        URLS.append({
            'id': uuid.uuid4().hex,
            'urlinput': post_data.get('urlinput')
        })
        response_object['message'] = 'URL updated!'
    if request.method == 'DELETE':
        remove_url(url_id)
        response_object['message'] = 'URL removed!'
    return jsonify(response_object)





if __name__ == '__main__':
    app.run()