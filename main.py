from flask import Flask, render_template, request

app = Flask(
  __name__,
  template_folder='templates',
  static_folder='static'
)


@app.route('/', methods=['GET', 'POST'])
def posts():
    if request.method == 'GET':
        return render_template('index.html', hello_world="print")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)