#-*- coding: utf8 -*-
from SPARQLWrapper import SPARQLWrapper, JSON
from configuracao import *
import string, networkx as x, nltk as k
import __builtin__
stemmer = k.stem.RSLPStemmer()

def fazRedeAmizades():
    global SPARQLWrapper
    q="""SELECT ?a ?b ?aname ?bname
       WHERE {
          ?a foaf:knows ?b .
       }"""
    sparql=SPARQLWrapper(URL_ENDPOINT_)
    sparql.setQuery(PREFIX+q)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    g=x.Graph()
    for amizade in results["results"]["bindings"]:
        nome1=amizade["a"]["value"]
        nome2=amizade["b"]["value"]
        g.add_edge(nome1,nome2)
    __builtin__.g=g


def fazRedeInteracao():
    q="""SELECT ?participante1 ?participante2 ?aname ?bname
       WHERE {
           ?comentario dc:type tsioc:Comment.
           ?participante1 ops:performsParticipation ?comentario.
           ?participante1 foaf:name ?aname.
           ?artigo sioc:has_reply ?comentario.
           ?participante2 ops:performsParticipation ?artigo.
           ?participante2 foaf:name ?bname.
       }"""
    sparql=SPARQLWrapper(URL_ENDPOINT_)
    sparql.setQuery(PREFIX+q)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    d=x.DiGraph()
    for interacao in results["results"]["bindings"]:
        nome_chegada=interacao["participante1"]["value"]
        nome_partida=interacao["participante2"]["value"]
        if (nome_partida,nome_chegada) in d.edges():
            d[nome_partida][nome_chegada]["weight"]+=1
        else:
            d.add_edge(nome_partida,nome_chegada,weight=1.)
    __builtin__.d=d

def fazBoW():
    """Faz Bag of Words de todos os comentários e artigos do site"""
    q="SELECT ?cbody ?titulo ?abody WHERE \
               {?foo ops:performsParticipation ?participacao.\
              OPTIONAL { ?participacao schema:articleBody ?abody. }\
              OPTIONAL {?participacao dc:title ?titulo . }\
               OPTIONAL {?participacao schema:text ?cbody .}}"
    sparql=SPARQLWrapper(URL_ENDPOINT_)
    sparql.setQuery(PREFIX+q)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    msgs_=results["results"]["bindings"]
    msgs=[mm for mm in msgs_ if ("titulo" not in mm.keys()) or
          (("teste de stress" not in mm["titulo"]["value"].lower())
          or ("cbody" not in mm.keys() or ("comunidade de desenvolvedores e nesse caso, quanto mais"
               not in mm["cbody"]["value"].lower())))]
    textos1=[i["cbody"]["value"] for i in msgs if "cbody" in i.keys()]
    textos2=[i["abody"]["value"] for i in msgs if "abody" in i.keys()]
    textos=textos1+textos2
    # faz BoW e guarda num dict
    texto=string.join(textos).lower()
    texto_= ''.join(ch for ch in texto if ch not in EXCLUDE)

    texto__=texto_.split()
    #texto___=[stemmer.stem(pp) for pp in texto__]
    texto___=[stemmer.stem(pp) for pp in texto__ if (pp not in STOPWORDS) and (not pp.isdigit())]
    fdist=k.FreqDist(texto___)
    radicais_escolhidos=fdist.keys()[:400]
    __builtin__.radicais_escolhidos=radicais_escolhidos
    __builtin__.bow=fdist

def fazBoWs():
    """Faz Bag of Words de cada usuário"""
    # puxa todos os usuarios
    q="""SELECT DISTINCT ?participante
           WHERE {
              ?foo dc:contributor ?participante .
           }"""
    sparql=SPARQLWrapper(URL_ENDPOINT_)
    sparql.setQuery(PREFIX+q)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    participantes_=results["results"]["bindings"]
    participantes=[i["participante"]["value"] for i in participantes_]
    # inicia loop
    if "radicais_escolhidos" not in dir(__builtin__):
        print(u"rode BoW antes, para saber do vocabulário geral do portal")
    else:
        radicais_escolhidos=__builtin__.radicais_escolhidos
    bows={}
    for participante in participantes:
        # puxa todos os comentarios de cada usuario
        # e os article bodys
        q="""SELECT DISTINCT ?abody ?cbody
             WHERE {
               <%s> ops:performsParticipation ?participacao.
                 OPTIONAL { ?participacao schema:articleBody ?abody. }
                 OPTIONAL { ?participacao schema:text ?cbody. }
                 OPTIONAL {?comentario dc:title ?titulo . }
             }"""%(participante,)
        sparql = SPARQLWrapper("http://localhost:82/participabr/query")
        sparql.setQuery(PREFIX+q)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        results_=results["results"]["bindings"]
        results__=[mm for mm in results_ if ("titulo" not in mm.keys()) or
          (("teste de stress" not in mm["titulo"]["value"].lower())
          or ("cbody" not in mm.keys() or ("comunidade de desenvolvedores e nesse caso, quanto mais"
               not in mm["cbody"]["value"].lower())))]

        textos1=[i["cbody"]["value"] for i in results__ if "cbody" in i.keys()]
        textos2=[i["abody"]["value"] for i in results__ if "abody" in i.keys()]
        textos=textos1+textos2
        # faz BoW e guarda num dict
        texto=string.join(textos).lower()
        texto_= ''.join(ch for ch in texto if ch not in EXCLUDE)
        texto__=texto_.split()
        texto___=[stemmer.stem(pp) for pp in texto__ if pp not in STOPWORDS]
        fdist=k.FreqDist(texto___)
        ocorrencias=[fdist[i] for i in radicais_escolhidos]
        bows[participante]=(fdist,ocorrencias)
    __builtin__.bows=bows

def fazBoWsC():
    """Faz Bag of Words de cada comunidade

    Por hora, há duas bag of words para cada comunidade:
    *) Média das bag of words de cada participante
    *) Bag of words de todos os textos da comunidade"""
    if "bows" not in dir(__builtin__):
        return "execute fazBoWs() primeiro"
    # puxar participantes de cada comunidade
    # fazer media dos bows deles

    # puxar texto relacionado a cada comunidade
    # fazer bow
