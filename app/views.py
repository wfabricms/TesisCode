#-*- coding: utf-8 -*-

import json
from app import app
from flask import jsonify
from flask import render_template, flash, redirect, request
import jinja2
from ConstruccionServicios import *

#import ExtractEntityLinkDBpedia

##!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

@app.route('/v1/TokensSentencias', methods = ['GET'])
def TokensSentencias():
    text = request.args.get('text', "Loja is the capital Loja province.")
    objConstServ = ConstruccionServicios()
    result = objConstServ.TokenizacionSentencias(text)
    return jsonify(result = result)
    #return jsonify(result = json.dumps(jsonResult))

@app.route('/v1/TokensPalabra', methods = ['GET'])
def TokenizarPalabras():
    text = request.args.get('text', "Loja is the capital Loja province")
    objConstServ = ConstruccionServicios()
    result = objConstServ.TokenizarTT(text)
    return jsonify(result = result)

@app.route('/v1/Etiquetado', methods = ['GET'])
def Etiquetado():
    text = request.args.get('text', "Loja is the capital Loja province")
    objConstServ = ConstruccionServicios()
    result = objConstServ.EtiquetarTT(text)
    return jsonify(result = result)
    #return jsonify(result = json.dumps(jsonResult))

@app.route('/v1/ExtracionEntidades', methods = ['GET'])
def ExtracionEntidades():
    text = request.args.get('text', "Loja is the capital Loja province")
    objConstServ = ConstruccionServicios()
    result = objConstServ.ExtracionEntidadesAndKeywords(text, 0)
    return jsonify(result = result)
    #return jsonify(result = json.dumps(jsonResult))

@app.route('/v1/Desambiguacion', methods = ['GET'])
def DesamabiguacionEntidades():
    text = request.args.get('text', "Loja is the capital Loja province")
    objConstServ = ConstruccionServicios()
    result = objConstServ.ExtracionEntidadesAndKeywords(text, 1)
    return jsonify(result = result)
    #return jsonify(result = json.dumps(jsonResult))

@app.route('/frontal', methods = ['GET', 'POST'])
def frontal():
        return render_template('frontal.html', 
        title = 'Web Servie Disambiguacion')

@app.route('/contactos', methods = ['GET', 'POST'])
def contactos():
        return render_template('contactos.html', 
        title = 'Web Servie Disambiguacion')

@app.route('/desarrollo', methods = ['GET', 'POST'])
def desarrollo():
        return render_template('desarrollo.html', 
        title = 'Web Servie Disambiguacion')