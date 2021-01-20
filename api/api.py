from flask import Flask, redirect, url_for, request, abort, render_template
import json
import os
import shutil
import time
import requests
app = Flask(__name__)
from flask_cors import CORS, cross_origin
cors = CORS(app)


@app.route('/test',methods = ['POST', 'GET'])
@cross_origin()
def test():
    if request.method == 'POST':
        print(request.headers)
        print(request.data)
        if not request.json:
            abort(400)
        print(request.json)
        return json.dumps(request.json)
    else:
        user = request.args.get('name')
        return 'hello %s' % user

@app.route('/hello/<name>')
@cross_origin()
def hello(name):
    return 'welcome %s' % name

@app.route('/',methods = ['POST', 'GET'])
@cross_origin()
def landing():
    if request.method == 'POST':
        return redirect(url_for('hello',name = user))
    else:
        tenplates_loc = "templates"
        shutil.rmtree(tenplates_loc, ignore_errors = True)
        os.mkdir(tenplates_loc)
        url = 'https://raw.githubusercontent.com/pravin-dsilva/ocp-install-dashboard/html-bootstrap/ocp-form.html'
        r = requests.get(url, allow_redirects=True)
        open(tenplates_loc + '/index.html', 'wb').write(r.content)

        message = "OpenShift on Power Deployment"
        return render_template('index.html', message=message)


@app.route('/deploy',methods = ['POST', 'GET'])
@cross_origin()
def deploy():
    if request.method == 'POST':
        print(request.form)
        if not request.form:
            abort(400)
        data = request.form
        if "name" in data:
            name = data["name"]
            description = data["description"]
            ocpversion = data["ocpversion"]
        else:
            print('ERROR : Cluster Name not provided')

        #call jenkins
        #write to db

        return json.dumps(data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8088, debug=True, threaded=True)
