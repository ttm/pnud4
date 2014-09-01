#-*- coding: utf8 -*-
from flask import Flask, render_template, make_response, session, redirect, url_for, escape, request,jsonify,Response   
import __builtin__, datetime
from dateutil import parser
import time as T, networkx as x, json # json.dumps
import cPickle, string
from SPARQLWrapper import SPARQLWrapper, JSON

atime=T.time()
from configuracao import *
from auxiliar import *
fazRedeAmizades()
print(T.time()-atime)
fazRedeInteracao()
print(T.time()-atime)
fazBoW()
print(T.time()-atime)
fazBoWs()
print(T.time()-atime)

import rotinasRecomendacao
app = Flask(__name__)

@app.route("/hello2/")
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
    destinatário: para quem está sendo feita a recomendação: participante, comunidade ou linha_editorial. Campo auxiliar ``idd'' para id do destinatário (comunidade ou participante). É identifier da tabela profiles.
    método: método para a recomendação: top(ológico), tex(tual) ou hib(rido). Campo auxiliar de polaridade sim(ilar), dis(similar) ou mis(ta).

    Exemplo:
    =======
    http://<urlDoServidor>/recomenda?recurso=participante&destinatario=comunidade&idd=mirosc&metodo=top&polaridade=mis"""
    # recomendar perfil para perfil
    recurso=     request.args.get("recurso")
    destinatario=request.args.get("destinatario")
    idd=         request.args.get("idd")
    metodo=      request.args.get("metodo")
    polaridade=  request.args.get("polaridade")
    if recurso=="participante":
        rec=rotinasRecomendacao.recomendaParticipante(destinatario,idd,metodo,polaridade)
    if recurso=="comunidade":
        rec=rotinasRecomendacao.recomendaComunidade(destinatario,idd,metodo,polaridade)
    if recurso=="trilha":
        rec=rotinasRecomendacao.recomendaTrilha(destinatario,idd,metodo,polaridade)
    if recurso=="artigo":
        rec=rotinasRecomendacao.recomendaArtigo(destinatario,idd,metodo,polaridade)
    if recurso=="comentario":
        rec=rotinasRecomendacao.recomendaComentario(destinatario,idd,metodo,polaridade)
    return json.dumps(rec)

    
    
    return "tudo"+request.args.get("coisa")+request.args["aquela"]
if __name__ == "__main__":
    app.debug = True
    print T.time()-atime
    #app.run(host='0.0.0.0.0')
    #app.run(host='localhost',port=83)
    #app.run(host='127.0.0.1',port=84)
    app.run(host='127.0.0.1',port=884)
