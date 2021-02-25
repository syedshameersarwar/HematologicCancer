from flask import Flask, request
from flask_cors import CORS, cross_origin
from prediction import Predict

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/')
@cross_origin()
def hello():
    return "Hello World!"

@app.route('/flask/get-response')
def response():
    return "Yo mayn"

@app.route('/flask/upload-csv', methods=['POST'])
def uploadCsv():
    uploadedfile = request.files['files']
    if uploadedfile.filename != '':
        uploadedfile.save(uploadedfile.filename)
        
    pred = Predict()
    result = pred.predictLogistic(uploadedfile.filename)
    
    return result


if __name__ == '__main__':
    app.run()
