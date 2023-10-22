from flask import Flask, render_template, request
import os
from dapr.clients import DaprClient
import json
import logging
from waitress import serve

app = Flask(__name__)

# get DAPR_APP from environment variable, or set default
dapr_app = os.environ.get('DAPR_APP', 'api')



@app.route('/')
def index():
    return render_template('index.html', result='')

@app.route('/submit', methods=['POST'])
def submit():
    text = request.form['text']
    bytes_data = json.dumps({'question': text}).encode('utf-8')

    # Make API call and get result (use Dapr)
    with DaprClient() as d:
        log.info(f"Making call to {dapr_app}")
        resp = d.invoke_method(dapr_app, 'generate', data=bytes_data,
                                 http_verb='POST', content_type='application/json')
        log.info(f"Response from API: {resp}")
    

    result = resp.json()['result']
    return render_template('index.html', result=result)

if __name__ == '__main__':
    # init logging
    logging.basicConfig(level=logging.INFO)
    log = logging.getLogger(__name__)
    serve(app, host="0.0.0.0", port=8001)