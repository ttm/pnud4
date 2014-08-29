#-*- coding: utf8 -*-
from flask import Flask, render_template, make_response, session, redirect, url_for, escape, request,jsonify,Response   
import __builtin__, datetime
from dateutil import parser
import time as T, networkx as x, json # json.dumps
import cPickle

app = Flask(__name__)
atime=T.time()

@app.route("/hello/")
def foo():
    return "bar"
@app.route("/tudo")
def tudo():
    return "tudo"+request.args.get("coisa")+request.args["aquela"]
@app.route("/recomenda/")
def recomenda():
    """Implementa recomendação de recursos para o participa.

    Parâmetros:
    ==========
    recurso: o recurso a ser recomendado: participantes, comunidades, trilhas, artigos ou comentários.
    destinatário: para quem está sendo feita a recomendação: participante, comunidade ou linha editorial. Campo auxiliar ``idd'' para id do destinatário (comunidade ou participante).
    método: método para a recomendação: top(ológico), tex(tual) ou hib(rido). Campo auxiliar de polaridade sim(ilar), dis(similar) ou mis(ta).

    Exemplo:
    =======
    http://<urlDoServidor>/recomenda?recurso=participante&destinatario=comunidade&idd=mirosc&metodo=top&polaridade=mis"""
    return "tudo"+request.args.get("coisa")+request.args["aquela"]
if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')
