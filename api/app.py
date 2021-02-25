from flask import Flask, request, redirect, url_for
from flask_cors import CORS, cross_origin

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
    print(request.headers)
    print(request.files['file'])
    uploadedfile = request.files['file']
    print('FILE', uploadedfile)
    if uploadedfile.filename != '':
        uploadedfile.save(uploadedfile.filename)
    return "recieved!"


if __name__ == '__main__':
    app.run()
