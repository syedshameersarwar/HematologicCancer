from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from .prediction import Predict

import os

load_dotenv()


app = Flask(__name__, static_folder='../client/dist/', static_url_path='/')
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/predict', methods=['POST'])
def uploadCsv():
    '''
    This fucntion does what it's name suggests, recieves the csv from frontend or 
    in future it will take csv/json from pipeline and then read it, process it and 
    make prediction over it. 
    '''
    uploadedfile = request.files['file']
    print('Recieved Dataeset for prediction: ', uploadedfile)

    if uploadedfile.filename != '':
        uploadedfile.save(uploadedfile.filename)

    predictor = Predict()
    payload = predictor.predictLogistic(str(uploadedfile.filename))
    return jsonify(payload)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))
    app.run(host='0.0.0.0', port=port)
