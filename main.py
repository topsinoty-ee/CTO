from flask import Flask, render_template, request
import os
from api import company_table, company_records, search_record_by_id

app = Flask(
  __name__,
  template_folder='templates',
  static_folder='static'
)

#db?

@app.route('/', methods=['GET'])
def posts():
    return render_template('index.html')


@app.route('/job-offers', methods=['GET'])
def job_offers():
    return render_template('job_offers.html')

@app.route('/all-companies', methods=['GET'])
def all_companies():
    return render_template(
        './all_companies.html',
        company_records=company_records, search=search_record_by_id
    )


@app.route('/new-hires', methods=['GET'])
def new_hires():
    return render_template('look_hires.html')


@app.route('/browse-all', methods=['GET'])
def browse_all():
    return render_template('browse_all.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)