from flask import Flask, jsonify, request, make_response,render_template
from flask_cors import CORS
import json
from io import StringIO
import os

from flask_mail import Mail, Message

from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://pswolsyqshnyxt:7087154f143fbb70a3c7f0c5e34ebb13deb5c5abc2d37adef4acd61cc7a5c360@ec2-79-125-2-142.eu-west-1.compute.amazonaws.com:5432/dfssnvstarnqsc"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
from models import URLS, URLschema

# mail config
app.config['SECRET_KEY'] = 'top-secret!'
app.config['MAIL_SERVER'] = 'smtp.sendgrid.net'
app.config['MAIL_PORT'] = 25
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'azure_e3192891127d75b81cf5f2411881696d@azure.com'
app.config['MAIL_PASSWORD'] = os.environ.get('SENDGRID_API_KEY')
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




@app.before_first_request
def create_tables():
    db.create_all()




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


####MAIL
@app.route('/send', methods=['GET', 'POST'])
def send():
    response_object = {'status': "success"}
    if request.method == 'POST':
        recipient = request.get_json()
        recipients = recipient['mail']
        msg = Message('YOUR URLS LIST', recipients=[recipients])
        urls=URLS.query.all()
        url_schema = URLschema(many=True)
        io=StringIO()
        urli = url_schema.dump(urls)
        url_str=json.dump(urli,io)
        data=io.getvalue()
        #url_schema = URLschema(many=True)
        print(data)
        msg.body=data
        mail.send(msg)
        response_object['message'] = 'Maila Error'
    return response_object

if __name__ == '__main__':
    db.init_app(app)
    app.run()

