from project import app  #projectの部分
from flask import render_template

@app.route('/')
def index():
    return render_template(
        'index.html'
    )