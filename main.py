from flask import Flask, render_template, request
import os
from pyairtable import Api
from pyairtable.api import table

# api = Api(os.environ['pat9ZkQrlG86qrIS3.56e36daf14e1b08a011a1115dd63412566eafde15bd2cc576df328d71d45665f'])
# company_table = api.table('Veric', 'Company')
# company_records = company_table.all()

app = Flask(
  __name__,
  template_folder='templates',
  static_folder='static'
)

#db?

@app.route('/', methods=['GET'])
def posts():
    if request.method == 'GET':
        return render_template('index.html')


@app.route('/job-offers', methods=['GET'])
def job_offers():
    if request.method == 'GET':
        return render_template('job_offers.html')


@app.route('/new-hires', methods=['GET'])
def new_hires():
    if request.method == 'GET':
        return render_template('look_hires.html')


@app.route('/browse-all', methods=['GET'])
def browse_all():
    if request.method == 'GET':
        return render_template('browse_all.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)