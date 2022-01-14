from unicodedata import name
from flask import Flask
from flask import render_template
app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    name = 'asd'
    return render_template(r"E:\Phogramozas\fizika_AI\index.html", title = 'WElcome', username=name)

if __name__ == '__main__':
    app.run()
