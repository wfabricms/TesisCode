#-*- coding: utf-8 -*-

import json
from app import app
from flask import jsonify
from flask import render_template, flash, redirect, request
import jinja2
from forms import *
from ExtractEntityLinkDBpedia import Procesar
from Etiquetado import ProcesarTextov1
from ConstruccionServicios import *

#import ExtractEntityLinkDBpedia

@app.route('/_add_numbers')
def add_numbers():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify(result=a + b)

@app.route('/')
def index():
    return render_template('index.html')

"""
@app.route('/')
@app.route('/index')
def index():
    user = { 'nickname': 'Fabricio' } # fake user
    return render_template("index.html",
                            title='home',
                            user=user)

"""
@app.route('/interfaz', methods = ['GET', 'POST'])
def interfaz():
        return render_template('interfaz.html', 
        title = 'Web Servie Disambiguacion')


@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for OpenID="' + form.openid.data + '", remember_me=' + str(form.remember_me.data))
        return redirect('/index')
    return render_template('login.html', 
        title = 'Sign In',
        form = form,
        providers = app.config['OPENID_PROVIDERS'])

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
        'done': False
    }
]

@app.route('/todo/api/v1.0/tasks', methods = ['GET'])
def get_tasks():
    return jsonify( { 'tasks': tasks } )

if __name__ == '__main__':
    app.run(debug = True)

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods = ['GET'])
def get_task(task_id):
    tasks = [
        {
            'id': 1,
            'title': u'Buy groceries',
            'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
            'done': False
        },
        {
            'id': 2,
            'title': u'Learn Python',
            'description': u'Need to find a good Python tutorial on the web', 
            'done': False
        }
    ]
    task = filter(lambda t: t['id'] == task_id, tasks)
    if len(task) == 0:
        abort(404)
    return jsonify( { 'task': task[0] } )

@app.route('/v1/entities/dbpedia/<string:text>', methods = ['GET'])
def entitiesNltkDbpedia(text):
    objProcesaTexto = Procesar()
    jsonResult = objProcesaTexto.ProcesarTextoNltkDBpedia(text)
    return jsonify( jsonResult )

@app.route('/v1/entities/<string:text>', methods = ['GET'])
def entities(text):
    objProcesaTexto = Procesar()
    jsonResult = objProcesaTexto.ProcesarTextoNltk(text)
    return jsonify( jsonResult )

@app.route('/v1/disambiguacion/<string:text>', methods = ['GET'])
def entitiesDisambiguacion(text):
    objProcesaTexto = ProcesarTextov1()
    jsonResult = objProcesaTexto.main(text)
    return jsonify(result = jsonResult)


@app.route('/v1/disambiguacionII/', methods = ['GET'])
def entitiesDisambiguacionII():
    text = request.args.get('text', "Loja capital of Ecuador")
    objProcesaTexto = ProcesarTextov1()
    jsonResult = objProcesaTexto.main(text)
    return jsonify(result = jsonResult)
    #return jsonify(result = json.dumps(jsonResult))

##!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

@app.route('/v1/TokensSentencias', methods = ['GET'])
def TokensSentencias():
    text = request.args.get('text', "Loja is the capital of Ecuador. Loja is here")
    objConstServ = ConstruccionServicios()
    result = objConstServ.TokenizacionSentencias(text)
    return jsonify(result = result)
    #return jsonify(result = json.dumps(jsonResult))

@app.route('/v1/Etiquetado', methods = ['GET'])
def Etiquetado():
    text = request.args.get('text', "Loja is the capital of Ecuador. Loja is here")
    objConstServ = ConstruccionServicios()
    result = objConstServ.EtiquetarTT(text)
    return jsonify(result = result)
    #return jsonify(result = json.dumps(jsonResult))

@app.route('/v1/ExtracionEntidades', methods = ['GET'])
def ExtracionEntidades():
    text = request.args.get('text', "Loja is the capital of Ecuador. Loja is here")
    objConstServ = ConstruccionServicios()
    result = objConstServ.ExtracionEntidadesAndKeywords(text)
    return jsonify(result = result)
    #return jsonify(result = json.dumps(jsonResult))
