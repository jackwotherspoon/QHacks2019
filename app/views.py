from flask import render_template
from app import app
from app.date import getDate

@app.route('/home')
def default():
    calendarData=getDate()
    return render_template('base.html', calendar_date=calendarData)