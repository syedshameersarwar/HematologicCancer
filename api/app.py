from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from prediction import Predict


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/predict', methods=['POST'])
def uploadCsv():
    uploadedfile = request.files['file']
    print('Recieved Dataeset for prediction: ', uploadedfile)
    if uploadedfile.filename != '':
        uploadedfile.save(uploadedfile.filename)
    predictor = Predict()
    predictions = predictor.predictLogistic(str(uploadedfile.filename))
    return jsonify(predictions)


if __name__ == '__main__':
    app.run(debug=True)
