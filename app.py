from flask import Flask, jsonify, request
from flask_cors import CORS


# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})



URLS = [
    {
        'urlinput': 'On the Road',

    },
    {
        'urlinput': 'Harry Potter and the Philosopher\'s Stone',

    },
    {
        'urlinput': 'Green Eggs and Ham',


    }
]




@app.route('/urls', methods=['GET', 'POST'])
def all_urls():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        URLS.append({ 'urlinput': post_data.get('urlinput'),
        })
        response_object['message'] = 'Url added!'
    else:
        response_object['urls'] = URLS
    return jsonify(response_object)








if __name__ == '__main__':
    app.run()