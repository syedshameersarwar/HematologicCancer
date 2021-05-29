from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from prediction import Predict


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


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
    app.run(debug=True)
