#-*- coding: utf8 -*-
from flask import Flask, render_template, make_response, session, redirect, url_for, escape, request,jsonify,Response   
import __builtin__, datetime
from dateutil import parser
import time as T, networkx as x, json # json.dumps
import cPickle as pickle, string
from SPARQLWrapper import SPARQLWrapper, JSON

atime=T.time()
from configuracao import *
from auxiliar import *
try:
    __builtin__.g=pickle.load( open( "pickledir/g.p", "rb" ) )
    __builtin__.d=pickle.load( open( "pickledir/d.p", "rb" ) )
    __builtin__.bow=pickle.load( open( "pickledir/bow.p", "rb" ) )
    __builtin__.radicais_escolhidos=pickle.load( open( "pickledir/radicais_escolhidos.p", "rb" ) )
    __builtin__.bows=pickle.load( open( "pickledir/bows.p", "rb" ) )
    print(T.time()-atime)
except:
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
    return "bar3"
@app.route("/hello5/")
def foo2():
    return "bar5"

@app.route("/atualiza/")
def atualiza():
    atime=T.time()
    foo=""
    fazRedeAmizades()
    foo+=str(T.time()-atime)
    fazRedeInteracao()
    foo+="<br />"+str(T.time()-atime)
    fazBoW()
    foo+="<br />"+str(T.time()-atime)
    fazBoWs()
    foo+="<br />"+str(T.time()-atime)
    return "atualizado!"+foo
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
    http://<urlDoServidor>/recomenda?recurso=participante&destinatario=comunidade&idd=mirosc&metodo=topologico&polaridade=mis&ordenacao=intercalada"""
    # recomendar perfil para perfil
    recurso=     request.args.get("recurso")
    destinatario=request.args.get("destinatario")
    idd=         request.args.get("idd")
    metodo=      request.args.get("metodo")
    polaridade=  request.args.get("polaridade")
    ordenacao=  request.args.get("ordenacao")
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
if __name__ == "__main__":
    app.debug = True
    print T.time()-atime
    #app.run(host='0.0.0.0.0')
    #app.run(host='localhost',port=83)
    #app.run(host='127.0.0.1',port=84)
    app.run(host='127.0.0.1',port=884)
