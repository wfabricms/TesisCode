from flask import Flask
from flask import render_template, flash, redirect, request

app = Flask(__name__)
app.config.from_object('config')
@app.route('/', methods = ['GET', 'POST'])
def frontals():
        return render_template('frontal.html', 
        title = 'Web Servie Disambiguacion')	

from app import views
