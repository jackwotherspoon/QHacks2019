from flask import render_template
from app import app

@app.route('/')
def default():
    return render_template('base.html')