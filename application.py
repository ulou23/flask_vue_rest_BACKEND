from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
import uuid
import os

from flask_mail import Mail, Message

from flask_sqlalchemy import SQLAlchemy

# instantiate the app
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://postgres:Freedom23@localhost:5432/vueflask"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
from models import URLS, URLschema

# mail config
app.config['SECRET_KEY'] = 'top-secret!'
app.config['MAIL_SERVER'] = 'smtp.sendgrid.net'
app.config['MAIL_PORT'] = 25
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'apikey'
app.config['MAIL_PASSWORD'] = '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' #os.environ.get('SENDGRID_API_KEY')
app.config['MAIL_DEFAULT_SENDER'] = 'lousalome23@gmail.com'

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})
mail = Mail(app)


#
# URLS = [
#   {
#       'id':uuid.uuid4().hex,
#       'urlinput': 'http://bootstrap.com',
#
#  }
#
# ]

####MAIL
@app.route('/send', methods=['GET', 'POST'])
def send():
    response_object = {'status': "success"}
    if request.method == 'POST':
        recipient = request.get_json()
        print(recipient['mail'])  # json i wtedy ...send : tresc
        recipients = recipient['mail']
        print(recipients)
        msg = Message('YOUR URLS LIST', recipients=[recipients])
        #urls=URLS.query.all()
        #url_schema = URLschema(many=True)

        mail.send(msg)
        response_object['message'] = 'Maila Error'
    return response_object


@app.before_first_request
def create_tables():
    db.create_all()


# def remove_url(url_id):
#    for u in URLS:
#        if u['id'] == url_id:
#            URLS.remove(u)
#            return URLS  #wczesniej bylo tu True i nie dzialalo
#    return False


#####REST API HTTP METHODS

# @app.route('/urls', methods=['GET', 'POST'])
# def all_urls():
#    response_object = {'status': 'success'}
#    if request.method == 'POST':
#        post_data = request.get_json()
#        URLS.append({                        #url_schema=URLschema()
#            'id': uuid.uuid4().hex,              # url,error =url_schema.load(data)
#            'urlinput': post_data.get('urlinput'),                 #  result= url_schema(url.create()).data
#        })
#        response_object['message'] = 'Url added!'
#    else:
#        response_object['urls'] = URLS
#    return jsonify(response_object)

@app.route('/urls', methods=['GET'])
def all_urls():
    db.create_all()
    get_urls = URLS.query.all()
    url_schema = URLschema(many=True)
    urls = url_schema.dump(get_urls)
    return make_response(jsonify({"urls": urls}))


@app.route('/urls', methods=['POST'])
def CREATE():
    data = request.get_json()
    url_schema = URLschema()
    url = url_schema.load(data, session=db.session)
    result = url_schema.dump(url.add())
    return make_response(jsonify({"url": result}))


# @app.route('/urls/<url_id>', methods=['PUT', 'DELETE'])
# def single_url(url_id):
#    response_object = {'status': 'success'}
#    if request.method == 'PUT':
#        post_data = request.get_json()
#        remove_url(url_id)
#        URLS.append({
#            'id': uuid.uuid4().hex,
#            'urlinput': post_data.get('urlinput')
#        })
#        response_object['message'] = 'URL updated!'
#    if request.method == 'DELETE':
#        remove_url(url_id)
#        response_object['message'] = 'URL removed!'
#    return jsonify(response_object)

@app.route('/urls/<url_id>', methods=['PUT', 'DELETE'])
def single_url(url_id):
    if request.method == 'PUT':
        post_data = request.get_json()
        get_url = URLS.query.get(url_id)
        if post_data.get('id'):
            get_url.id = post_data['id']
        if post_data.get('urlinput'):
            get_url.urlinput = post_data['urlinput']

        db.session.add(get_url)
        db.session.commit()
        url_schema = URLschema(only=['id', 'urlinput'])
        url = url_schema.dump(get_url)
        return make_response(jsonify({"url": url}))

    if request.method == 'DELETE':
        get_url = URLS.query.get(url_id)
        db.session.delete(get_url)
        db.session.commit()

        get_urls = URLS.query.all()
        url_schema = URLschema(many=True)
        urls = url_schema.dump(get_urls)
        return make_response(jsonify({"urls": urls}))


if __name__ == '__main__':
    db.init_app(app)
    app.run()
