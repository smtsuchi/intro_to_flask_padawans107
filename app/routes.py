from app import app
from flask import render_template

@app.route('/')
def homePage():
    people = ['name', "Brandt", "Aubrey","Nicole"]
    text = "SENDING THIS FROM PYTHON!!!"
    return render_template('index.html', people = people, my_text = text )


@app.route('/contact')
def contactPage():
    return render_template('contact.html')